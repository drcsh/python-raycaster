import math

class Player:
    TURNSPEED = 10 * math.pi / 360
    MOVESPEED = 0.2

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
        self._check_angle()

    def turn_right(self):
        self.angle += self.TURNSPEED
        self._check_angle()

    def _check_angle(self):
        """
        when we turn we're modifying the player angle by a fraction of pi. If this angle goes > 2pi or < 0 we need to
        reset it to prevent other calculations getting thrown out.
        :return:
        """
        if self.angle > math.tau:
            self.angle -= math.tau
        elif self.angle < 0:
            self.angle += math.tau
