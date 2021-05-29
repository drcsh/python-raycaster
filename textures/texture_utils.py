import pygame


def replace_colour_on_surface(surface: pygame.Surface, original_colour: pygame.Color, replacement_colour: pygame.Color):

    surface.lock()
    px_arr = pygame.PixelArray(surface)
    px_arr.replace(original_colour, replacement_colour)
    px_arr.close()
