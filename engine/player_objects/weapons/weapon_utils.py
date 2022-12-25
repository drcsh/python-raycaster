from typing import Dict

from engine.player_objects.weapons.bullet_stats import BulletStats
from engine.player_objects.weapons.player_weapon import PlayerWeapon
from textures.texturemap import TextureMap


def load() -> Dict:
    # TODO: Get these from a file instead of hardcoded
    pistol_bullet_stats = BulletStats(
        speed=0.2,
        damage=251,
        texture_map=TextureMap.load_common('simple_bullet.png')
    )
    pistol = PlayerWeapon(
        display_name="Pistol",
        ammo=100,
        cooldown=1,
        texture_map=TextureMap.load_common('simple_bullet.png'),  # TODO: Weapon texture!
        bullet_stats=pistol_bullet_stats
    )

    return {
        'pistol': pistol
    }
