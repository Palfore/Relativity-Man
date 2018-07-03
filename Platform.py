import pygame
import settings as settings


class Platform:
    def __init__(self, top, left, width, height):
        self.top = top
        self.left = left
        self.width = width
        self.height = height

    def get_left(self):
        return self.left

    def get_top(self):
        return self.top

    def get_bottom(self):
        return self.top + self.height

    def get_right(self):
        return self.left + self.width

    def draw(self, screen):
        thickness = 4
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.left, self.top, self.width, self.height))

        if settings.is_debugging():
            pygame.draw.line(screen, (100, 100, 100),
                             (self.left, self.top), (self.get_right(), self.top), thickness)
            pygame.draw.line(screen, (100, 100, 100),
                             (self.left, self.get_bottom()), (self.get_right(), self.get_bottom()), thickness)

    def update(self, dt):
        pass
