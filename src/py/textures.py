import os
import pygame

class Textures:
    def __init__(self):
        base_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        texture_path = os.path.join(base_path, "assets", "textures", "wall.png")
        file_texture_path = os.path.join(base_path, "assets", "textures", "file.png")

        if os.path.exists(texture_path):
            self.wall = pygame.image.load(texture_path).convert()
        else:
            self.wall = pygame.Surface((64, 64))
            self.wall.fill((120, 120, 120))
            for y in range(0, 64, 8):
                pygame.draw.line(self.wall, (80, 80, 80), (0, y), (64, y), 2)
        self.wall = pygame.transform.scale(self.wall, (64, 64))

        if os.path.exists(file_texture_path):
            self.file_img = pygame.image.load(file_texture_path).convert_alpha()
        else:
            self.file_img = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.rect(self.file_img, (0, 140, 255), (0, 0, 64, 64), border_radius=8)
            pygame.draw.rect(self.file_img, (255, 255, 255), (0, 0, 64, 64), 4, border_radius=8)
        self.file_img = pygame.transform.scale(self.file_img, (64, 64))