import pygame as pg


class Bird:
    x = 50
    y = 50
    gravity = 0.5
    y_velocity = 0
    jump_power = -10
    jumping = False

    def __init__(self, image: pg.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + (self.rect.width / 2),
                            self.y + (self.rect.height / 2))
        self.mask = pg.mask.from_surface(self.image)

    def jump(self):
        self.y_velocity = self.jump_power

    def update(self):
        self.y_velocity += self.gravity
        self.y += self.y_velocity
        self.rect.center = (self.x + (self.rect.width / 2),
                            self.y + (self.rect.height / 2))

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, ground_y, pipes: list):
        if self.rect.collidepoint(self.rect.x, ground_y):
            print("Hit ground - DEAD")
            return True

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
                return True

        return False
