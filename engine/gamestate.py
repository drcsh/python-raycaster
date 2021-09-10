from engine.behaviours.bullet_behaviour import BulletBehaviour
from engine.behaviours.enemy_behaviour import EnemyBehaviour
from engine.level_objects.level import Level
from engine.player_objects.player import Player


class GameState:
    """
    This is the top level object which tracks everything within the game world
    and handles coordination between them.

    Todo: provide save and load functionality!
    """

    def __init__(self, player: Player, level: Level):

        self.player = player
        self.level = level

    def update(self):

        self.update_enemies()
        self.update_bullets()

    def update_enemies(self):

        for enemy in self.level.enemies:
            EnemyBehaviour.act(enemy, self.level, self.player)

    def update_bullets(self):

        for bullet in self.level.bullets:
            BulletBehaviour.act(bullet, self.level, self.player)


