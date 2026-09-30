import pygame as pg

_ = False

MAP_DATA = [
    [ # Level 0
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, _, _, _, 3, _, _, _, 1],
        [1, 1, 4, _, _, 1, 1, _, 1, 1, 1, 1, 1, _, 1],
        [1, 1, _, _, _, 1, 1, _, _, _, _, _, 1, _, 1],
        [1, 1, 1, 1, _, 1, 1, 1, 1, _, 1, _, 1, _, 1],
        [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, 1],
        [1, _, 1, 1, 1, 1, 1, _, 1, 1, 1, 1, 1, 1, 1],
        [1, 3, 1, _, _, _, 1, _, _, _, _, _, _, 3, 1],
        [1, _, 1, _, 3, _, 1, 1, 1, 1, 1, 1, 1, _, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [ # Level 1
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 3, _, _, _, 1, 3, _, _, _, _, _, 3, 1],
        [1, 1, 4, _, 1, _, 1, 1, _, 1, _, 1, 1, 1, 1, 1, _, 1],
        [1, 1, _, _, _, _, _, 1, _, 1, _, _, _, _, _, 1, _, 1],
        [1, 1, 1, 1, 1, 1, _, 1, _, 1, 1, 1, 1, 1, _, 1, _, 1],
        [1, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, 1, _, 1],
        [1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, 1, 1, _, 1],
        [1, 3, _, _, _, _, _, _, _, _, _, _, _, 1, 3, _, _, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [ # Level 2
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 4, _, _, _, 1, 3, _, 3, 1, _, _, _, 3, 1],
        [1, _, 1, 1, _, 1, _, 1, _, 1, _, 1, 1, _, 1],
        [1, _, 1, 3, _, _, _, 1, _, _, _, 3, 1, _, 1],
        [1, _, 1, 1, 1, 1, _, 1, _, 1, 1, 1, 1, _, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, 1, 1, _, 1, 1, 1, _, 1, 1, 1, _, 1, 1, 1],
        [1, 3, _, _, _, _, _, 3, 1, 1, _, _, _, 3, 1],
        [1, 1, 1, _, 1, 1, 1, 1, 1, 1, 1, _, 1, 1, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 1, 1, 1, 1, _, 1, _, 1, 1, 1, 1, _, 1],
        [1, _, 1, 3, _, _, _, 1, _, _, _, 3, 1, _, 1],
        [1, _, 1, 1, _, 1, _, 1, _, 1, _, 1, 1, _, 1],
        [1, 3, _, _, _, 1, 3, _, 3, 1, _, _, _, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
]

class Map:
    def __init__(self, game):
        self.game = game
        self.title_size = 100
        
        lvl = getattr(self.game, 'current_level', 0) % len(MAP_DATA)
        self.mini_map = [row[:] for row in MAP_DATA[lvl]]

        self.world_map = {}
        self.files_map = {}
        self.player_start = (2, 2)
        self.get_map()

    def get_map(self):
        self.world_map.clear()
        self.files_map.clear()
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value == 1:
                    self.world_map[(i, j)] = value
                elif value == 3:
                    self.files_map[(i, j)] = value
                elif value == 4:
                    self.player_start = (i + 0.5, j + 0.5)
        self.game.total_files = len(self.files_map)

    def is_wall(self, x, y):
        cell_x = int(x // self.title_size)
        cell_y = int(y // self.title_size)
        return (cell_x, cell_y) in self.world_map

    def check_file_collection(self, player_x, player_y):
        cell_x = int(player_x // self.title_size)
        cell_y = int(player_y // self.title_size)
        
        if (cell_x, cell_y) in self.files_map:
            del self.files_map[(cell_x, cell_y)]
            if 0 <= cell_y < len(self.mini_map) and 0 <= cell_x < len(self.mini_map[cell_y]):
                self.mini_map[cell_y][cell_x] = '_'
            if hasattr(self.game, 'collected_files'):
                self.game.collected_files += 1
            
            if hasattr(self.game, 'sounds') and self.game.sounds:
                self.game.sounds.play_collect()
                
            return True
        return False

    def draw(self, screen):
        for pos, val in self.world_map.items():
            pg.draw.rect(screen, (80, 80, 80), (pos[0] * self.title_size, pos[1] * self.title_size, self.title_size, self.title_size), 2)
        
        for pos in self.files_map:
            block_size = int(self.title_size * 0.5)
            offset = (self.title_size - block_size) // 2
            rect = (int(pos[0] * self.title_size + offset), int(pos[1] * self.title_size + offset), block_size, block_size)
            pg.draw.rect(screen, (0, 120, 255), rect)
            pg.draw.rect(screen, (255, 255, 255), rect, 2)
