import pygame as pg


class Audio:

    def __init__(self):
        pg.mixer.init()

        self.die_sfx = pg.mixer.Sound("sfx/die.mp3")
        self.die_sfx.set_volume(0.2)

        self.flap_sfx = pg.mixer.Sound("sfx/flap.mp3")
        self.flap_sfx.set_volume(0.2)

        self.hit_sfx = pg.mixer.Sound("sfx/hit.mp3")
        self.hit_sfx.set_volume(0.2)

        self.point_sfx = pg.mixer.Sound("sfx/point.mp3")
        self.point_sfx.set_volume(0.1)

    def play_die(self):
        self.die_sfx.play()

    def play_flap(self):
        self.flap_sfx.play()

    def play_hit(self):
        self.hit_sfx.play()

    def play_point(self):
        self.point_sfx.play()

