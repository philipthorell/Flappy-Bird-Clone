import random

import pygame as pg


class Pipe:
    gap = 200
    height = 0
    top = 0
    bottom = 0

    def __init__(self, image: pg.Surface, x_pos):
        self.x = x_pos
        self.image = image

        self.pipe_top = self.image
        self.pipe_bottom = pg.transform.flip(self.image, False, True)

        self.width = self.pipe_top.get_width()

        self.top_rect = self.pipe_top.get_rect()
        self.bottom_rect = self.pipe_bottom.get_rect()

        self.top_mask = pg.mask.from_surface(self.pipe_top)
        self.bottom_mask = pg.mask.from_surface(self.pipe_bottom)

        self.set_height()

        self.passed = False

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self, velocity):
        self.x -= velocity
        self.top_rect.center = (self.x + (self.width / 2),
                                self.top + (self.pipe_top.get_height() / 2))
        self.bottom_rect.center = (self.x + (self.width / 2),
                                   self.bottom + (self.pipe_bottom.get_height() / 2))

    def draw(self, screen: pg.Surface):
        screen.blit(self.pipe_top, (self.x, self.top))
        screen.blit(self.pipe_bottom, (self.x, self.bottom))
