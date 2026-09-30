import pygame

class UI:
    def __init__(self, width, height, game=None):
        self.width = width
        self.height = height
        self.game = game
        self.max_health = 100
        self.current_health = 100
        self.show_fps = False
        self.total_seconds = 9 * 60 + 20
        self.last_tick = pygame.time.get_ticks()

        try:
            self.font = pygame.font.SysFont("Courier New", 16, bold=True)
            self.fps_font = pygame.font.SysFont("Arial", 14, bold=True)
            self.continue_font = pygame.font.SysFont("Courier New", 32, bold=True)
            self.clock_font = pygame.font.SysFont("Courier New", 20, bold=True)
        except:
            self.font = None
            self.fps_font = None
            self.continue_font = None
            self.clock_font = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self.show_fps = not self.show_fps

    def draw(self, screen, clock=None):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_tick >= 1000:
            self.total_seconds += 1
            self.last_tick = current_time

        level_completed = (self.game and self.game.total_files > 0 and self.game.collected_files >= self.game.total_files)

        if not level_completed:
            bar_x, bar_y, bar_width, bar_height = 20, 20, 120, 6
            health_pct = max(0, min(self.current_health, self.max_health)) / self.max_health
            
            pygame.draw.rect(screen, (20, 20, 20), (bar_x, bar_y, bar_width, bar_height))
            if health_pct > 0:
                pygame.draw.rect(screen, (160, 20, 20), (bar_x, bar_y, int(bar_width * health_pct), bar_height))

            if self.font:
                if self.game and hasattr(self.game, 'total_files'):
                    collected = getattr(self.game, 'collected_files', 0)
                    total = self.game.total_files
                    files_text = self.font.render(f"Files: {collected}/{total}", True, (150, 150, 150))
                    screen.blit(files_text, (bar_x, bar_y + 12))

            if self.clock_font:
                minutes = self.total_seconds // 60
                seconds = self.total_seconds % 60
                time_text = f"{minutes:02d}:{seconds:02d}"
                time_surface = self.clock_font.render(time_text, True, (200, 200, 200))
                time_rect = time_surface.get_rect(topright=(self.width - 20, 20))
                screen.blit(time_surface, time_rect)

        if level_completed:
            if self.continue_font:
                overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 220))
                screen.blit(overlay, (0, 0))

                text_surface = self.continue_font.render("STAGE CLEARED", True, (200, 200, 200))
                sub_surface = self.font.render("Press ENTER to continue", True, (100, 100, 100))
                
                screen.blit(text_surface, text_surface.get_rect(center=(self.width // 2, self.height // 2 - 20)))
                screen.blit(sub_surface, sub_surface.get_rect(center=(self.width // 2, self.height // 2 + 25)))

        if self.show_fps and clock and self.fps_font:
            fps_val = int(clock.get_fps())
            fps_surface = self.fps_font.render(f"FPS: {fps_val}", True, (100, 255, 100))
            screen.blit(fps_surface, (self.width - 80, 50))