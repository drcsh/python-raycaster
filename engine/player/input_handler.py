import pygame

from engine.utils.exceptions import GameExitException


class InputHandler:
    """
    Class for handling player inputs
    """

    def __init__(self):

        # TODO: load these from a settings file
        self.QUIT_K = pygame.K_ESCAPE
        self.FORWARD_K = pygame.K_w
        self.BACK_K = pygame.K_s
        self.LEFT_K = pygame.K_a
        self.RIGHT_K = pygame.K_d

    def handle(self, player):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise GameExitException("Pygame Quit event")
            if event.type == pygame.KEYDOWN and event.key == self.QUIT_K:
                raise GameExitException("Player pressed Quit key")

            if event.type == pygame.KEYDOWN and event.key == self.FORWARD_K:
                player.move_forward()
            if event.type == pygame.KEYDOWN and event.key == self.BACK_K:
                player.move_backward()
            if event.type == pygame.KEYDOWN and event.key == self.LEFT_K:
                player.turn_left()
            if event.type == pygame.KEYDOWN and event.key == self.RIGHT_K:
                player.turn_right()
