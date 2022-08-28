import math
from typing import List, Dict

from engine.player_objects.weapons.player_weapon import PlayerWeapon
from engine.utils import math_utils
from engine.utils.exceptions import PlayerDeadException


class Player:
    TURNSPEED = 10 * math.pi / 360
    MOVESPEED = 0.2
    MAX_HP = 100

    def __init__(self, x: float, y: float, angle: float, weapons: Dict):
        self.x = x
        self.y = y
        self.angle = angle
        self.hp = self.MAX_HP
        self.weapons = weapons
        self._weapon_equipped = list(self.weapons.keys())[0]

    def move(self, new_x: float, new_y: float):
        """
        Moves the player to a new position
        """
        self.x = new_x
        self.y = new_y

    def turn_left(self):
        self.angle -= self.TURNSPEED
        self._check_angle()

    def turn_right(self):
        self.angle += self.TURNSPEED
        self._check_angle()

    def get_equipped_weapon(self) -> PlayerWeapon:
        try:
            return self.weapons[self._weapon_equipped]
        except KeyError:
            self._weapon_equipped = list(self.weapons.keys())[0]
            return self.weapons[self._weapon_equipped]


    def take_damage(self, damage: int):
        """
        Apply damage to the player. Raises PlayerDeadException if the damage takes the player at or below 0 HP.
        :param int damage:
        :raises PlayerDeadException:
        :return:
        """
        self.hp -= damage

        if self.hp <= 0:
            raise PlayerDeadException("Player HP Reached 0")

    def coords_in_hitbox(self, x, y):
        return math_utils.distance_formula(x, y, self.x, self.y) < 0.5

    def _check_angle(self):
        """
        When we turn we're modifying the player_objects angle in radians. If we go > 2pi or < 0 radians we need to
        reset it to prevent other calculations getting thrown out.
        """
        if self.angle > math.tau:
            self.angle -= math.tau
        elif self.angle < 0:
            self.angle += math.tau
