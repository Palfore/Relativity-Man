from src.Game import Game

from cmath import sqrt, sin, exp, cos, pi, asin, atan, log


if __name__ == '__main__':
    game = Game(80)
    game.main_loop()

    game = Game(8)
    game.main_loop()

    game = Game(6.5)
    game.main_loop()

    game = Game(8, True)
    game.main_loop()


