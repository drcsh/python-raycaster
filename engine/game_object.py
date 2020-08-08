from pygame.sprite import Sprite


class GameObject(Sprite):
    """
    For keeping track of game furniture
    """

    def __init__(self, sprite_group, x, y, texturemap_tile_num):
        self.x = x
        self.y = y
        self.texturemap_tile_num = texturemap_tile_num
        super(GameObject, self).__init__(sprite_group)
