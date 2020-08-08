from engine.game_object import GameObject


class Enemy(GameObject):
    """
    Enemy is a subclass of GameObject, in addition to the basic information tracked by GameObject, it keeps track of
    variables needed for the enemy, such as its HP.
    """

    DEFAULT_MOVE_SPEED = 0.25

    def __init__(self, sprite_group, x, y, max_hp, texturemap_tile_num, speed=DEFAULT_MOVE_SPEED):
        self.max_hp = max_hp
        self.hp = max_hp
        self.texturemap_tile_num = texturemap_tile_num  # Temp, for animation, each enemy will need their own TextureMap
        self.speed = speed

        super(Enemy, self).__init__(sprite_group, x, y, texturemap_tile_num)
