import pygame

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.selected_option = 0
        self.options = ["Start Game", "Exit"]
        
        try:
            self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
            self.font = pygame.font.SysFont("Arial", 28, bold=True)
            self.small_font = pygame.font.SysFont("Arial", 18)
        except:
            self.title_font = None
            self.font = None
            self.small_font = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_W:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_S:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None

    def draw(self, screen):
        screen.fill((15, 15, 20))

        if self.title_font and self.font:
            title_surf = self.title_font.render("ENDLESS DREAM", True, (240, 240, 255))
            title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 3 - 30))
            screen.blit(title_surf, title_rect)

            start_y = self.height // 2 + 10
            for i, option in enumerate(self.options):
                color = (255, 255, 100) if i == self.selected_option else (180, 180, 180)
                prefix = "> " if i == self.selected_option else "  "
                
                opt_surf = self.font.render(f"{prefix}{option}", True, color)
                opt_rect = opt_surf.get_rect(center=(self.width // 2, start_y + i * 45))
                screen.blit(opt_surf, opt_rect)

            if self.small_font:
                footer_surf = self.small_font.render("Dream", True, (120, 120, 140))
                footer_rect = footer_surf.get_rect(center=(self.width // 2, self.height - 40))
                screen.blit(footer_surf, footer_rect)