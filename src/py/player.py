import math
import pygame

class Player:
    def __init__(self, game_map, game=None):
        self.game_map = game_map
        self.game = game
        self.x, self.y = game_map.player_start_pos
        self.angle = 0
        self.speed = 3.0
        self.sensitivity = 0.003
        self.is_moving = False
        self.bob_timer = 0.0
        self.bob_amount = 0.0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed_factor = self.speed * dt * 60
        self.is_moving = False

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx += cos_a * speed_factor
            dy += sin_a * speed_factor
            self.is_moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx -= cos_a * speed_factor
            dy -= sin_a * speed_factor
            self.is_moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx += sin_a * speed_factor
            dy -= cos_a * speed_factor
            self.is_moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx -= sin_a * speed_factor
            dy += cos_a * speed_factor
            self.is_moving = True

        if not self.check_wall(int((self.x + dx) // self.game_map.title_size), int(self.y // self.game_map.title_size)):
            self.x += dx
        if not self.check_wall(int(self.x // self.game_map.title_size), int((self.y + dy) // self.game_map.title_size)):
            self.y += dy

        if self.is_moving:
            self.bob_timer += 0.15 * speed_factor
            self.bob_amount = math.sin(self.bob_timer) * 8
        else:
            self.bob_timer = 0
            self.bob_amount = 0

        rel_x, _ = pygame.mouse.get_rel()
        if rel_x != 0:
            self.angle += rel_x * self.sensitivity
            self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) in self.game_map.world_map