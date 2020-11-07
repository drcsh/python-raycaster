# python-raycaster

I've always wanted to build one of these, so I decided to try building one based on 
tinyraycaster (https://github.com/ssloy/tinyraycaster). However, I'm not well versed 
in C++, and didn't want to distract myself learning the language instead of the 
internals of a raycaster, so I decided to convert ssloy's code to Python as I went. 
My commits will (initially at least) follow ssloy's.  

For performance and ease of image processing, I decided to use pygame. 

# Requirements

Python 3, pip, and the packages in requirements.txt

# Running
With a virtualenv set up with requirements installed, simply
`python3 core.py`

# Raycasting Calculation

In ssloy's original raycaster, we start at the player coordinates x,y with a player angle
which is in relation to the x axis. This angle will be the center of the player's field of
view.
 
For each vertical column of pixels we want on the render area, we work out the angle of
that column in relation to the player's angle, and do some trigonometry to work out a 
point 0.05 of a map tile along a theoretical line (ray) at that angle from the player. 

We then do this in a loop, basically travelling down the ray at 0.05 map tiles per 
iteration until we hit a wall. We then work out where on the texture of that wall the
ray has hit, and render it to scale depending on how far away the ray now is from the
player.

However, while this works well in C++, it's slow in Python, with each full raycast 
of the screen averaging at about 0.56s. What we really need is rendering times at < 0.016s
to get 60fps. The faster, the better. So I started refining the algorithm. 

## Method of checking
I set up a timeit timer either side of the call to the raycaster in the game loop, collected 100 calls to it (that's
100 full renderings), and printed the average to the terminal.

While timing I left the camera in the default position, with a wide view reaching down to the end of the map. 

## Version 2

To improve the situation I decided that rather than travelling the whole length of the
ray, we're only really interested in where the ray passes into another map square, at
that's the only location we may encounter a wall (since walls are always 1x1 square).

To work out these points of interest (POIs), we solve the linear equation of the ray, and
knowing which direction the ray is traveling in relation to the x and y axis, we can
calculate where the ray will cross those lines. We then take the closest one as our
ray location, and keep hopping along these POIs until we hit a wall.

This is significantly more efficient, clocking in at 0.04 to 0.07s per full sweep. 

## Version 3
I switched computer and virtualization environment (VirtualBox to Hyper-V), and started at
average raycast times around about 0.021-0.027s for a full sweep. 

My initial theories on where to go from here:
1. reduce the number of times the distance equation is called. Cache POIs and the distance
to the next unused POI so it doesn't have to be recalculated.
2. cache the results of the linear equations and retrieve them if available.

When timing these equations, the distance equation was, as expected, the slowest, but even
that was clocking in at <0.0000007s 

I tried caching the distances between points in a dict so that when we are working out the next closest
POI, we may not have to run the distance calculation, but the overhead of the caching slowed
down the function by a factor of 6

I also tried various strategies to squeeze more speed out of the math itself, i.e. trying 
different ways of structuring the equations, or using different built in libs (e.g. math.pow() instead of **2), 
but each change slowed down the rendering time.

I then switched to looking at the Texture load time. I realised I was re-slicing the textures
again and again for no real reason, so I modified Texture into two separate classes, one of which
pre-sliced the textures into 1px wide strips for raycasting. This produced a minor performance 
gain, getting us to raycast times of about 0.019-0.025s 

## Squeezing more out of it
I started out with some experiments, for example, the raycaster does a bit of packing coordinates in tuples and 
retrieving them, and this is really only to give tidy method signatures. I tried unpacking the tuples, but there
wasn't an observable impact on rendering time, so I put them back to their original state.

I disabled the visibility cone rendering as this was only for demonstration. I suspected that had an overhead for 
setting individual pixel colours. This saved about 0.03-0.04s from each render. I switched the map + visibility cone
rendering to an optional setting (to enable, set dev_mode=True in core.py). I'm still seeing cast times up to 0.025s
however, and it's stubbornly not going down to less than 0.02s.

Next I simplified the POI calculations by removing some sanity checks. This would theoretically mean it could generate
POIs outside of the map area, but it should always hit a wall before calculating them anyway. I also did a pass through
of the code removing unnecessary calculations and simplifying the logical structure, especially on the code called
frequently. After doing this, cast times got down to <0.02s and frequently under the 0.0167s required for 60 fps. 

I then went back to my previous idea of removing the tuple juggling, and accepting the messy method signatures. This
got cast times down just a hair further, 

# In Action

Basic version with fisheye correction: 

![](/screenshots/basic_version.gif)

Now with textures!:

![](/screenshots/textures_loading.gif)

Hopping along our points of interest for a faster render:

![](/screenshots/efficient_casting.gif)

Now with enemies!

![](/screenshots/now_with_enemies.gif)

Enemies can now move and have some animations but they cannot attack. Hug simulator 2020?

![](/screenshots/hug_simulator.gif)
