from engine.player_objects.weapons.bullet_stats import BulletStats
from textures.texturemap import TextureMap

# TODO: convert to dataclass or put methods for animation and shooting here?
class PlayerWeapon:

    def __init__(self, display_name: str, ammo: int, cooldown: int, texture_map: TextureMap, bullet_stats: BulletStats):
        self.display_name = display_name
        self.ammo = ammo
        self.cooldown = cooldown
        self.texture_map = texture_map
        self.bullet_stats = bullet_stats

        self.cooldown_until = 0
