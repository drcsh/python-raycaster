# python-raycaster

A simple 2.5D raycasting shooter built with python and pygame-ce.

The basic premise is based on [ssloy's tinyraycaster](https://github.com/ssloy/tinyraycaster).

It's built in Python because:
1. I'm not well versed in C++, and didn't want to distract myself learning the language instead of the
internals of a raycaster, so I decided to convert ssloy's code to Python as I went.
2. I am interested in extracting as much performance from Python as possible.

For performance and ease of image processing, I decided to use pygame-ce (pygame Community Edition), the actively maintained fork of pygame. 

# Requirements

Python 3.10.x, pip, and the packages in requirements.txt

# Running
With a virtualenv set up with requirements installed, simply
`python3 core.py`

# Features

Currently starting the game puts you straight into the only level. Enemies walk towards you and
try to attack you. You can shoot them (spacebar). After 2 hits, they die. If they get close, they will attack
and try to kill you.

![](/screenshots/may_2021.gif)

# Algorithm and Performance

I keep notes on the algorithm and discussion of its performance and performance improvements in a separate file, 
[click here for algorithm and performance discussion](/docs/algorithm_and_performance.md)




