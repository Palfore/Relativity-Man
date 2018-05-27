from src.Game import Game
from src.Menu import menu, instructions, scores

import time
if __name__ == '__main__':
    game_state = 'Main Menu'
    while True:
        if game_state == 'Main Menu':
            game_state = menu()
        elif game_state == 'Instructions':
            game_state = instructions()
        elif game_state == 'Scores':
            game_state = scores()
        elif game_state == 'Time Trial':
            t = time.time()
            game = Game(80, time_this=True, start_time=t)
            response = game.main_loop()
            if response == 'Menu':
                game_state = 'Main Menu'
                continue

            game = Game(8, time_this=True, start_time=t)
            response = game.main_loop()
            if response == 'Menu':
                game_state = 'Main Menu'
                continue

            game = Game(6.5, time_this=True, start_time=t)
            response = game.main_loop()
            if response == 'Menu':
                game_state = 'Main Menu'
                continue

            game_state = scores(time.time()-t)
        elif game_state == 'Endless Play 1':
            game = Game(8, True)
            game.main_loop()
            game_state = 'Main Menu'
        elif game_state == 'Endless Play 2':
            game = Game(6.5, True)
            game.main_loop()
            game_state = 'Main Menu'
        else:
            print("Error: Could not determine game state.")
            exit(0)

