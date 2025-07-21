import pygame as pg

from sprite_loader import SpriteLoader
from ground import Ground
from bird import Bird
from pipe import Pipe
from menu import MainMenu, GameOver
from debug import Debug


"""
    ADD BIRD COLOR SWITCHING
    ADD SOUNDS
"""


class Game:
    FPS = 60
    SCALE = 3.5  # 3.5
    VELOCITY = 3
    WIDTH, HEIGHT = 144 * SCALE, 256 * SCALE
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Flappy Birb")
    pg.mouse.set_visible(False)
    clock = pg.time.Clock()
    running = True

    bronze = 25
    silver = 50
    gold = 100
    platinum = 200

    single_point_pos = pg.Vector2(504 / 2, 100)
    double_point_pos1 = pg.Vector2(504 / 2 - 22, 100)
    double_point_pos2 = pg.Vector2(504 / 2 + 22, 100)
    triple_point_pos1 = pg.Vector2(504 / 2 - 43, 100)
    triple_point_pos3 = pg.Vector2(504 / 2 + 43, 100)

    day = True

    bird_anim_cooldown = 75
    sparkle_anim_cooldown = 250

    def __init__(self):
        pg.init()

        self.sprite_loader = SpriteLoader(self.SCALE)

        self.cursor = self.sprite_loader.get_cursor()

        self.bg_imgs = self.sprite_loader.get_background()
        ground_img = self.sprite_loader.get_ground()
        bird_imgs = self.sprite_loader.get_bird()
        self.pipe_imgs = self.sprite_loader.get_pipe()
        self.point_imgs = self.sprite_loader.get_points()
        main_menu_imgs = self.sprite_loader.get_main_menu()
        game_over_imgs = self.sprite_loader.get_game_over()
        medal_imgs = self.sprite_loader.get_medal()
        sparkle_imgs = self.sprite_loader.get_sparkle()
        score_imgs = self.sprite_loader.get_score()

        self.background_img = self.bg_imgs[0]
        self.ground = Ground(ground_img, self.WIDTH, self.HEIGHT, self.VELOCITY)
        self.bird = Bird(bird_imgs, self.HEIGHT)
        pipe1 = Pipe(self.pipe_imgs, self.WIDTH, self.VELOCITY, 1, self.day)
        pipe2 = Pipe(self.pipe_imgs, self.WIDTH, self.VELOCITY, 2, self.day)
        pipe3 = Pipe(self.pipe_imgs, self.WIDTH, self.VELOCITY, 3, self.day)
        self.pipes = [pipe1, pipe2, pipe3]
        self.main_menu_screen = MainMenu(main_menu_imgs, bird_imgs, self.bird_anim_cooldown)
        self.game_over_screen = GameOver(game_over_imgs, medal_imgs, sparkle_imgs, score_imgs,
                                         (self.bronze, self.silver, self.gold, self.platinum),
                                         self.sparkle_anim_cooldown)

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

    def change_sprites(self):
        self.day = not self.day
        if self.day:
            self.background_img = self.bg_imgs[0]
        else:
            self.background_img = self.bg_imgs[1]
        for pipe in self.pipes:
            pipe.change_sprite(self.day)

    def reset(self):
        self.bird.reset()
        pipe1 = Pipe(self.pipe_imgs, self.WIDTH, self.VELOCITY, 1, self.day)
        pipe2 = Pipe(self.pipe_imgs, self.WIDTH, self.VELOCITY, 2, self.day)
        pipe3 = Pipe(self.pipe_imgs, self.WIDTH, self.VELOCITY, 3, self.day)
        self.pipes = [pipe1, pipe2, pipe3]
        self.points = 0
        self.updated_score_file = False
        self.new_high_score = False

    def update(self):
        if self.main_menu:
            self.ground.move()
            self.main_menu_screen.animation()
            if self.updated_score_file:
                self.updated_score_file = False
            if self.new_high_score:
                self.new_high_score = False

        elif self.game_over:
            self.game_over_screen.animation()
            if not self.updated_score_file:
                self.update_high_score()

        elif self.gaming:
            if not self.bird.dead:
                self.ground.move()

                for pipe in self.pipes:
                    pipe.move()
                    if not pipe.passed and self.bird.x > pipe.x + pipe.width:
                        self.points += 1
                        pipe.passed = True

            self.bird.check_collision(self.ground.y, self.pipes)

            self.bird.update()

            if self.bird.y > self.HEIGHT:
                self.game_over = True
                self.gaming = False

    def draw_points(self):
        points_str = str(self.points)
        if len(points_str) == 1:
            point_img = self.point_imgs[self.points]
            self.screen.blit(point_img, point_img.get_rect(center=self.single_point_pos))
        elif len(points_str) == 2:
            point_img1 = self.point_imgs[int(points_str[0])]
            point_img2 = self.point_imgs[int(points_str[1])]
            self.screen.blit(point_img1, point_img1.get_rect(center=self.double_point_pos1))
            self.screen.blit(point_img2, point_img2.get_rect(center=self.double_point_pos2))
        elif len(points_str) == 3:
            point_img1 = self.point_imgs[int(points_str[0])]
            point_img2 = self.point_imgs[int(points_str[1])]
            point_img3 = self.point_imgs[int(points_str[2])]
            self.screen.blit(point_img1, point_img1.get_rect(center=self.triple_point_pos1))
            self.screen.blit(point_img2, point_img2.get_rect(center=self.single_point_pos))
            self.screen.blit(point_img3, point_img3.get_rect(center=self.triple_point_pos3))

    def draw(self):
        self.screen.fill("lightblue")

        if self.day:
            bg_img = self.bg_imgs[0]
        else:
            bg_img = self.bg_imgs[1]

        self.screen.blit(bg_img, (0, 0))

        if self.gaming or self.game_over:
            for pipe in self.pipes:
                pipe.draw(self.screen)

        self.ground.draw(self.screen)

        if self.main_menu:
            self.main_menu_screen.draw(self.screen, self.day)

        if self.gaming:
            self.bird.draw(self.screen)
            self.draw_points()

        if self.game_over:
            self.game_over_screen.draw(self.screen, self.points, self.high_score, self.new_high_score)

        mouse_pos = pg.mouse.get_pos()
        self.screen.blit(self.cursor, (mouse_pos[0] - 21, mouse_pos[1] - 13))

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
                self.main_menu_screen.mode_rect,
                None,
                pg.Vector2(self.main_menu_screen.mode_pos),
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

            if self.gaming and event.key == pg.K_SPACE and not self.bird.dead and not self.bird.jumping:
                self.bird.jumping = True
                self.bird.jump()

        if self.gaming and event.type == pg.KEYUP:
            if event.key == pg.K_SPACE and self.bird.jumping:
                self.bird.jumping = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            if self.main_menu:
                if self.main_menu_screen.start_pressed(mouse_pos):
                    self.gaming = True
                    self.main_menu = False
                elif self.main_menu_screen.mode_pressed(mouse_pos):
                    self.change_sprites()

            elif self.gaming and not self.bird.dead and not self.bird.jumping:
                self.bird.jumping = True
                self.bird.jump()

            elif self.game_over:
                if self.game_over_screen.menu_pressed(mouse_pos):
                    self.main_menu = True
                    self.game_over = False
                    self.reset()
                elif self.game_over_screen.ok_pressed(mouse_pos):
                    self.gaming = True
                    self.game_over = False
                    self.reset()

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
