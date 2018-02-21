import pygame
from src.Player import Player
from src.Platform import Platform


class Key:
    def __init__(self, py_key, state=False):
        self.py_key = py_key
        self.state = state


class Game:
    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 750
    GROUND = WINDOW_HEIGHT
    DT = 0.01

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Relativity Man")
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.player = Player(150, Game.GROUND - 300)
        self.platforms = (Platform(self.GROUND - 100, 100, 200, 10),
                          Platform(self.GROUND - 200, 200, 200, 10),
                          Platform(self.GROUND - 500, 500, 200, 10),
                          Platform(self.GROUND - 400, 300, 200, 10),
                          Platform(self.GROUND - 300, 700, 200, 10),
                          )
        self.keys = {}  # Automatically initialized in handle user input.

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            self.clear_scene()

            self.player.draw(self.screen)
            for platform in self.platforms:
                platform.draw(self.screen)
            self.show_scene()

            clock.tick(60)
            for frames in range(300):
                self.update_key_states()
                self.player.update(self.DT)
                self.player.handle_collisions(self.platforms)
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

