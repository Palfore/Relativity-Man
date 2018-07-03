import pygame
from Player import Player
from Platform import Platform
from Clock import Clock, Ball
from settings import using_joy_stick
import copy
from math import atan2, cos, sin, sqrt

class Key:
    def __init__(self, py_key, state=False):
        self.py_key = py_key
        self.state = state


class Nobel_Prize:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 100
        self.width = 100
        self.image = pygame.transform.scale(pygame.image.load("assets/Nobel_Prize.png"), (
            int(self.height), int(self.width)
        ))
        self.hidden = False
        self.time_held_for = -1

    def in_prize(self, x, y):
        return (x-self.x)**2 + (y-self.y)**2 <= (self.height**2 + self.width**2)*0.5

    def draw(self, screen):
        if not self.hidden:
            screen.blit(self.image, (self.x, self.y))

import time
class Game:
    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 750
    GROUND = WINDOW_HEIGHT
    DT = 0.01

    def __init__(self, c, is_last_level=False, time_this=False, start_time=time.time()):
        self.time_this = time_this
        self.start_time = start_time
        self.jump_sound = None
        self.is_last_level = is_last_level
        self.SPEED_OF_LIGHT = c  # 80 -> 8 -> 5.5
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Relativity Man")
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.FULLSCREEN)

        self.player = Player(150, Game.GROUND - 300)
        thickness = 25
        self.platforms = (Platform(self.GROUND - 100, 100, 1600, 2*thickness),
                          Platform(self.GROUND - 200, 200,  200, thickness),
                          Platform(self.GROUND - 500, 500,  200, thickness),
                          Platform(self.GROUND - 400, 300,  200, thickness),
                          Platform(self.GROUND - 300, 700,  200, thickness),
                          )
        self.clock_rel = Clock(50, 100, 200, 100, self.SPEED_OF_LIGHT)
        self.clock = Clock(160, 100, 200, 100, self.SPEED_OF_LIGHT)
        self.keys = {}  # Automatically initialized in handle user input.

        self.ball = Ball(50, 50, 0)

    def main_loop(self):
        clock = pygame.time.Clock()

        prize = Nobel_Prize(550, 100)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        if not self.jump_sound:
            self.jump_sound = pygame.mixer.Sound('assets/jump.wav')
        while True:
            try:
                self.clear_scene()

                prize.draw(self.screen)

                if not prize.hidden:
                    if prize.in_prize(self.player.x, self.player.y):
                        prize.hidden = True
                        prize_sound = pygame.mixer.Sound('assets/powerup.wav')
                        prize_sound.play()
                else:
                    textsurface = myfont.render("Congratulations! You got Einstein a Nobel Prize!", False, (100, 100, 100))
                    self.screen.blit(textsurface, (self.WINDOW_WIDTH / 2.0 - 200, 50))
                    prize.time_held_for += 1
                    if prize.time_held_for > 200:
                        if not self.is_last_level:
                            return 'Next Level'
                        else:
                            prize.hidden = False
                            prize.time_held_for = -1


                textsurface = myfont.render("Einstein", False, (100, 100, 100))
                self.screen.blit(textsurface, (0, 200))
                textsurface = myfont.render("Lab", False, (100, 100, 100))
                self.screen.blit(textsurface, (130, 200))

                if self.time_this:
                    textsurface = myfont.render("Time: {0:.2f}".format((time.time() - self.start_time)), False, (100, 100, 100))
                    self.screen.blit(textsurface, (Game.WINDOW_WIDTH * 0.9, Game.WINDOW_HEIGHT * 0.8))


                self.player.draw(self.screen)
                for platform in self.platforms:
                    platform.draw(self.screen)
                self.clock.draw(self.screen)
                self.clock_rel.draw(self.screen)

                clock_rel_copy = copy.deepcopy(self.clock_rel)
                clock_rel_copy.x = self.player.x
                clock_rel_copy.y = self.player.y - self.player.height - 50
                clock_rel_copy.draw(self.screen)


                vx2_c2 = self.player.vx ** 2 / self.SPEED_OF_LIGHT ** 2
                vy2_c2 = self.player.vy ** 2 / self.SPEED_OF_LIGHT ** 2
                v2_c2 = vx2_c2 + vy2_c2
                theta = atan2(self.player.vy, self.player.vx)
                gamma = 1.0 / sqrt(1 - v2_c2)
                lorentz_y = gamma ** 1 * cos(theta) ** 2 + gamma ** 3 * sin(theta) ** 2
                lorentz_x = gamma ** 3 * cos(theta) ** 2 + gamma ** 1 * sin(theta) ** 2

                speed = (self.player.vx ** 2 + self.player.vy ** 2) ** 0.5 / self.SPEED_OF_LIGHT * 100

                textsurface = myfont.render('v  = {:.2f}% c'.format(speed), False, (100, 100, 100))
                self.screen.blit(textsurface, (self.WINDOW_WIDTH - 200, 50))

                textsurface = myfont.render('m_x = {:.2f}'.format(lorentz_x), False, (100, 100, 100))
                self.screen.blit(textsurface, (self.WINDOW_WIDTH - 200, 100))

                textsurface = myfont.render('m_y = {:.2f}'.format(lorentz_y), False, (100, 100, 100))
                self.screen.blit(textsurface, (self.WINDOW_WIDTH - 200, 150))

                textsurface = myfont.render('Walking Speed = {:.1f}%c'.format(self.player.walking_speed / self.SPEED_OF_LIGHT), False, (100, 100, 100))
                self.screen.blit(textsurface, (300, 0))


                self.show_scene()

                clock.tick(60)
                for frames in range(300):
                    try:
                        if self.keys['space'].state:
                            if self.player.onGround:
                                # self.jump_sound.play()
                                pass
                    except:
                        pass
                    player_wants_to_return = self.update_key_states()
                    if player_wants_to_return:
                        return 'Menu'
                    self.handle_user_input()


                    self.player.update(self.DT, self.SPEED_OF_LIGHT)
                    self.player.handle_collisions(self.platforms)
                    self.clock.update(self.DT, 0, 0, self.SPEED_OF_LIGHT)
                    self.clock_rel.update(self.DT, self.player.vx, self.player.vy, self.SPEED_OF_LIGHT)

                    if self.player.is_dead(self.GROUND):
                        self.player = Player(150, Game.GROUND - 300)
            except ValueError:
                self.player.x = 150
                self.player.y = Game.GROUND - 300
                self.player.vx = 0
                self.player.vy = 0
                print("Crashed: [Slightly] Exceeded the speed of light (its a bug).")

    def update_key_states(self):
        if using_joy_stick() and pygame.joystick.get_count():
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            jump_button = joystick.get_button(0)
            d_pressed = joystick.get_hat(0)[0] > 0
            a_pressed = joystick.get_hat(0)[0] < 0

            for char, key_object in self.keys.items():
                if char == 'space':
                    self.keys[char] = Key(key_object.py_key, jump_button)
                if char == 'a':
                    self.keys[char] = Key(key_object.py_key, a_pressed)
                if char == 'd':
                    self.keys[char] = Key(key_object.py_key, d_pressed)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if e.type == pygame.KEYDOWN:
                for char, key_object in self.keys.items():
                    if e.key == 8:
                        return True
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
                self.player.fx = -(self.player.walking_speed + self.player.vx/self.DT) * self.player.mass
            if self.keys['d'].state:
                self.player.fx = -(-self.player.walking_speed + self.player.vx / self.DT) * self.player.mass
            if self.keys['space'].state:
                if self.player.onGround:
                    self.jump_sound.play()
                    # self.player.vy = -self.player.jumping_speed
                    self.player.fy = -self.player.jumping_speed / 0.01
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

