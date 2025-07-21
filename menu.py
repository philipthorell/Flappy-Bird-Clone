import pygame as pg


class MainMenu:
    title_pos = pg.Vector2(250, 150)
    start_pos = pg.Vector2(125, 600)  # divide with scaling to get raw value
    mode_pos = pg.Vector2(375, 600)
    bird_pos = pg.Vector2(250, 350)

    def __init__(self, images: tuple[pg.Surface], bird_imgs: tuple[pg.Surface], anim_cooldown):

        self.title_img = images[0]
        self.start_img = images[1]
        self.day_img = images[2]
        self.night_img = images[3]
        self.bird_imgs = bird_imgs + (bird_imgs[1], )

        self.title_rect = self.title_img.get_rect(center=self.title_pos)
        self.start_rect = self.start_img.get_rect(center=self.start_pos)
        self.mode_rect = self.day_img.get_rect(center=self.mode_pos)

        self.animation_cooldown = anim_cooldown  # milliseconds
        self.bird_frame = 0
        self.last_time = pg.time.get_ticks()

    def animation(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_time > self.animation_cooldown:
            self.last_time = current_time
            self.bird_frame += 1
            if self.bird_frame >= len(self.bird_imgs):
                self.bird_frame = 0

    def draw(self, screen: pg.Surface, day_time: bool):
        screen.blit(self.title_img, self.title_rect)
        screen.blit(self.start_img, self.start_rect)

        bird_img = self.bird_imgs[self.bird_frame]
        bird_rect = bird_img.get_rect(center=self.bird_pos)
        screen.blit(bird_img, bird_rect)

        mode_img = self.night_img
        mode_rect = mode_img.get_rect(center=self.mode_pos)
        if day_time:
            mode_img = self.day_img
            mode_rect = mode_img.get_rect(center=self.mode_pos)
        screen.blit(mode_img, mode_rect)

    def start_pressed(self, mouse_pos):
        if self.start_rect.collidepoint(mouse_pos):
            return True
        return False

    def mode_pressed(self, mouse_pos):
        if self.mode_rect.collidepoint(mouse_pos):
            return True
        return False


class GameOver:
    title_pos = pg.Vector2(504 / 2, 200)
    board_pos = pg.Vector2(504 / 2, 896 / 2)
    medal_pos = pg.Vector2(138, 458)  # divide with scaling to get raw value
    sparkle_pos = pg.Vector2(160, 430)
    score1_pos = pg.Vector2(400 - (25 * 2), 420)
    score2_pos = pg.Vector2(400 - 25, 420)
    score3_pos = pg.Vector2(400, 420)
    best1_pos = pg.Vector2(400 - (25 * 2), 495)
    best2_pos = pg.Vector2(400 - 25, 495)
    best3_pos = pg.Vector2(400, 495)
    new_pos = pg.Vector2(315, 460)
    menu_pos = pg.Vector2(52 + 100, 580)
    ok_pos = pg.Vector2(504 - 52 - 100, 580)

    def __init__(self,
                 images: tuple[pg.Surface],
                 medal_images: tuple[pg.Surface],
                 sparkle_images: tuple[pg.Surface],
                 score_images: tuple[pg.Surface],
                 medal_tiers: tuple[int, int, int, int],
                 anim_cooldown: int):
        self.title_img = images[0]
        self.board_img = images[1]
        self.new_img = images[2]
        self.menu_img = images[3]
        self.ok_img = images[4]
        self.medal_imgs = medal_images
        self.sparkle_imgs = sparkle_images + (sparkle_images[1], )
        self.score_imgs = score_images

        self.medal_tiers = medal_tiers

        self.title_rect = self.title_img.get_rect(center=self.title_pos)
        self.board_rect = self.board_img.get_rect(center=self.board_pos)
        self.new_rect = self.new_img.get_rect(center=self.new_pos)
        self.menu_rect = self.menu_img.get_rect(center=self.menu_pos)
        self.ok_rect = self.ok_img.get_rect(center=self.ok_pos)

        self.animation_cooldown = anim_cooldown  # milliseconds
        self.sparkle_frame = 0
        self.last_time = pg.time.get_ticks()

    def animation(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_time > self.animation_cooldown:
            self.last_time = current_time
            self.sparkle_frame += 1
            if self.sparkle_frame >= len(self.sparkle_imgs):
                self.sparkle_frame = 0

    def show_medal(self, screen, high_score):
        if high_score >= self.medal_tiers[3]:
            medal_img = self.medal_imgs[3]
        elif high_score >= self.medal_tiers[2]:
            medal_img = self.medal_imgs[2]
        elif high_score >= self.medal_tiers[1]:
            medal_img = self.medal_imgs[1]
        elif high_score >= self.medal_tiers[0]:
            medal_img = self.medal_imgs[0]
        else:
            return

        medal_rect = medal_img.get_rect(center=self.medal_pos)
        screen.blit(medal_img, medal_rect)

        sparkle_img = self.sparkle_imgs[self.sparkle_frame]
        sparkle_rect = sparkle_img.get_rect(center=self.sparkle_pos)
        screen.blit(sparkle_img, sparkle_rect)

    def get_score_str(self, score):
        score_str = str(score).zfill(3)
        s1 = int(score_str[0])
        s2 = int(score_str[1])
        s3 = int(score_str[2])
        score1_img = self.score_imgs[s1]
        score2_img = self.score_imgs[s2]
        score3_img = self.score_imgs[s3]
        score_imgs = (score1_img, score2_img, score3_img)
        return score_imgs

    def draw(self, screen: pg.Surface, score: int, high_score: int, new_high_score: bool):
        screen.blit(self.title_img, self.title_rect)
        screen.blit(self.board_img, self.board_rect)

        self.show_medal(screen, high_score)

        if new_high_score:
            high_score = score
            screen.blit(self.new_img, self.new_rect)

        score_imgs = self.get_score_str(score)
        screen.blit(score_imgs[0], score_imgs[0].get_rect(center=self.score1_pos))
        screen.blit(score_imgs[1], score_imgs[1].get_rect(center=self.score2_pos))
        screen.blit(score_imgs[2], score_imgs[2].get_rect(center=self.score3_pos))

        high_score_imgs = self.get_score_str(high_score)
        screen.blit(high_score_imgs[0], high_score_imgs[0].get_rect(center=self.best1_pos))
        screen.blit(high_score_imgs[1], high_score_imgs[1].get_rect(center=self.best2_pos))
        screen.blit(high_score_imgs[2], high_score_imgs[2].get_rect(center=self.best3_pos))

        screen.blit(self.menu_img, self.menu_rect)
        screen.blit(self.ok_img, self.ok_rect)

    def menu_pressed(self, mouse_pos):
        if self.menu_rect.collidepoint(mouse_pos):
            return True
        return False

    def ok_pressed(self, mouse_pos):
        if self.ok_rect.collidepoint(mouse_pos):
            return True
        return False
