import pygame as pg


class Bird:
    position = pg.Vector2(50, 50)
    gravity = 0.5
    y_velocity = 0
    jump_power = -10
    jumping = False

    def __init__(self, image: pg.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.position.x + (self.rect.width / 2),
                            self.position.y + (self.rect.height / 2))
        self.mask = pg.mask.from_surface(self.image)

    def jump(self):
        self.y_velocity = self.jump_power

    def update(self):
        self.y_velocity += self.gravity
        self.position.y += self.y_velocity
        self.rect.center = (self.position.x + (self.rect.width / 2),
                            self.position.y + (self.rect.height / 2))

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.position)

    def check_collision(self, ground_y, pipes: list):
        if self.rect.collidepoint(self.rect.x, ground_y):
            print("Hit ground - DEAD")
            return True

        pipe = [p for p in pipes if not p.passed][0]

        top_offset = (pipe.x - self.position.x, pipe.top - round(self.position.y))
        bottom_offset = (pipe.x - self.position.x, pipe.bottom - round(self.position.y))

        t_collision = self.mask.overlap(pipe.top_mask, top_offset)
        b_collision = self.mask.overlap(pipe.bottom_mask, bottom_offset)

        if t_collision or b_collision:
            if t_collision:
                print("TOP!")
            print("Hit pipe - DEAD")
            return True

        return False
