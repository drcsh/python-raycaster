from engine.entities.bullet import Bullet
from engine.level_objects.level import Level
from engine.entities.player import Player


class BulletBehaviour:

    @classmethod
    def act(cls, bullet: Bullet, level: Level, player: Player):
        """
        Updates the bullet location and handles it hitting something (e.g. an
        enemy, or the player)
        """

        new_x, new_y = bullet.get_next_move_location()

        if level.wall_at_location(new_x, new_y):
            bullet.kill()
            return

        enemy = level.enemy_near_location(new_x, new_y)
        if enemy:
            enemy.take_damage(bullet.damage)
            bullet.kill()
            return

        # Todo: allow bullets to damage player. Caveat: bullet spawns on player location and is moved!

        bullet.move(new_x, new_y)
