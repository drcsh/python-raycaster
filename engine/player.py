import math

class Player:
    TURNSPEED = 10 * math.pi / 360
    MOVESPEED = 0.5

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def move(self, speed):
        self.x = self.x + speed * math.cos(self.angle)
        self.y = self.y + speed * math.sin(self.angle)

    def move_forward(self):
        self.move(self.MOVESPEED)

    def move_backward(self):
        self.move(-self.MOVESPEED)

    def turn_left(self):
        self.angle -= self.TURNSPEED

    def turn_right(self):
        self.angle += self.TURNSPEED
