
class Enemy:

    DEFAULT_MOVE_SPEED = 0.25

    def __init__(self, loc_x, loc_y, sprite, max_hp, speed=DEFAULT_MOVE_SPEED):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.sprite = sprite
        self.max_hp = max_hp
        self.hp = max_hp
        self.speed = speed

