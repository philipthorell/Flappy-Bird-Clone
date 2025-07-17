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

    def __init__(self, image: pg.Surface, image2: pg.Surface, image3: pg.Surface, SCREEN_HEIGHT):
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.image = image
        self.falling_img = image
        self.mid_flap_img = image2
        self.full_flap_img = image3
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + (self.rect.width / 2),
                            self.y + (self.rect.height / 2))
        self.mask = pg.mask.from_surface(self.image)

    def jump(self):
        self.y_velocity = self.jump_power

    def update(self):
        if self.y < self.SCREEN_HEIGHT:
            self.y_velocity += self.gravity
            self.y += self.y_velocity
            self.rect.center = (self.x + (self.rect.width / 2),
                                self.y + (self.rect.height / 2))

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

    def check_collision(self, ground_y, pipes: list):
        if self.rect.collidepoint(self.rect.x, ground_y):
            print("Hit ground - DEAD")
            self.dead = True

        for pipe in pipes:

            top_offset = (pipe.x - self.x, pipe.top - round(self.y))
            bottom_offset = (pipe.x - self.x, pipe.bottom - round(self.y))

            t_collision = self.mask.overlap(pipe.top_mask, top_offset)
            b_collision = self.mask.overlap(pipe.bottom_mask, bottom_offset)

            if t_collision or b_collision:
                if t_collision:
                    print("TOP!")
                if b_collision:
                    print("BOTTOM!")
                self.dead = True

    def death_animation(self):
        self.image = pg.transform.rotozoom(self.falling_img, 50, 1)
        self.y_velocity = self.jump_power
        self.death_anim = True
