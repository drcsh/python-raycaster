from images.level_image_generator import LevelImageGenerator
import pygame


def main():
    win_w = 512
    win_h = 512

    surface = LevelImageGenerator.generate(win_w, win_h)
    pygame.image.save(surface, "out.bmp")


if __name__ == "__main__":
    main()
