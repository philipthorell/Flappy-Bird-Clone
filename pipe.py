import pygame as pg

import random


class Pipe:
    gap = 200
    height = 0
    top = 0
    bottom = 0

    def __init__(self, images: tuple[pg.Surface], SCREEN_WIDTH, VELOCITY, POSITION, DAY_TIME):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.VELOCITY = VELOCITY

        self.x = SCREEN_WIDTH + (250 * (POSITION - 1))

        self.day_pipe = images[0]
        self.night_pipe = images[1]

        if DAY_TIME:
            pipe_sprite = self.day_pipe
        else:
            pipe_sprite = self.night_pipe

        self.pipe_top = pipe_sprite
        self.pipe_bottom = pg.transform.flip(pipe_sprite, False, True)

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

    def change_sprite(self, day_time: bool):
        if day_time:
            self.pipe_top = self.day_pipe
            self.pipe_bottom = pg.transform.flip(self.day_pipe, False, True)
        else:
            self.pipe_top = self.night_pipe
            self.pipe_bottom = pg.transform.flip(self.night_pipe, False, True)

    def move(self):
        self.x -= self.VELOCITY
        self.top_rect.center = (self.x + (self.width / 2),
                                self.top + (self.pipe_top.get_height() / 2))
        self.bottom_rect.center = (self.x + (self.width / 2),
                                   self.bottom + (self.pipe_bottom.get_height() / 2))

        self.top_mask = pg.mask.from_surface(self.pipe_top)
        self.bottom_mask = pg.mask.from_surface(self.pipe_bottom)

        if self.x + self.width <= 0:
            self.x = self.SCREEN_WIDTH + 150
            self.set_height()
            self.passed = False

    def draw(self, screen: pg.Surface):
        screen.blit(self.pipe_top, (self.x, self.top))
        screen.blit(self.pipe_bottom, (self.x, self.bottom))
