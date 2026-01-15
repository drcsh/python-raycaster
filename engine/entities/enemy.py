import math
from typing import Tuple

import pygame

from engine.textures.texturemap import TextureMap
from .animated_object import AnimatedObject
from engine.utils import math_utils
from .player import Player


class Enemy(AnimatedObject):
    """
    Enemy is a subclass of AnimatedObject,  keeps track of variables needed for the enemies, such as HP.
    """

    DEFAULT_MOVE_SPEED = 0.25
    DEFAULT_ATTACK_RANGE = 1
    DEFAULT_ATTACK_DAMAGE = 20
    DAMAGE_DEALT_ON_STATE = 3

    def __init__(self,
                 sprite_group: pygame.sprite.Group,
                 x: float,
                 y: float,
                 max_hp: int,
                 texturemap: TextureMap,
                 speed: int = DEFAULT_MOVE_SPEED,
                 attack_range: float = DEFAULT_ATTACK_RANGE,
                 attack_damage: int = DEFAULT_ATTACK_DAMAGE):
        """
        :param sprite_group: Which spritegroup this will belong to
        :param x: X coord on the Map where this enemy appears.
        :param y: Y coord on the Map where this enemy appears.
        :param texturemap:
        :param max_hp:
        :param speed:
        :param attack_range:
        :param attack_damage:
        """

        self.max_hp = max_hp
        self.hp = max_hp
        self.speed = speed
        self.attack_range = attack_range
        self.attack_damage = attack_damage

        # This is used to throttle how many actions the enemy takes. E.g. we don't want an enemy to attack every single
        # game iteration, or it will attack as fast as the game runes.
        self.wait_until = 0

        super().__init__(sprite_group, x, y, texturemap)

    @property
    def dead(self) -> bool:
        return self.hp <= 0

    def can_attack(self, player: Player):
        """
        Determines if the enemy is close enough to the player to attack
        """
        if math_utils.distance_formula(self.x, self.y, player.x, player.y) < self.attack_range:
            return True

        return False

    def get_next_move_location(self, player: Player) -> Tuple[float, float]:
        """
        Works out where to move to next, this location needs to be validity tested before
        movement can happen
        :return:
        """
        angle_to_player = math.atan2(player.y - self.y, player.x - self.x)

        return math_utils.get_new_coordinates(self.x, self.y, angle_to_player, self.speed)

    def move(self, new_x: float, new_y: float):
        """
        Set the appropriate animation and move to the given location
        """
        self.set_animation_type(self.MOVE_ANIMATION)

        self.x = new_x
        self.y = new_y

    def attack(self, player: Player):
        """
        Perform attack animation and do damage to the player.
        """
        self.set_animation_type(self.ATTACK_ANIMATION)

        # Don't deal the damage until the final frame of the attack animation
        if self.animation_state == self.DAMAGE_DEALT_ON_STATE:
            player.take_damage(self.attack_damage)

    def die(self):
        """
        Perform the death animation and then remove the sprite.
        """
        self.set_animation_type(self.DEATH_ANIMATION)

        if self.animation_state == self.animation_state_max:
            self.kill()

    def take_damage(self, damage: int):
        """
        Reduce current HP by the damage taken until dead.
        """
        if not self.dead:
            self.hp -= damage
