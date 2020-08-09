import math

from engine.game_objects.game_object import GameObject


class Bullet(GameObject):

    DEFAULT_SIZE = 10
    DEFAULT_COLOR = (0, 255, 255)
    DEFAULT_DAMAGE = 10

    def __init__(self, sprite_group, x, y, angle, speed, texturemap_tile_num, size=DEFAULT_SIZE, damage=DEFAULT_DAMAGE):
        self.angle = angle
        self.speed = speed
        self.size = size
        self.damage = damage

        self.cos_angle = math.cos(angle)
        self.sin_angle = math.sin(angle)

        super(self).__init__(sprite_group, x, y, texturemap_tile_num)

    def move(self, gamestate):
        """

        :param GameState gamestate:
        :return:
        """
        new_x = self.x + self.speed * math.cos(self.angle)
        new_y = self.y + self.speed * math.sin(self.angle)

        if gamestate.level.wall_at_location(new_x, new_y):
            self.kill()
            return

        enemy = gamestate.level.enemy_near_location(new_x, new_y)
        if enemy:
            enemy.take_damage(self.damage)
            self.kill()
            return

        self.x = new_x
        self.y = new_y