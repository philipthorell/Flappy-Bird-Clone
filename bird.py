import pygame as pg


class Bird:
    x = 50
    y = 50
    gravity = 0.5
    y_velocity = 0
    jump_power = -10
    jumping = False
    dead = False
    death_anim = False

    def __init__(self, images: tuple[tuple[pg.Surface]], SCREEN_HEIGHT):

        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.birds_imgs = images

        self.bird_idx = 0

        self.current_bird_imgs = self.birds_imgs[self.bird_idx]

        self.image = self.current_bird_imgs[0]
        self.falling_img = self.current_bird_imgs[0]
        self.mid_flap_img = self.current_bird_imgs[1]
        self.full_flap_img = self.current_bird_imgs[2]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + (self.rect.width / 2),
                            self.y + (self.rect.height / 2))
        self.mask = pg.mask.from_surface(self.image)

        self.hit_time = 0
        self.played_death_sfx = False

    def jump(self):
        self.y_velocity = self.jump_power

    def update(self, audio):
        if self.hit_time != 0 and not self.played_death_sfx and pg.time.get_ticks() - self.hit_time >= 500:
            self.played_death_sfx = True
            audio.play_die()

        if self.y <= self.SCREEN_HEIGHT:
            self.y_velocity += self.gravity
            self.y += self.y_velocity
            self.rect.center = (self.x + (self.rect.width / 2),
                                self.y + (self.rect.height / 2))

        if self.dead and not self.death_anim:
            audio.play_hit()
            self.hit_time = pg.time.get_ticks()
            self.death_animation()

    def draw(self, screen: pg.Surface):
        if not self.dead:
            if self.jump_power < self.y_velocity < -7:
                self.image = self.mid_flap_img
            elif -7 < self.y_velocity < -4:
                self.image = self.full_flap_img
            elif -4 < self.y_velocity < -1:
                self.image = self.mid_flap_img
            else:
                self.image = self.falling_img

        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, ground_y, pipes: list, roof_y):
        if self.rect.collidepoint(self.rect.x, ground_y) or self.y < roof_y:
            self.dead = True

        for pipe in pipes:

            top_offset = (pipe.x - self.x, pipe.top - round(self.y))
            bottom_offset = (pipe.x - self.x, pipe.bottom - round(self.y))

            t_collision = self.mask.overlap(pipe.top_mask, top_offset)
            b_collision = self.mask.overlap(pipe.bottom_mask, bottom_offset)

            if t_collision or b_collision:
                self.dead = True

    def death_animation(self):
        self.image = pg.transform.rotozoom(self.falling_img, 50, 1)
        self.y_velocity = self.jump_power
        self.death_anim = True

    def reset(self):
        self.x = 50
        self.y = 50
        self.y_velocity = 0
        self.jumping = False
        self.dead = False
        self.death_anim = False

        self.played_death_sfx = False
        self.hit_time = 0

    def change_skin(self):
        self.bird_idx += 1
        if self.bird_idx >= len(self.birds_imgs):
            self.bird_idx = 0

        self.current_bird_imgs = self.birds_imgs[self.bird_idx]

        self.image = self.current_bird_imgs[0]
        self.falling_img = self.current_bird_imgs[0]
        self.mid_flap_img = self.current_bird_imgs[1]
        self.full_flap_img = self.current_bird_imgs[2]
