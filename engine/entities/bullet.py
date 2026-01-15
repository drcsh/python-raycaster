import math
from typing import Tuple

import pygame

from engine.entities.game_object import GameObject
from engine.utils import math_utils
from engine.surfaces.surface_map import SurfaceMap


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
                 surface_map: SurfaceMap,
                 size: int = DEFAULT_SIZE,
                 damage: int = DEFAULT_DAMAGE
                 ):
        self.angle = angle
        self.speed = speed
        self.size = size
        self.damage = damage

        self.cos_angle = math.cos(angle)
        self.sin_angle = math.sin(angle)

        super().__init__(sprite_group, x, y, surface_map)

    def get_next_move_location(self) -> Tuple[float, float]:
        """
        This method is just a wrapper for the math_utils function at the
        moment, but is preserved so it can be overwritten for interesting
        movement behaviours, e.g. homing missiles.
        """
        return math_utils.get_new_coordinates(self.x, self.y, self.angle, self.speed)

    def move(self, new_x: float, new_y: float):
        """
        Update bullet location.
        Todo: Bullet animations!
        """
        self.x = new_x
        self.y = new_y
