import math
import pygame

class Raycasting:
    def __init__(self, width, height, game_map, textures):
        self.width = width
        self.height = height
        self.game_map = game_map
        self.textures = textures
        self.fov = math.pi / 3
        self.half_fov = self.fov / 2
        self.num_rays = width   
        self.delta_angle = self.fov / self.num_rays
        self.max_depth = 8 * game_map.title_size
        self.scale = width // self.num_rays

    def render(self, screen, player):
        half_height = (self.height // 2) + int(player.bob_amount)
        screen.fill((3, 3, 5), (0, 0, self.width, half_height))
        screen.fill((8, 8, 10), (0, half_height, self.width, self.height - half_height))
        
        left_ray = player.angle - self.half_fov
        depth_buffer = [0 for _ in range(self.num_rays)]

        for ray in range(self.num_rays):
            ray_angle = left_ray + ray * self.delta_angle
            cos_angle = math.cos(ray_angle)
            sin_angle = math.sin(ray_angle)

            depth = 0
            while depth < self.max_depth:
                target_x = player.x + depth * cos_angle
                target_y = player.y + depth * sin_angle

                cell_x = int(target_x // self.game_map.title_size)
                cell_y = int(target_y // self.game_map.title_size)
                if (cell_x, cell_y) in self.game_map.world_map:
                    break
                depth += 2

            correct_depth = depth * math.cos(player.angle - ray_angle)
            if correct_depth < 1:
                correct_depth = 1

            depth_buffer[ray] = correct_depth
            projected_height = min(int((self.game_map.title_size / correct_depth) * (self.width / 2)), self.height * 2)
            wall_slice_top = half_height - (projected_height // 2)
            hit_x = player.x + depth * cos_angle
            hit_y = player.y + depth * sin_angle
            tex_x = int(hit_x + hit_y) % 64
            wall_slice = self.textures.wall.subsurface(tex_x, 0, 1, 64)
            wall_slice = pygame.transform.scale(wall_slice, (self.scale, projected_height))
            
            fog_factor = max(0.0, min(1.0, correct_depth / self.max_depth))
            shade_factor = max(0.01, 1.0 - (fog_factor ** 1.5))
            
            dark_surface = pygame.Surface(wall_slice.get_size(), pygame.SRCALPHA)
            dark_surface.fill((int(255 * shade_factor), int(255 * shade_factor), int(255 * shade_factor)))
            wall_slice.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(wall_slice, (ray * self.scale, wall_slice_top))

        for pos in self.game_map.files_map:
            file_x = (pos[0] + 0.5) * self.game_map.title_size
            file_y = (pos[1] + 0.5) * self.game_map.title_size
            dx = file_x - player.x
            dy = file_y - player.y
            angle_to_file = math.atan2(dy, dx) - player.angle
            
            while angle_to_file > math.pi: angle_to_file -= math.tau
            while angle_to_file < -math.pi: angle_to_file += math.tau

            if -self.half_fov < angle_to_file < self.half_fov:
                dist = math.hypot(dx, dy) * math.cos(angle_to_file)
                if dist < 1: dist = 1

                if dist < self.max_depth:
                    screen_x = int((self.width / 2) + (angle_to_file / self.half_fov) * (self.width / 2))
                    proj_size = min(int((self.game_map.title_size / dist) * (self.width / 2) * 0.7), self.height)
                    
                    ray_index = int(screen_x / self.scale)
                    if 0 <= ray_index < self.num_rays and dist < depth_buffer[ray_index]:
                        scaled_file = pygame.transform.scale(self.textures.file_img, (proj_size, proj_size))
                        fog_factor = max(0.0, min(1.0, dist / self.max_depth))
                        shade_factor = max(0.02, 1.0 - (fog_factor ** 1.5))
                        
                        dark_file = pygame.Surface(scaled_file.get_size(), pygame.SRCALPHA)
                        dark_file.fill((int(255 * shade_factor), int(255 * shade_factor), int(255 * shade_factor)))
                        scaled_file.blit(dark_file, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        screen.blit(scaled_file, (screen_x - proj_size // 2, half_height - (proj_size // 2)))