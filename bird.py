import pygame as pg


class Bird:
    position = pg.Vector2(50, 50)
    gravity = 0.5
    y_velocity = 0
    jump_power = -10
    jumping = False

    def __init__(self, image: pg.Surface):
        self.image = image
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pg.mask.from_surface(self.image)

    def jump(self):
        self.y_velocity = self.jump_power

    def update(self):
        self.y_velocity += self.gravity
        self.position.y += self.y_velocity
        self.rect.center = self.position

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)

    def check_collision(self, ground_y, pipes: list):
        if self.rect.collidepoint(self.rect.x, ground_y):
            print("Hit ground - DEAD")
            return True

        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                offset = (pipe.rect.x - self.rect.x, pipe.rect.y - self.rect.y)
                if self.mask.overlap(pipe.mask, offset):
                    print("Hit pipe - DEAD")
                    return True
