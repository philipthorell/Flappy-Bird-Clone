import pygame as pg


class SpriteLoader:
    def __init__(self, SCALE):
        self.SCALE = SCALE
        sprite_path = "D:/Game Sprites/Flappy Bird/Mobile - Flappy Bird - Version 12 Sprites.png"
        self.sprite_sheet = pg.image.load(sprite_path)
        self.sprite_sheet = pg.transform.rotozoom(self.sprite_sheet, 0, self.SCALE)

        blue_bird_img = self.get_sprite(87, 491, 105, 505)
        blue_bird2_img = self.get_sprite(115, 329, 133, 343)
        blue_bird3_img = self.get_sprite(115, 355, 133, 369)
        self.blue_bird_imgs = (blue_bird_img, blue_bird2_img, blue_bird3_img)

        red_bird_img = self.get_sprite(115, 381, 133, 395)
        red_bird2_img = self.get_sprite(115, 407, 133, 421)
        red_bird3_img = self.get_sprite(115, 433, 133, 447)
        self.red_bird_imgs = (red_bird_img, red_bird2_img, red_bird3_img)

    def get_sprite(self, x1, y1, x2, y2):
        """ Gets a sprite from the sprite sheet """
        start_pos = pg.Vector2(x1, y1) * self.SCALE  # since sprite sheet is scaled
        end_pos = pg.Vector2(x2, y2) * self.SCALE
        width, height = (end_pos - start_pos)
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), area=(start_pos.x, start_pos.y, width, height))
        return image

    def get_background(self):
        background_img = self.get_sprite(0, 0, 144, 256)
        return background_img

    def get_ground(self):
        ground_img = self.get_sprite(293, 0, 460, 56)
        return ground_img

    def get_pipe(self):
        pipe_img = self.get_sprite(55, 324, 82, 484)
        return pipe_img

    def get_main_menu(self):
        title_img = self.get_sprite(351, 91, 441, 116)
        start_img = self.get_sprite(354, 118, 407, 147)
        leaderboard_img = self.get_sprite(414, 118, 467, 147)
        main_menu_imgs = (title_img, start_img, leaderboard_img)
        return main_menu_imgs

    def get_game_over(self):
        board_img = self.get_sprite(3, 259, 117, 318)
        medal_img = self.get_sprite(112, 477, 135, 500)
        new_img = self.get_sprite(112, 501, 129, 510)
        game_over_imgs = (board_img, medal_img, new_img)
        return game_over_imgs

    def get_score(self):
        score_zero_img = self.get_sprite(147, 258, 157, 271)
        score_one_img = self.get_sprite(158, 258, 166, 271)
        score_two_img = self.get_sprite(167, 258, 177, 271)
        score_three_img = self.get_sprite(178, 258, 188, 271)
        score_four_img = self.get_sprite(189, 258, 199, 271)
        score_five_img = self.get_sprite(200, 258, 210, 271)
        score_six_img = self.get_sprite(211, 258, 221, 271)
        score_seven_img = self.get_sprite(222, 258, 232, 271)
        score_eight_img = self.get_sprite(233, 258, 243, 271)
        score_nine_img = self.get_sprite(244, 258, 254, 271)
        score_imgs = (score_zero_img, score_one_img, score_two_img, score_three_img,
                      score_four_img, score_five_img, score_six_img, score_seven_img,
                      score_eight_img, score_nine_img)
        return score_imgs

    def get_bird(self):
        bird_img = self.get_sprite(3, 491, 21, 505)
        bird2_img = self.get_sprite(31, 491, 49, 505)
        bird3_img = self.get_sprite(59, 491, 77, 505)
        bird_imgs = (bird_img, bird2_img, bird3_img)
        return bird_imgs
