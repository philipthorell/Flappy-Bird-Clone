class Ground:

    def __init__(self, image, SCREEN_WIDTH, SCREEN_HEIGHT, VELOCITY):
        self.image = image
        self.image2 = self.image.copy()

        self.SCREEN_WIDTH = SCREEN_WIDTH

        self.x = 0
        self.x2 = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - self.image.get_height()

        self.VELOCITY = VELOCITY

    def move(self):
        self.x -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x <= -self.SCREEN_WIDTH:
            self.x = self.SCREEN_WIDTH
        if self.x2 <= -self.SCREEN_WIDTH:
            self.x2 = self.SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.image2, (self.x2, self.y))

