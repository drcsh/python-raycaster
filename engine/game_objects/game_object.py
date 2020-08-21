from pygame.sprite import Sprite


class GameObject(Sprite):
    """
    For keeping track of game furniture
    """

    MOVE_ANIMATION = 0
    ATTACK_ANIMATION = 1
    DEATH_ANIMATION = 2

    def __init__(self, sprite_group, x, y, texturemap):
        self.x = x
        self.y = y
        self.texturemap = texturemap
        self.animation_state = 0
        self.animation_type = self.MOVE_ANIMATION
        super(GameObject, self).__init__(sprite_group)

    @staticmethod
    def check_location_valid(gamestate, new_x, new_y):
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

        if gamestate.level.enemy_near_location(new_x, new_y):
            return False

        return True
