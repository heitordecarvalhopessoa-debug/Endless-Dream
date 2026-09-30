import os
import pygame

class UI:
    def __init__(self, width, height, game=None):
        self.width = width
        self.height = height
        self.game = game
        self.max_health = 100
        self.current_health = 100
        self.show_fps = False
        self.elapsed_seconds = 0.0
        self.last_level = 0

        try:
            self.font = pygame.font.SysFont("Arial", 20, bold=True)
            self.fps_font = pygame.font.SysFont("Arial", 16, bold=True)
            self.continue_font = pygame.font.SysFont("Arial", 36, bold=True)
            self.clock_font = pygame.font.SysFont("Courier New", 22, bold=True)
        except:
            self.font = None
            self.fps_font = None
            self.continue_font = None
            self.clock_font = None

        base_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
        clock_path = os.path.join(base_path, "assets", "textures", "clock.png")
        if os.path.exists(clock_path):
            self.clock_bg = pygame.image.load(clock_path).convert_alpha()
            self.clock_bg = pygame.transform.scale(self.clock_bg, (140, 50))
        else:
            self.clock_bg = pygame.Surface((140, 50))
            self.clock_bg.fill((20, 20, 20))
            pygame.draw.rect(self.clock_bg, (100, 100, 100), (0, 0, 140, 50), 2, border_radius=4)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self.show_fps = not self.show_fps

    def draw(self, screen, clock=None):
        if self.game and hasattr(self.game, 'current_level'):
            if self.game.current_level != self.last_level:
                self.elapsed_seconds = 0.0
                self.last_level = self.game.current_level

        if clock:
            self.elapsed_seconds += clock.get_time() / 1000.0

        level_completed = (self.game and self.game.total_files > 0 and self.game.collected_files >= self.game.total_files)

        if not level_completed:
            bar_x = 30
            bar_y = 30
            bar_width = 200
            bar_height = 14

            bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            pygame.draw.rect(screen, (50, 50, 50), bg_rect, border_radius=3)
            
            health_percentage = max(0, min(self.current_health, self.max_health)) / self.max_health
            current_bar_width = int(bar_width * health_percentage)

            if current_bar_width > 0:
                health_rect = pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)
                pygame.draw.rect(screen, (220, 50, 50), health_rect, border_radius=3)

            pygame.draw.rect(screen, (100, 100, 100), bg_rect, 1, border_radius=3)

            if self.font:
                if self.game and hasattr(self.game, 'total_files'):
                    collected = getattr(self.game, 'collected_files', 0)
                    total = self.game.total_files
                    files_text = self.font.render(f"Files: {collected} / {total}", True, (240, 240, 240))
                    screen.blit(files_text, (bar_x, bar_y + bar_height + 8))

            clock_box_width = 140
            clock_box_height = 50
            clock_box_x = self.width - clock_box_width - 30
            clock_box_y = 30

            screen.blit(self.clock_bg, (clock_box_x, clock_box_y))

            total_secs = int(9 * 60 + self.elapsed_seconds)
            minutes = total_secs // 60
            seconds = total_secs % 60
            time_str = f"{minutes:02d}:{seconds:02d}"

            if self.clock_font:
                time_surface = self.clock_font.render(time_str, True, (255, 40, 40))
                t_rect = time_surface.get_rect(center=(clock_box_x + clock_box_width // 2, clock_box_y + clock_box_height // 2))
                screen.blit(time_surface, t_rect)

        if level_completed:
            if self.continue_font:
                overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                screen.blit(overlay, (0, 0))

                text_surface = self.continue_font.render("CONTINUE", True, (255, 255, 0))
                sub_surface = self.font.render("Press ENTER for the next map", True, (255, 255, 255))
                t_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 20))
                s_rect = sub_surface.get_rect(center=(self.width // 2, self.height // 2 + 25))
                
                screen.blit(text_surface, t_rect)
                screen.blit(sub_surface, s_rect)

        if self.show_fps and clock and self.fps_font:
            fps_val = int(clock.get_fps())
            fps_surface = self.fps_font.render(f"FPS: {fps_val}", True, (100, 255, 100))
            screen.blit(fps_surface, (self.width - 90, 90))