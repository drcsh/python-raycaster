import pygame

from engine.utils.exceptions import GameExitException


class InputHandler:
    """
    Class for handling player_objects inputs
    """

    def __init__(self, gui_manager):

        self.gui_manager = gui_manager

        # TODO: load these from a settings file
        self.QUIT_K = pygame.K_ESCAPE
        self.FORWARD_K = pygame.K_w
        self.BACK_K = pygame.K_s
        self.LEFT_K = pygame.K_a
        self.RIGHT_K = pygame.K_d
        self.SHOOT_K = pygame.K_SPACE

    def handle(self, gamestate):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise GameExitException("Pygame Quit event")
            if event.type == pygame.KEYDOWN and event.key == self.QUIT_K:
                raise GameExitException("Player pressed Quit key")

            if event.type == pygame.KEYDOWN and event.key == self.SHOOT_K:
                gamestate.player.shoot(gamestate)
                continue
            if event.type == pygame.KEYDOWN and event.key == self.FORWARD_K:
                gamestate.player.move_forward()
                continue
            if event.type == pygame.KEYDOWN and event.key == self.BACK_K:
                gamestate.player.move_backward()
                continue
            if event.type == pygame.KEYDOWN and event.key == self.LEFT_K:
                gamestate.player.turn_left()
                continue
            if event.type == pygame.KEYDOWN and event.key == self.RIGHT_K:
                gamestate.player.turn_right()
                continue

            self.gui_manager.process_events(event)
