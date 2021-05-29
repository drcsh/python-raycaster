from .game_object import GameObject


class AnimatedObject(GameObject):
    """
    Subclass of GameObject specifically for objects which have animations (e.g. enemies)
    """

    MOVE_ANIMATION = 0
    ATTACK_ANIMATION = 1
    DEATH_ANIMATION = 2

    def __init__(self, sprite_group, x, y, texturemap):
        """
        This is just a wrapper for the parent class' init. The params here are passed straight through.
        :param SpriteGroup sprite_group:
        :param int x:
        :param int y:
        :param TextureMap texturemap:
        """

        # animation state is basically which horizontal texture tile to display
        self.animation_state = 0
        self.animation_state_max = texturemap.horizontal_tiles_total - 1  # -1 due to 0 index.

        # animation type is which row of tiles from the texturemap to use
        self.animation_type = self.MOVE_ANIMATION  # default animation state is moving

        # When we change animation type, we will want to reset to the first tile, rather than continuing
        self.previous_animation_type = 0

        super(AnimatedObject, self).__init__(sprite_group, x, y, texturemap)

    def get_display_tile(self):
        """
        Overwrites the parent class function so that we pick the tile at the right frame of the animation
        :return:
        :rtype TextureTile:
        """
        return self.texturemap.get_tile_at(self.animation_state, self.animation_type)

    def reset_animation_state(self):
        self.animation_state = 0

    def set_animation_type(self, animation_type):
        """
        Because we want to reset to the resting animation tile between animation states, we need to keep track of the
        previous animation type, and reset to tile 0 when the animation type changes.

        :param int animation_type:
        :return:
        """  
        self.previous_animation_type = self.animation_type
        self.animation_type = animation_type

    def animate(self):
        """
        Updates the animation state to the next one in the sequence (rolling back to the start if appropriate).
        :return:
        """
        if self.animation_type != self.previous_animation_type:
            self.reset_animation_state()
        elif self.animation_state >= self.animation_state_max:
            self.reset_animation_state()
        else:
            self.animation_state += 1
