import pygame
import src.settings as settings


class Player:
    def __init__(self, init_x, init_y):
        self.image = pygame.image.load("../assets/einstein.png")
        self.height = 75
        self.width = 75
        self.onGround = False

        self.bounciness = 0.4
        self.walking_speed = 200
        self.jumping_speed = 7
        self.mass = 1

        self.x = init_x
        self.y = init_y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

    def update(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.ax = 0
        self.ay = 0.05
        drag = 0.01 if self.onGround else 0.05
        self.vx *= (1 - drag * dt)
        self.vy *= (1 - 0.01 * dt)

    def is_dead(self, ground_level):
        return self.get_top() >= ground_level

    def handle_collisions(self, platforms):
        if not self.onGround and self.vy > 0:
            for p in platforms:
                if p.top + 2 >= self.get_bottom() >= p.top:
                    if p.get_right() >= self.get_left() and \
                                    p.get_left() <= self.get_right():  # >= p.left:
                        self.vy *= -self.bounciness
                        self.set_bottom(p.top)
                        self.onGround = True
        else:
            self.onGround = False


    def draw(self, screen):
        image = pygame.transform.scale(self.image, (self.height, self.width))
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
