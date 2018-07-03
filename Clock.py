import pygame


class Ball:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = c
        self.r = 5

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt


class ExceededSpeedOfLight(Exception):
    def __init__(self):
        super().__init__("EXCEEDED SPEED OF LIGHT")


class Clock:
    def __init__(self, x, y, height, width, c):
        self.x = x
        self.y = y
        self.ball = Ball(0, 0, c)
        self.height = height
        self.width = width

    # def draw(self, screen):
    #     thickness = 4
    #     pygame.draw.line(screen, (100, 100, 100),
    #                      (self.get_left(), self.get_top()), (self.get_right(), self.get_top()), thickness)
    #     pygame.draw.line(screen, (100, 100, 100),
    #                      (self.get_left(), self.get_bottom()), (self.get_right(), self.get_bottom()), thickness)
    #
    #     pygame.draw.circle(screen, (100, 100, 100), (int(self.ball.x), int(self.ball.y)), int(self.ball.r))

    def draw(self, screen, x=None, y=None):
        if x is None or y is None:
            x = self.x
            y = self.y
        thickness = 4
        left = x - 0.5*self.width
        right = x + 0.5 * self.width
        top = y + 0.5 * self.height
        bottom = y - 0.5 * self.height

        pygame.draw.line(screen, (100, 100, 100),
                         (left, top), (right, top), thickness)
        pygame.draw.line(screen, (100, 100, 100),
                         (left, bottom), (right, bottom), thickness)

        pygame.draw.circle(screen, (100, 100, 100),
                           (int(self.x + self.ball.x), int(self.y + self.ball.y)),
                           int(self.ball.r))

    def update(self, dt, vx, vy, c):
        if not self.get_left() + self.ball.r <= self.x + self.ball.x <= self.get_right() - self.ball.r:
            self.ball.vx *= -1
        if not self.get_bottom() + self.ball.r <= self.y + self.ball.y <= self.get_top() - self.ball.r:
            self.ball.vy *= -1

        # discriminant = 1.0 - ((vx+self.ball.vx)**2+(vy+self.ball.vy)**2)/c**2
        # discriminant = 1.0 - ((vx)**2+(vy)**2)/c**2
        # if discriminant < 0:
        #     raise ExceededSpeedOfLight
        # dt *= discriminant**0.5

        v = (vx**2 + vy**2)**0.5
        # v -> c - v (but keep same sign)
        self.ball.vy = self.ball.vy / float(abs(self.ball.vy)) * (c - v)
        self.ball.update(dt)

    def get_left(self):
        return self.x - 0.5*self.width

    def get_right(self):
        return self.x + 0.5 * self.width

    def get_top(self):
        return self.y + 0.5 * self.height

    def get_bottom(self):
        return self.y - 0.5 * self.height
