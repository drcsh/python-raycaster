import math

from engine.game_objects.bullet import Bullet
from textures.texturemap import TextureMap


class Player:
    TURNSPEED = 10 * math.pi / 360
    MOVESPEED = 0.2

    def __init__(self, x, y, angle, level):
        self.x = x
        self.y = y
        self.angle = angle
        self.level = level

    def move(self, speed):
        """
        Move the player_objects at self.angle by the given speed. Positive numbers for forwards, negative for backwards.

        The player_objects is prevented from moving through enemies and walls.

        :param speed:
        :return:
        """
        new_x = self.x + speed * math.cos(self.angle)
        new_y = self.y + speed * math.sin(self.angle)

        if self.level.wall_at_location(new_x, new_y):
            return

        if self.level.enemy_near_location(new_x, new_y):
            return

        self.x = new_x
        self.y = new_y

    def move_forward(self):
        self.move(self.MOVESPEED)

    def move_backward(self):
        self.move(-self.MOVESPEED)

    def turn_left(self):
        self.angle -= self.TURNSPEED
        self._check_angle()

    def turn_right(self):
        self.angle += self.TURNSPEED
        self._check_angle()

    def shoot(self, gamestate):

        # TODO: Get equipped weapon
        # TODO: check weapon equipped has ammo
        # TODO: trigger weapon firing animation
        # TODO: Get bullet characteristics for weapon
        b_speed = 0.4
        b_texturemap = TextureMap.load_common('simple_bullet.png')
        b_damage = 25

        # create bullet object with self.angle and weapon speed
        bullet = Bullet(
            sprite_group=gamestate.level.bullets,
            x=self.x,
            y=self.y,
            angle=self.angle,
            speed=b_speed,
            texturemap=b_texturemap,
            damage=b_damage
        )

        # trigger bullet move immediately to get it infront of the player and check for impact
        bullet.move(gamestate)
        print("BANG!")

    def _check_angle(self):
        """
        when we turn we're modifying the player_objects angle by a fraction of pi. If this angle goes > 2pi or < 0 we need to
        reset it to prevent other calculations getting thrown out.
        :return:
        """
        if self.angle > math.tau:
            self.angle -= math.tau
        elif self.angle < 0:
            self.angle += math.tau
