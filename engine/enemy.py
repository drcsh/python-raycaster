from pygame.sprite import Sprite


class Enemy(Sprite):

    DEFAULT_MOVE_SPEED = 0.25

    def __init__(self, sprite_group, loc_x, loc_y, max_hp, texturemap_tile_num, speed=DEFAULT_MOVE_SPEED):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.max_hp = max_hp
        self.hp = max_hp
        self.texturemap_tile_num = texturemap_tile_num  # Temp, for animation, each enemy will need their own TextureMap
        self.speed = speed

        super(Enemy, self).__init__(sprite_group)
