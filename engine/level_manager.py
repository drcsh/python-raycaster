from engine.behaviours.bullet_behaviour import BulletBehaviour
from engine.behaviours.enemy_behaviour import EnemyBehaviour
from engine.level_objects.level import Level
from engine.player_objects.player import Player
from engine.utils.exceptions import LevelCompleteException


class LevelManager:
    """
    LevelManager stiches together the Player and Level objects to provide a higher level
    interface for managing the state of the game level. It proves an easy interface for triggering the behaviour of
    all game objects currently in the level. It's intended as the main point of contact between the game engine and the
    lower level game objects, and to prevent lower level game objects from needing to know about each other.

    To higher level entities (for handling inputs and rendering), LevelManager keeps track of
    what's going on and provides utility functions to effect the whole level, e.g. calling the
    Behaviours upon all enemies in the level.

    Lower level entities (e.g. enemies) shouldn't really reach 'up' into the LevelManager, they should be acted upon from
    'above'.

    Todo: provide save and load functionality!
    """

    def __init__(self, player: Player, level: Level):

        self.player = player
        self.level = level

    def trigger_all_behaviours(self):
        """
        Utility method which causes all behaviours to be run against all objects in the level which have behaviours.
        :return:
        """

        self.trigger_enemy_behaviour()
        self.trigger_bullet_behaviour()

        # Check if level is complete after processing behaviours
        if self.level.is_complete():
            raise LevelCompleteException("All enemies defeated")

    def trigger_enemy_behaviour(self):
        for enemy in self.level.enemies:
            EnemyBehaviour.act(enemy, self.level, self.player)

    def trigger_bullet_behaviour(self):
        for bullet in self.level.bullets:
            BulletBehaviour.act(bullet, self.level, self.player)


