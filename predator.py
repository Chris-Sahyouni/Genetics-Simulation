import pygame
import numpy as np
from utils import resource_path

class Predator(pygame.sprite.Sprite):

    def __init__(self):
        super(Predator, self).__init__()
        self.image = self.setImage()
        self.surf = self.image
        self.rect = [np.random.randint(300, 900), np.random.randint(15, 100)]
        self._time_till_move = self.setRandomTime()
        self._direction = 0
        self._orientation = 1
        self._speed = 2
        # self.perch()


    def setImage(self):
        img = pygame.image.load(resource_path('images/predator.png'))
        return pygame.transform.scale(img, (50, 50))


    def setRandomTime(self):
        return ((np.random.rand() * 3) + 0.5) * 1000


    def setDirection(self):
        if self.rect[0] < 250:
            self._direction = 1
        elif self.rect[0] > 1150:
            self._direction = -1
        else:
            self._direction = np.random.choice([-1, 1])
        self.setOrientation()


    def setOrientation(self):
        if self._orientation != self._direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self._orientation = self._direction


    # def perch(self):
    #     self.image = pygame.transform.rotate(self.image, self._orientation * 45)


    # def unperch(self):
    #     self.image = pygame.transform.rotate(self.image, -self._orientation * 45)


    def update(self, time_elapsed):
        pygame.sprite.Sprite.update(time_elapsed)
        self._time_till_move -= time_elapsed
        if self._time_till_move <= 0:
            if self._direction == 0:
                self.setDirection()
                # self.unperch()
            else:
                self._direction = 0
                # self.perch()

            self._time_till_move = self.setRandomTime()

        if self.rect[0] < 250:
            self._direction = 0
            self.rect[0] += 1
            self._time_till_move = self.setRandomTime()

        if self.rect[0] > 1150:
            self._direction = 0
            self.rect[0] -= 1
            self._time_till_move = self.setRandomTime()

        self.rect[0] += self._speed * self._direction


    def draw(self, screen):
        screen.blit(self.surf, self.rect.topleft)