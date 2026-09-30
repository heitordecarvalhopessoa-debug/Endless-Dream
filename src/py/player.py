import math
import pygame

class Player:
    def __init__(self, game_map, game=None):
        self.game_map = game_map
        self.game = game
        self.x, self.y = game_map.player_start_pos
        self.angle = 0
        self.speed = 3.5
        self.sensitivity = 0.003
        self.is_moving = False
        self.bob_timer = 0.0
        self.bob_amount = 0.0
        self.smooth_bob = 0.0

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

        if not self.game_map.is_wall(self.x + dx + math.copysign(20, dx), self.y):
            self.x += dx
        if not self.game_map.is_wall(self.x, self.y + dy + math.copysign(20, dy)):
            self.y += dy

        self.game_map.check_file_collection(self.x, self.y)

        target_bob = 0.0
        if self.is_moving:
            self.bob_timer += 0.15 * speed_factor
            target_bob = math.sin(self.bob_timer) * 6
        else:
            self.bob_timer = 0
            target_bob = 0.0
        
        self.smooth_bob += (target_bob - self.smooth_bob) * 0.2
        self.bob_amount = self.smooth_bob

        rel_x, _ = pygame.mouse.get_rel()
        if rel_x != 0:
            self.angle += rel_x * self.sensitivity
            self.angle %= math.tau