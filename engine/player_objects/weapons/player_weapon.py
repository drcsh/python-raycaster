from typing import Callable
from textures.texturemap import TextureMap


class PlayerWeapon:

    def __init__(self, ammo: int, cooldown: int, texture: TextureMap, bullet_class: Callable):
        """
        Data class for tracking player weapon
        :param ammo:
        :param cooldown:
        :param texture:
        :param bullet_class:
        """
        self.ammo = ammo
        self.cooldown = cooldown
        self.texture = texture
        self.bullet_class = bullet_class

        self.cooldown_until = 0
