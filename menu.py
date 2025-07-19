import pygame as pg


class MainMenu:
    title_pos = pg.Vector2(250, 150)
    start_pos = pg.Vector2(125, 600)  # divide with scaling to get raw value
    leaderboard_pos = pg.Vector2(375, 600)
    bird_pos = pg.Vector2(250, 350)

    def __init__(self, images: tuple[pg.Surface], bird_imgs: tuple[pg.Surface]):

        self.title_img = images[0]
        self.start_img = images[1]
        self.leaderboard_img = images[2]
        self.bird_img = bird_imgs[0]

        self.title_rect = self.title_img.get_rect(center=self.title_pos)
        self.start_rect = self.start_img.get_rect(center=self.start_pos)
        self.leaderboard_rect = self.leaderboard_img.get_rect(center=self.leaderboard_pos)
        self.bird_rect = self.bird_img.get_rect(center=self.bird_pos)

    def draw(self, screen: pg.Surface):
        screen.blit(self.title_img, self.title_rect)
        screen.blit(self.start_img, self.start_rect)
        screen.blit(self.leaderboard_img, self.leaderboard_rect)
        screen.blit(self.bird_img, self.bird_rect)

    def start_pressed(self, mouse_pos):
        if self.start_rect.collidepoint(mouse_pos):
            print("PLAY")
            return True
        return False

    def leaderboard_pressed(self, mouse_pos):
        if self.leaderboard_rect.collidepoint(mouse_pos):
            print("LEADERBOARD")
            return True
        return False


class GameOver:
    board_pos = pg.Vector2(504 / 2, 896 / 2)
    medal_pos = pg.Vector2(138, 458)  # divide with scaling to get raw value
    score1_pos = pg.Vector2(400 - (25 * 2), 420)
    score2_pos = pg.Vector2(400 - 25, 420)
    score3_pos = pg.Vector2(400, 420)
    best1_pos = pg.Vector2(400 - (25 * 2), 495)
    best2_pos = pg.Vector2(400 - 25, 495)
    best3_pos = pg.Vector2(400, 495)
    new_pos = pg.Vector2(315, 460)

    def __init__(self,
                 images: tuple[pg.Surface],
                 medal_images: tuple[pg.Surface],
                 score_images: tuple[pg.Surface],
                 medal_tiers: tuple[int, int, int, int]):
        self.board_img = images[0]
        self.new_img = images[1]
        self.medal_imgs = medal_images
        self.score_imgs = score_images

        self.medal_tiers = medal_tiers

        self.board_rect = self.board_img.get_rect(center=self.board_pos)
        self.new_rect = self.new_img.get_rect(center=self.new_pos)

    def draw(self, screen: pg.Surface, score: int, high_score: int, new_high_score: bool):
        screen.blit(self.board_img, self.board_rect)

        if high_score >= self.medal_tiers[3]:
            medal_img = self.medal_imgs[3]
            medal_rect = medal_img.get_rect(center=self.medal_pos)
            screen.blit(self.medal_imgs[3], medal_rect)

        elif high_score >= self.medal_tiers[2]:
            medal_img = self.medal_imgs[2]
            medal_rect = medal_img.get_rect(center=self.medal_pos)
            screen.blit(self.medal_imgs[2], medal_rect)

        elif high_score >= self.medal_tiers[1]:
            medal_img = self.medal_imgs[1]
            medal_rect = medal_img.get_rect(center=self.medal_pos)
            screen.blit(self.medal_imgs[1], medal_rect)

        elif high_score >= self.medal_tiers[0]:
            medal_img = self.medal_imgs[0]
            medal_rect = medal_img.get_rect(center=self.medal_pos)
            screen.blit(self.medal_imgs[0], medal_rect)

        if new_high_score:
            high_score = score
            screen.blit(self.new_img, self.new_rect)

        score_str = str(score).zfill(3)
        high_score_str = str(high_score).zfill(3)

        s1 = int(score_str[0])
        s2 = int(score_str[1])
        s3 = int(score_str[2])

        hs1 = int(high_score_str[0])
        hs2 = int(high_score_str[1])
        hs3 = int(high_score_str[2])

        score1_img = self.score_imgs[s1]
        score2_img = self.score_imgs[s2]
        score3_img = self.score_imgs[s3]
        screen.blit(score1_img, score1_img.get_rect(center=self.score1_pos))
        screen.blit(score2_img, score2_img.get_rect(center=self.score2_pos))
        screen.blit(score3_img, score3_img.get_rect(center=self.score3_pos))

        high_score1_img = self.score_imgs[hs1]
        high_score2_img = self.score_imgs[hs2]
        high_score3_img = self.score_imgs[hs3]
        screen.blit(high_score1_img, high_score1_img.get_rect(center=self.best1_pos))
        screen.blit(high_score2_img, high_score2_img.get_rect(center=self.best2_pos))
        screen.blit(high_score3_img, high_score3_img.get_rect(center=self.best3_pos))

    def button_pressed(self, mouse_pos):
        pass
