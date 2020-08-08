import pygame

from engine.game_objects.game_object import GameObject


class Enemy(GameObject):
    """
    Enemy is a subclass of GameObject, in addition to the basic information tracked by GameObject, it keeps track of
    variables needed for the enemy, such as its HP.
    """

    DEFAULT_MOVE_SPEED = 0.25

    def __init__(self,
                 sprite_group,
                 x,
                 y,
                 max_hp,
                 texturemap_tile_num,
                 speed=DEFAULT_MOVE_SPEED):
        self.max_hp = max_hp
        self.hp = max_hp
        self.texturemap_tile_num = texturemap_tile_num  # Temp, for animation, each enemy will need their own TextureMap
        self.speed = speed

        # This is used to throttle how many actions the enemy takes. E.g. we don't want an enemy to attack every single
        # game iteration, or it will attack as fast as the game runes.
        self.wait_until = 0

        super(Enemy, self).__init__(sprite_group, x, y, texturemap_tile_num)

    def act(self, gamestate):
        """
        This function defines the behavior of the enemy, it should be called once per game iteration.
        :return:
        """
        if pygame.time.get_ticks() < self.wait_until:
            return

        # Todo - need to do various things based on the gamestate
        pass

    def has_los_to_player(self, gamestate):
        """
        This function determines if the enemy can see the player from where it is (i.e. if there is an uninterrupted
        line from the player to the enemy).

        :param gamestate:
        :return:
        """
        # TODO: will need to work this out similar to how the raycast works, by jumping along points of interest
        pass

    def move(self):
        # TODO: if the enemy can see the player, it will move towards them. Maybe have more advanced movement?
        pass

    def attack(self):
        # TODO: If the enemy can see the player and the enemy is in range, make an attack
        pass
