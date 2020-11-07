from pygame.sprite import Sprite


class GameObject(Sprite):
    """
    For keeping track of game furniture
    """

    def __init__(self, sprite_group, x, y, texturemap):
        self.x = x
        self.y = y
        self.texturemap = texturemap
        super(GameObject, self).__init__(sprite_group)

    def get_display_tile(self):
        """
        Returns the tile from the texturemap for display.

        This is here so that in RayCaster we can treat static game furniture and animated objects the same way
        for rendering purposes.
        :return:
        :rtype TextureTile:
        """
        return self.texturemap.get_tile_at(0, 0)

    def check_location_valid(self, gamestate, new_x, new_y):
        """
        Helper method for all (moving) game objects to determine if their new location is valid.
        :param GameState gamestate:
        :param float new_x:
        :param float new_y:
        :return: True if there's nothing blocking this location, False otherwise
        :rtype bool:
        """

        if gamestate.level.wall_at_location(new_x, new_y):
            return False

        if gamestate.level.enemy_near_location(new_x, new_y, exclude_enemy=self):
            return False

        return True
