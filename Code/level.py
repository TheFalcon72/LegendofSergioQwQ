import pygame
from settings import *
from tile import Tile
from player import Player
from network import Network
from debug import debug


class Level:
    def __init__(self):
        # Sprite Group Setup
        self.p2Pos = None
        self.string = None
        self.visible_sprite = YSortCamaraGroup()
        self.obstacles_sprite = pygame.sprite.Group()
        self.net = Network()
        self.p1 = []
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
                    self.player1 = Player((x, y), [self.visible_sprite], self.obstacles_sprite)
                if col == 'q':
                    self.player2 = Player((x, y), [self.visible_sprite], self.obstacles_sprite)

    def read_pos(self, str):
        str = str.split(",")
        return int(str[0]), int(str[1])

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1])

    def run(self):
        self.visible_sprite.custom_draw(self.player1, self.player2)
        # Update and Draw the game
        self.p1.insert(self.player1.rect.x, self.player1.rect.y)

        self.p2Pos = self.read_pos(self.net.send(self.make_pos((self.player1.rect.x, self.player1.rect.y))))
        self.player2.hitbox.x = self.p2Pos[0]
        self.player2.hitbox.y = self.p2Pos[1]
        self.player2.update()
        self.visible_sprite.update()


class YSortCamaraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()

        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player1, player2):
        # getting the offset
        self.offset.x = player1.rect.centerx - self.half_width
        self.offset.y = player1.rect.centery - self.half_height

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
