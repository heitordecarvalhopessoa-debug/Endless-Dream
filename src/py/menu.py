import pygame

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.selected_option = 0
        self.options = ["Start Game", "Exit"]
        
        try:
            self.title_font = pygame.font.SysFont("Courier New", 48, bold=True)
            self.font = pygame.font.SysFont("Courier New", 24, bold=True)
        except:
            self.title_font = None
            self.font = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None

    def draw(self, screen):
        screen.fill((5, 5, 8))

        if self.title_font and self.font:
            title_surf = self.title_font.render("ENDLESS DREAM", True, (180, 20, 20))
            title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 3))
            screen.blit(title_surf, title_rect)

            start_y = self.height // 2 + 20
            for i, option in enumerate(self.options):
                color = (240, 240, 240) if i == self.selected_option else (70, 70, 70)
                prefix = "> " if i == self.selected_option else "  "
                
                opt_surf = self.font.render(f"{prefix}{option}", True, color)
                opt_rect = opt_surf.get_rect(center=(self.width // 2, start_y + i * 45))
                screen.blit(opt_surf, opt_rect)