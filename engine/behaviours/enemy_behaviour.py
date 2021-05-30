import pygame

from engine.level_objects.level import Level
from engine.player_objects.player import Player
from engine.game_objects.enemy import Enemy


class EnemyBehaviour:
    
    @classmethod
    def act(cls, enemy: Enemy, level: Level, player: Player):
        if pygame.time.get_ticks() < enemy.wait_until:
            return

        if level.line_of_sight_between_coords(enemy.x, enemy.y, player.x, player.y):

            if enemy.dead:  # todo: remove dead enemies when out of LOS
                enemy.die()
            elif enemy.can_attack(player):
                enemy.attack(player)
            else:
                next_x, next_y = enemy.get_next_move_location(player)
                if level.location_is_valid(next_x, next_y, exclude_enemy=enemy):
                    enemy.move(next_x, next_y)

            enemy.animate()
            enemy.wait_until = pygame.time.get_ticks() + enemy.ANIMATION_WAIT_TICKS

