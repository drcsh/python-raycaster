from engine.behaviours.bullet_behaviour import BulletBehaviour
from engine.behaviours.enemy_behaviour import EnemyBehaviour
from engine.game_objects.bullet import Bullet
from engine.level_objects.level import Level
from engine.player_objects.player import Player
from textures.texturemap import TextureMap


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

    def player_attack(self):
        """
        This action has to go here rather than on the player object, because it creates bullet
        objects which need to be kept track of by the gamestate.
        :return:
        """

        # TODO: Get equipped weapon
        # TODO: check weapon equipped has ammo
        # TODO: trigger weapon firing animation
        # TODO: Get bullet characteristics for weapon
        b_speed = 0.2
        b_texturemap = TextureMap.load_common('simple_bullet.png')
        b_damage = 25

        # create bullet object with self.angle and weapon speed
        bullet = Bullet(
            sprite_group=self.level.bullets,
            x=self.player.x,
            y=self.player.y,
            angle=self.player.angle,
            speed=b_speed,
            texturemap=b_texturemap,
            damage=b_damage
        )

        # trigger bullet move immediately to get it infront of the player and check for impact
        BulletBehaviour.act(bullet, self.level, self.player)

    def player_moves_forward(self):
        new_x, new_y = self.player.get_next_forward_position()

        if self.level.location_is_valid(new_x, new_y):
            self.player.move(new_x, new_y)

    def player_moves_backwards(self):
        new_x, new_y = self.player.get_next_backward_position()

        if self.level.location_is_valid(new_x, new_y):
            self.player.move(new_x, new_y)

    def player_turns_left(self):
        self.player.turn_left()

    def player_turns_right(self):
        self.player.turn_right()
