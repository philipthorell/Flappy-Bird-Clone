import pygame as pg

from sprite_loader import SpriteLoader
from ground import Ground
from bird import Bird
from pipe import Pipe
from menu import MainMenu, GameOver
from debug import Debug


class Game:
    FPS = 60
    SCALE = 3.5  # 3.5
    VELOCITY = 3
    WIDTH, HEIGHT = 144 * SCALE, 256 * SCALE
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Flappy Birb")
    clock = pg.time.Clock()
    running = True

    bronze = 25
    silver = 50
    gold = 100
    platinum = 200

    def __init__(self):
        pg.init()

        self.sprite_loader = SpriteLoader(self.SCALE)

        self.bg_img = self.sprite_loader.get_background()
        ground_img = self.sprite_loader.get_ground()
        bird_imgs = self.sprite_loader.get_bird()
        pipe_img = self.sprite_loader.get_pipe()
        main_menu_imgs = self.sprite_loader.get_main_menu()
        game_over_imgs = self.sprite_loader.get_game_over()
        medal_imgs = self.sprite_loader.get_medal()
        score_imgs = self.sprite_loader.get_score()

        self.ground = Ground(ground_img, self.WIDTH, self.HEIGHT, self.VELOCITY)
        self.bird = Bird(bird_imgs, self.HEIGHT)
        pipe1 = Pipe(pipe_img, self.WIDTH, self.VELOCITY, 1)
        pipe2 = Pipe(pipe_img, self.WIDTH, self.VELOCITY, 2)
        pipe3 = Pipe(pipe_img, self.WIDTH, self.VELOCITY, 3)
        self.pipes = [pipe1, pipe2, pipe3]
        self.main_menu_screen = MainMenu(main_menu_imgs, bird_imgs)
        self.game_over_screen = GameOver(game_over_imgs, medal_imgs, score_imgs,
                                         (self.bronze, self.silver, self.gold, self.platinum))

        self.main_menu = True
        self.game_over = False
        self.gaming = False

        self.points = 0
        self.high_score = 0

        self.read_high_score()

        self.updated_score_file = False
        self.new_high_score = False

        self.debug_state = False
        self.debug = Debug(self.screen)

    def read_high_score(self):
        try:
            with open("score.txt", "r") as file:
                try:
                    self.high_score = int(file.readline())
                    if self.high_score > 999:
                        self.high_score = 999
                except ValueError:
                    pass
        except FileNotFoundError:
            pass

    def update_high_score(self):
        if self.points > self.high_score:
            self.new_high_score = True
            self.high_score = self.points
            with open("score.txt", "w") as file:
                file.write(str(self.high_score))

        self.updated_score_file = True

    def update(self):
        if self.main_menu:
            self.ground.move()
            if self.updated_score_file:
                self.updated_score_file = False
            if self.new_high_score:
                self.new_high_score = False

        elif self.game_over:
            if not self.updated_score_file:
                self.update_high_score()

        elif self.gaming:
            if not self.bird.dead:
                self.ground.move()

                for pipe in self.pipes:
                    pipe.move(self.bird.x)
                    if not pipe.passed and self.bird.x > pipe.x + pipe.width:
                        self.points += 1
                        pipe.passed = True

            self.bird.check_collision(self.ground.y, self.pipes)

            self.bird.update()

            if self.bird.y > self.HEIGHT:
                self.game_over = True
                self.gaming = False

    def draw(self):
        self.screen.fill("lightblue")

        self.screen.blit(self.bg_img, (0, 0))

        if self.gaming or self.game_over:
            for pipe in self.pipes:
                pipe.draw(self.screen)

        self.ground.draw(self.screen)

        if self.main_menu:
            self.main_menu_screen.draw(self.screen)

        if self.gaming:
            self.bird.draw(self.screen)

        if self.game_over:
            self.game_over_screen.draw(self.screen, self.points, self.high_score, self.new_high_score)

        if self.debug_state:
            self.show_debug_info()

        pg.display.flip()

    def show_debug_info(self):
        if self.main_menu:
            self.debug.show(
                self.main_menu_screen.start_rect,
                None,
                pg.Vector2(self.main_menu_screen.start_pos),
                coords_color="black"
            )
            self.debug.show(
                self.main_menu_screen.leaderboard_rect,
                None,
                pg.Vector2(self.main_menu_screen.leaderboard_pos),
                coords_color="black"
            )

        elif self.gaming:
            self.debug.show_ground(
                self.ground.y,
                self.WIDTH
            )
            self.debug.show(
                self.bird.rect,
                self.bird.mask,
                pg.Vector2((self.bird.x, self.bird.y))
            )
            for pipe in self.pipes:
                self.debug.show(
                    pipe.top_rect,
                    pipe.top_mask,
                    pg.Vector2(pipe.x, pipe.top)
                )
                self.debug.show(
                    pipe.bottom_rect,
                    pipe.bottom_mask,
                    pg.Vector2(pipe.x, pipe.bottom)
                )

        elif self.game_over:
            self.debug.show(
                self.game_over_screen.score_imgs[0].get_rect(center=self.game_over_screen.score1_pos),
                None,
                None
            )

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F1:
                self.debug_state = not self.debug_state

            if self.gaming and event.key == pg.K_SPACE and not self.bird.jumping:
                self.bird.jumping = True
                self.bird.jump()

        if self.gaming and event.type == pg.KEYUP:
            if event.key == pg.K_SPACE and self.bird.jumping:
                self.bird.jumping = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.main_menu:
                if self.main_menu_screen.start_pressed(pg.mouse.get_pos()):
                    self.gaming = True
                    self.main_menu = False
                if self.main_menu_screen.leaderboard_pressed(pg.mouse.get_pos()):
                    pass

            elif self.gaming and not self.bird.jumping:
                self.bird.jumping = True
                self.bird.jump()

        if self.gaming and event.type == pg.MOUSEBUTTONUP and self.bird.jumping:
            self.bird.jumping = False

    def run(self):
        while self.running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                self.handle_input(event)

            self.update()

            self.draw()

            self.clock.tick(self.FPS)

        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
