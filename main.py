import pygame as pg

from bird import Bird
from debug import Debug


class Game:
    FPS = 60
    SCALE = 3.5
    VELOCITY = 3
    WIDTH, HEIGHT = 144 * SCALE, 256 * SCALE
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Flappy Birb")
    clock = pg.time.Clock()
    loop_running = True

    def __init__(self):
        pg.init()
        sprite_path = "D:/Game Sprites/Flappy Bird/Mobile - Flappy Bird - Version 12 Sprites.png"
        self.sprite_sheet = pg.image.load(sprite_path)
        self.sprite_sheet = pg.transform.rotozoom(self.sprite_sheet, 0, self.SCALE)

        self.background_img = self.get_sprite(0, 0, 144, 256)
        self.ground_img = self.get_sprite(293, 0, 460, 56)
        self.ground_2_img = self.ground_img.copy()
        self.ground_x = 0
        self.ground_2_x = self.WIDTH

        bird_img = self.get_sprite(3, 491, 21, 505)

        self.bird = Bird(bird_img)

        self.pipes = []

        self.debug_state = False
        self.debug = Debug()

    def get_sprite(self, x1, y1, x2, y2):
        """ Gets a sprite from the sprite sheet """
        start_pos = pg.Vector2(x1, y1) * self.SCALE  # since sprite sheet is scaled
        end_pos = pg.Vector2(x2, y2) * self.SCALE
        width, height = (end_pos - start_pos)
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), area=(start_pos.x, start_pos.y, width, height))
        return image

    def update(self):
        self.ground_x -= self.VELOCITY
        self.ground_2_x -= self.VELOCITY

        if self.ground_x <= -self.WIDTH:
            self.ground_x = self.WIDTH
        if self.ground_2_x <= -self.WIDTH:
            self.ground_2_x = self.WIDTH

        self.bird.update()
        self.bird.check_collision(self.HEIGHT - self.ground_img.get_height(), self.pipes)

    def draw(self):
        self.screen.fill("lightblue")

        self.screen.blit(
            self.background_img,
            (0, 0)
        )
        self.screen.blit(
            self.ground_img,
            (self.ground_x, self.HEIGHT - self.ground_img.get_height())
        )
        self.screen.blit(
            self.ground_2_img,
            (self.ground_2_x, self.HEIGHT - self.ground_img.get_height())
        )

        self.bird.draw(self.screen)

        if self.debug_state:
            self.debug.show(
                self.screen,
                self.bird.rect,
                self.bird.mask,
                pg.Vector2(self.bird.rect.center)
            )

        pg.display.flip()

    def run(self):
        while self.loop_running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.loop_running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE and not self.bird.jumping:
                        self.bird.jumping = True
                        self.bird.jump()

                    if event.key == pg.K_F1:
                        self.debug_state = not self.debug_state

                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE and self.bird.jumping:
                        self.bird.jumping = False

            self.update()

            self.draw()

            self.clock.tick(self.FPS)

        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
