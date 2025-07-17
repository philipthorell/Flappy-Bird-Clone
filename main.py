import pygame as pg


class Game:
    FPS = 60
    SCALE = 3.5
    screen = pg.display.set_mode((144 * SCALE, 256 * SCALE))
    clock = pg.time.Clock()
    running = True

    def __init__(self):
        pg.init()

    def run(self):
        while self.running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.screen.fill("lightblue")

            pg.display.flip()
            self.clock.tick(self.FPS)

        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()

