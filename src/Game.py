import pygame
from src.Player import Player
from src.Platform import Platform
from src.Clock import Clock
import copy

class Key:
    def __init__(self, py_key, state=False):
        self.py_key = py_key
        self.state = state


class Game:
    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 750
    GROUND = WINDOW_HEIGHT
    DT = 0.01
    SPEED_OF_LIGHT = 8

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Relativity Man")
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.player = Player(150, Game.GROUND - 300)
        self.platforms = (Platform(self.GROUND - 100, 100, 1600, 10),
                          Platform(self.GROUND - 200, 200, 200, 10),
                          Platform(self.GROUND - 500, 500, 200, 10),
                          Platform(self.GROUND - 400, 300, 200, 10),
                          Platform(self.GROUND - 300, 700, 200, 10),
                          )
        self.clock_rel = Clock(50, 50, 200, 100, self.SPEED_OF_LIGHT)
        self.clock = Clock(150, 50, 200, 100, self.SPEED_OF_LIGHT)
        self.keys = {}  # Automatically initialized in handle user input.

    def main_loop(self):
        clock = pygame.time.Clock()
        max_speed = 0
        while True:
            self.clear_scene()

            self.player.draw(self.screen)
            for platform in self.platforms:
                platform.draw(self.screen)
            self.clock.draw(self.screen)
            self.clock_rel.draw(self.screen)
            clock_rel_copy = copy.deepcopy(self.clock_rel)
            clock_rel_copy.x = self.player.x
            clock_rel_copy.y = self.player.y - self.player.height - 50
            clock_rel_copy.draw(self.screen)

            speed = (self.player.vx ** 2 + self.player.vy ** 2) ** 0.5 / self.SPEED_OF_LIGHT * 100
            myfont = pygame.font.SysFont('Comic Sans MS', 30)
            textsurface = myfont.render('{:.2f}'.format(speed), False, (100, 100, 100))
            self.screen.blit(textsurface, (500, 500))

            self.show_scene()


            clock.tick(60)
            for frames in range(300):
                self.update_key_states()
                self.player.update(self.DT)
                self.player.handle_collisions(self.platforms)
                self.clock.update(self.DT, 0, 0, self.SPEED_OF_LIGHT)
                self.clock_rel.update(self.DT, self.player.vx, self.player.vy, self.SPEED_OF_LIGHT)
                self.handle_user_input()
                if self.player.is_dead(self.GROUND):
                    self.player = Player(150, Game.GROUND - 300)

    def update_key_states(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if e.type == pygame.KEYDOWN:
                for char, key_object in self.keys.items():
                    if e.key == key_object.py_key:
                        self.keys[char] = Key(key_object.py_key, True)
            if e.type == pygame.KEYUP:
                for char, key_object in self.keys.items():
                    if e.key == key_object.py_key:
                        self.keys[char] = Key(key_object.py_key, False)

    def handle_user_input(self):
        """ To add a new key function, just add it in this if else block. It will
            be automatically added in the exception. Keys should be named according to:
            https://www.pygame.org/docs/ref/key.html under the 'Common Name' column. """
        try:
            if self.keys['a'].state:
                self.player.vx = -self.player.walking_speed * self.DT
            if self.keys['d'].state:
                self.player.vx = +self.player.walking_speed * self.DT
            if self.keys['space'].state:
                if self.player.onGround:
                    self.player.vy = -self.player.jumping_speed
                    self.keys['space'].state = False
            if self.keys['escape'].state:
                pygame.quit()
                exit(0)
        except KeyError as e:
            ''' If it can't access a key (exception thrown), it will add the key automatically. '''
            invalid_key = str(e).strip("'")
            num_keys_possible = 133
            for i in range(num_keys_possible):
                if pygame.key.name(i) == invalid_key:
                    self.keys[invalid_key] = Key(i, False)
                    break

    @staticmethod
    def show_scene():
        pygame.display.flip()

    def clear_scene(self):
        self.screen.fill(0)

