import pygame
import settings as settings
from math import sqrt, atan2, sin ,cos


class Player:
    def __init__(self, init_x, init_y):
        self.image = pygame.image.load("assets/einstein.png")
        self.proper_height = 150
        self.proper_width = 150
        self.mass = 1

        self.height = self.proper_height
        self.width = self.proper_width

        self.bounciness = 0.2
        self.walking_speed = 550
        self.jumping_speed = 5.00

        self.onGround = False

        self.x = init_x
        self.y = init_y
        self.vx = 0
        self.vy = 0
        self.fx = 0
        self.fy = 0

    def update(self, dt, c):
        vx2_c2 = self.vx ** 2 / c ** 2
        vy2_c2 = self.vy ** 2 / c ** 2
        v2_c2 = vx2_c2 + vy2_c2
        gamma = 1.0 / sqrt(1 - v2_c2)
        gamma_x = 1.0 / sqrt(1 - vx2_c2)
        gamma_y = 1.0 / sqrt(1 - vy2_c2)

        theta = atan2(self.vy, self.vx)

        lorentz_y = gamma**1 * cos(theta)**2 + gamma**3 * sin(theta)**2
        lorentz_x = gamma**3 * cos(theta)**2 + gamma**1 * sin(theta)**2
        self.vx += self.fx / (self.mass*lorentz_x) * dt
        self.vy += self.fy / (self.mass*lorentz_y) * dt

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.fx = 0
        self.fy = 0.1 * self.mass  # *lorentz_y # gravity

        drag = 0.01 if self.onGround else 0.10
        self.vx *= (1 - drag * dt)
        self.vy *= (1 - 0.01 * dt)

        self.height = self.proper_height / gamma_y
        self.width = self.proper_width / gamma_x


    def is_dead(self, ground_level):
        return self.get_top() >= ground_level

    def handle_collisions(self, platforms):
        if not self.onGround and self.vy > 0:
            for p in platforms:
                if (p.get_bottom() - p.top)*0.75 >= self.get_bottom() - p.top >= 0:  # above 25% of platform
                    if p.get_right() >= self.get_left() and \
                                    p.get_left() <= self.get_right():  # >= p.left:
                        self.vy *= -self.bounciness
                        self.set_bottom(p.top)
                        self.onGround = True
        else:
            self.onGround = False

    def draw(self, screen):
        image = pygame.transform.scale(self.image, (
            int(self.width), int(self.height)
        ))
        screen.blit(image, (self.get_left(), self.get_top()))

        if settings.is_debugging():
            thickness = 4
            pygame.draw.circle(screen, (100, 100, 100), (int(self.x), int(self.y)), thickness)
            pygame.draw.line(screen, (100, 100, 100),
                             (self.get_left(), self.get_top()), (self.get_right(), self.get_top()), thickness)
            pygame.draw.line(screen, (100, 100, 100),
                             (self.get_left(), self.get_bottom()), (self.get_right(), self.get_bottom()), thickness)
            pygame.draw.line(screen, (100, 100, 100),
                             (self.get_left(), self.get_top()), (self.get_left(), self.get_bottom()), thickness)
            pygame.draw.line(screen, (100, 100, 100),
                             (self.get_right(), self.get_top()), (self.get_right(), self.get_bottom()), thickness)

    def get_left(self):
        return self.x - 0.5*self.width

    def get_right(self):
        return self.x + 0.5*self.width

    def get_top(self):
        return self.y - 0.5*self.height

    def get_bottom(self):
        return self.y + 0.5*self.height

    def set_bottom(self, y):
        self.y = y - 0.5*self.height
