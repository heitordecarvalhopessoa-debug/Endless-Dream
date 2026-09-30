import pygame
from src.py.player import Player
from src.py.map import Map
from src.py.raycasting import Raycasting
from src.py.textures import Textures
from src.py.ui import UI
from src.py.sounds import Sounds
from src.py.menu import Menu

WIDTH = 960
HEIGHT = 540
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Endless Dream")
        self.clock = pygame.time.Clock()
        
        self.state = "MENU"
        self.menu = Menu(WIDTH, HEIGHT)
        
        self.current_level = 0
        self.total_files = 0
        self.collected_files = 0
        
        self.sounds = Sounds()
        self.game_map = None
        self.textures = Textures()
        self.player = None
        self.raycasting = None
        self.ui = UI(WIDTH, HEIGHT, self)

        self.running = True

    def start_game(self):
        self.current_level = 0
        self.collected_files = 0
        self.game_map = Map(self)
        self.player = Player(self.game_map, self)
        self.raycasting = Raycasting(WIDTH, HEIGHT, self.game_map, self.textures)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.state = "PLAYING"

    def next_level(self):
        self.current_level += 1
        self.collected_files = 0
        self.game_map = Map(self)
        self.player = Player(self.game_map, self)
        self.raycasting = Raycasting(WIDTH, HEIGHT, self.game_map, self.textures)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            if self.state == "MENU":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                    
                    action = self.menu.handle_event(event)
                    if action == "Start Game":
                        self.start_game()
                    elif action == "Exit":
                        self.running = False

                self.menu.draw(self.screen)
                pygame.display.flip()

            elif self.state == "PLAYING":
                level_completed = (self.total_files > 0 and self.collected_files >= self.total_files)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.mouse.set_visible(True)
                            pygame.event.set_grab(False)
                            self.state = "MENU"
                        if level_completed and event.key == pygame.K_RETURN:
                            self.next_level()
                    self.ui.handle_event(event)

                if not level_completed:
                    self.player.update(dt)

                self.raycasting.render(self.screen, self.player)
                self.ui.draw(self.screen, self.clock)
                pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
