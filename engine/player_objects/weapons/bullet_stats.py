from dataclasses import dataclass

from textures.texturemap import TextureMap


@dataclass
class BulletStats:
    """
    Variables for initialising instances of a certain type of bullet, e.g. pistol bullets.
    """
    speed: int
    damage: int
    texture_map: TextureMap
