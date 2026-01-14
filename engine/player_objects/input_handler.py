import pygame
import pygame_gui

from engine.behaviours.bullet_behaviour import BulletBehaviour
from engine.game_objects.bullet import Bullet
from engine.levelmanager import LevelManager
from engine.utils import math_utils
from engine.utils.exceptions import GameExitException
from textures.texturemap import TextureMap


class InputHandler:
    """
    Class for handling player_objects inputs
    """

    def __init__(self, level_state: LevelManager, gui_manager: pygame_gui.UIManager):

        self.level_state = level_state
        self.gui_manager = gui_manager

        # TODO: load these from a settings file
        self.QUIT_K = pygame.K_ESCAPE
        self.FORWARD_K = pygame.K_w
        self.BACK_K = pygame.K_s
        self.LEFT_K = pygame.K_a
        self.RIGHT_K = pygame.K_d
        self.SHOOT_K = pygame.K_SPACE

    def handle(self):

        # TODO: different behaviours based on menu active or game active etc.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise GameExitException("Pygame Quit event")
            if event.type == pygame.KEYDOWN and event.key == self.QUIT_K:
                raise GameExitException("Player pressed Quit key")

            if event.type == pygame.KEYDOWN and event.key == self.SHOOT_K:
                self.player_attack()
                continue
            if event.type == pygame.KEYDOWN and event.key == self.FORWARD_K:
                self.player_moves_forward()
                continue
            if event.type == pygame.KEYDOWN and event.key == self.BACK_K:
                self.player_moves_backwards()
                continue
            if event.type == pygame.KEYDOWN and event.key == self.LEFT_K:
                self.level_state.player.turn_left()
                continue
            if event.type == pygame.KEYDOWN and event.key == self.RIGHT_K:
                self.level_state.player.turn_right()
                continue

            self.gui_manager.process_events(event)

    def player_attack(self):
        """
        This action has to go here rather than on the player object, because it creates bullet
        objects which need to be kept track of by the level_state.
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
        # Note: Bullet is added to the sprite group so doesn't need explicitly added to the LevelManager
        bullet = Bullet(
            sprite_group=self.level_state.level.bullets,
            x=self.level_state.player.x,
            y=self.level_state.player.y,
            angle=self.level_state.player.angle,
            speed=b_speed,
            texturemap=b_texturemap,
            damage=b_damage
        )

        # trigger bullet move immediately to get it infront of the player and check for impact
        BulletBehaviour.act(bullet, self.level_state.level, self.level_state.player)

    def player_moves_forward(self):
        self._player_moves(self.level_state.player.MOVESPEED)

    def player_moves_backwards(self):
        self._player_moves(-self.level_state.player.MOVESPEED)

    def _player_moves(self, speed: float):
        """
        Given the player speed, works out their new location and if that location
        is valid, updates the player object
        :param float speed:
        :return:
        """

        new_x, new_y = math_utils.get_new_coordinates(
            self.level_state.player.x,
            self.level_state.player.y,
            self.level_state.player.angle,
            speed
        )

        if self.level_state.level.location_is_valid(new_x, new_y):
            self.level_state.player.move(new_x, new_y)

    def player_turns_left(self):
        self.level_state.player.turn_left()

    def player_turns_right(self):
        self.level_state.player.turn_right()