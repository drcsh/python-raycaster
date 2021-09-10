import pygame
import pygame_gui

from engine.behaviours.bullet_behaviour import BulletBehaviour
from engine.game_objects.bullet import Bullet
from engine.gamestate import GameState
from engine.utils.exceptions import GameExitException
from textures.texturemap import TextureMap


class InputHandler:
    """
    Class for handling player_objects inputs
    """

    def __init__(self, gamestate: GameState, gui_manager: pygame_gui.UIManager):

        self.gamestate = gamestate
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
                self.gamestate.player.turn_left()
                continue
            if event.type == pygame.KEYDOWN and event.key == self.RIGHT_K:
                self.gamestate.player.turn_right()
                continue

            self.gui_manager.process_events(event)

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
        BulletBehaviour.act(bullet, self.gamestate.level, self.gamestate.player)

    def player_moves_forward(self):
        new_x, new_y = self.gamestate.player.get_next_forward_position()

        if self.gamestate.level.location_is_valid(new_x, new_y):
            self.gamestate.player.move(new_x, new_y)

    def player_moves_backwards(self):
        new_x, new_y = self.gamestate.player.get_next_backward_position()

        if self.gamestate.level.location_is_valid(new_x, new_y):
            self.gamestate.player.move(new_x, new_y)
