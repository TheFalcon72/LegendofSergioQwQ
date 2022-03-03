import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite Group Setup
        self.visible_sprite = pygame.sprite.Group()
        self.obstacles_sprite = pygame.sprite.Group()

        # Sprite Setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprite, self.obstacles_sprite])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprite])

    def run(self):
        # Update and Draw the game
        self.visible_sprite.draw(self.display_surface)
        self.visible_sprite.update()
        debug(self.player.direction)