import pygame as pg
import pygame.display


class Game:
    FPS = 60
    SCALE = 3.5
    VELOCITY = 7
    WIDTH, HEIGHT = 144 * SCALE, 256 * SCALE
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Birb")
    clock = pg.time.Clock()
    running = True

    def __init__(self):
        pg.init()
        sprite_path = "D:/Game Sprites/Flappy Bird/Mobile - Flappy Bird - Version 12 Sprites.png"
        self.sprite_sheet = pg.image.load(sprite_path).convert_alpha()
        self.sprite_sheet = pg.transform.rotozoom(self.sprite_sheet, 0, self.SCALE)

        self.background_img = self.get_sprite(0, 0, 144, 256)
        self.ground_img = self.get_sprite(293, 0, 460, 56)

    def get_sprite(self, x1, y1, x2, y2):
        """ Gets a sprite from the sprite sheet """
        start_pos = pg.Vector2(x1, y1) * self.SCALE  # since sprite sheet is scaled
        end_pos = pg.Vector2(x2, y2) * self.SCALE
        width, height = (end_pos - start_pos)
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), area=(start_pos.x, start_pos.y, width, height))
        return image

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.ground_img, (0, self.HEIGHT - self.ground_img.get_height()))

    def run(self):
        while self.running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.screen.fill("lightblue")

            self.draw()

            pg.display.flip()
            self.clock.tick(self.FPS)

        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()

