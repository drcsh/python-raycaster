import math
from typing import Tuple

import pygame

from engine.game_objects.game_object import GameObject
from textures.texturemap import TextureMap


class Bullet(GameObject):

    DEFAULT_SIZE = 10
    DEFAULT_COLOR = (0, 255, 255)
    DEFAULT_DAMAGE = 10

    def __init__(self,
                 sprite_group: pygame.sprite.Group,
                 x: float,
                 y: float,
                 angle: float,
                 speed: float,
                 texturemap: TextureMap,
                 size: int = DEFAULT_SIZE,
                 damage: int = DEFAULT_DAMAGE
                 ):
        self.angle = angle
        self.speed = speed
        self.size = size
        self.damage = damage

        self.cos_angle = math.cos(angle)
        self.sin_angle = math.sin(angle)

        super().__init__(sprite_group, x, y, texturemap)

    def get_next_move_location(self) -> Tuple[float, float]:
        """
        Work out the next location the bullet will inhabit
        """
        new_x = self.x + self.speed * math.cos(self.angle)
        new_y = self.y + self.speed * math.sin(self.angle)

        return new_x, new_y

    def move(self, new_x: float, new_y: float):
        """
        Update bullet location.
        Todo: Bullet animations!
        """
        self.x = new_x
        self.y = new_y
