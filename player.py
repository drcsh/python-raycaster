import math

class Player:
    TURNSPEED = 10 * math.pi / 360
    MOVESPEED = 0.5

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def move_forward(self):
        self.x = self.x + self.MOVESPEED * math.cos(self.angle)
        self.y = self.y + self.MOVESPEED * math.sin(self.angle)

    def turn_left(self):
        self.angle -= self.TURNSPEED

    def turn_right(self):
        self.angle += self.TURNSPEED
