import pygame
from src.settings import using_joy_stick

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 750


class Key:
    def __init__(self, py_key, state=False):
        self.py_key = py_key
        self.state = state


def scores(time_string=''):
    def update_key_states():
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                    if e.key == 27:  # Esc
                        pygame.quit()
                        exit(0)
                    if e.key == 8:  # backspace
                        return 'Main Menu'

                    if 122 >= e.key >= 97 or e.key == 32:
                        return pygame.key.name(e.key)
                    if e.key == 13:
                        return -2
        return -1
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Relativity Man")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)

    times = []
    for line in open('../assets/scores.dat', 'r'):
        if line.strip() == '':
            continue
        time_and_maybe_name = line.split(' ', 1)
        time = float(time_and_maybe_name[0])
        name = ' '
        if len(time_and_maybe_name) > 1:
            name = time_and_maybe_name[1].strip()
        times.append((time, name))
    times = sorted(times, key=lambda x: x[0])

    name = " "
    finished_name = False
    while True:
        screen.fill(0)

        title_font = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = title_font.render("High Scores", False, (100, 100, 100))
        screen.blit(textsurface, (WINDOW_WIDTH / 2.0 - 200, 50))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("Here are all the top scores:", False, (100, 100, 100))
        screen.blit(textsurface, (800, 100))

        if time_string:
            textsurface = title_font.render("Your time was {0:.2f}, please enter your name:".format(time_string), False, (100, 100, 100))
            screen.blit(textsurface, (200, 200))

            textsurface = title_font.render("Name: {0}".format(name), False, (100, 100, 100))
            screen.blit(textsurface, (250, 250))

        for i, time in enumerate(times):
            textsurface = title_font.render(str(time[0]) + "s : " + str(time[1]), False, (100, 100, 100))
            screen.blit(textsurface, (850, 150 + 50*i))

        key_states = update_key_states()
        if (not time_string) or finished_name:  # can only exit if just looking, or name is finished
            if key_states == 'Main Menu':
                if time_string:
                    f = open('../assets/scores.dat', 'a')
                    f.write("{0:.3f}".format(time_string) + " " + name + '\n')
                    f.close()
                return key_states
        if not finished_name and not any([key_states == s for s in [-1, -2, "Main Menu"]]):
            name += key_states if key_states != 'space' else ' '
        if key_states == -2:
            finished_name = True

        pygame.display.flip()


def instructions():
    def update_key_states():
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                    print(e.key)
                    if e.key == 27:  # Esc
                        pygame.quit()
                        exit(0)
                    if e.key == 8:  # backspace
                        return 'Main Menu'
        return -1
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Relativity Man")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
    while True:
        screen.fill(0)

        title_font = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = title_font.render("Instructions", False, (100, 100, 100))
        screen.blit(textsurface, (WINDOW_WIDTH / 2.0 - 200, 50))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("You play as Einstein as he tries to collect Nobel Prizes.", False, (100, 100, 100))
        screen.blit(textsurface, (200, 100))
        title_font = pygame.font.SysFont('Comic Sans MS', 25)

        textsurface = title_font.render("You can use 'a' and 'd' to move left and right, respectively,"+
                                        " and spacebar to jump.", False, (100, 100, 100))
        screen.blit(textsurface, (200, 150))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("In the Time Trial move, you will progress through 3 levels,", False, (100, 100, 100))
        screen.blit(textsurface, (200, 200))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("and each one will decrease the speed of light, so you will notice the effects of relativity more.", False, (100, 100, 100))
        screen.blit(textsurface, (200, 250))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("You're time to complete the 3 levels will be recorded and shown in the High Scores.", False, (100, 100, 100))
        screen.blit(textsurface, (200, 300))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("In Endless Play mode, you can explore motion at a set speed as much as you like.", False, (100, 100, 100))
        screen.blit(textsurface, (200, 350))


        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("Go Back (Backspace)", False, (100, 100, 100))
        screen.blit(textsurface, (250, 450))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("Exit (Esc)", False, (100, 100, 100))
        screen.blit(textsurface, (700, 450))


        key_states = update_key_states()
        if key_states != -1:
            return key_states

        pygame.display.flip()




def menu():
    def update_key_states():
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                    print(e.key)
                    if e.key == 27:  # Esc
                        pygame.quit()
                        exit(0)
                    if e.key == 49:  # p
                        return 'Time Trial'
                    if e.key == 50:  # p
                        return 'Endless Play 1'
                    if e.key == 51:  # p
                        return 'Endless Play 2'
                    if e.key == 105:  # i
                        return 'Instructions'
                    if e.key == 115:  # s
                        return 'Scores'
        return -1
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Relativity Man")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
    while True:
        screen.fill(0)

        title_font = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = title_font.render("Welcome to Relativity Man", False, (100, 100, 100))
        screen.blit(textsurface, (WINDOW_WIDTH / 2.0 - 200, 50))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("What would you like to do?", False, (100, 100, 100))
        screen.blit(textsurface, (200, 100))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("Time Trial (1)", False, (100, 100, 100))
        screen.blit(textsurface, (250, 150))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("Endless Play at 0.67c (2)", False, (100, 100, 100))
        screen.blit(textsurface, (250, 200))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("Endless Play at 0.88c (3)", False, (100, 100, 100))
        screen.blit(textsurface, (250, 250))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("Instructions (i)", False, (100, 100, 100))
        screen.blit(textsurface, (250, 300))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("High Scores (s)", False, (100, 100, 100))
        screen.blit(textsurface, (250, 350))

        title_font = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = title_font.render("Exit (Esc)", False, (100, 100, 100))
        screen.blit(textsurface, (250, 400))

        textsurface = title_font.render("Backspace will bring you back to the menu at any point.", False, (100, 100, 100))
        screen.blit(textsurface, (300, 500))

        key_states = update_key_states()
        if key_states != -1:
            return key_states

        pygame.display.flip()


