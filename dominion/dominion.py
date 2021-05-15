from game import Game
import os

if __name__ == '__main__':
    game = Game()
    os.system('cls||clear')
    print(game, '\n')

    while True:
        val = input("Play a new game (Y/n)?")
        if val in ['', 'y', 'Y']:
            os.system('cls||clear')
            game.next_game()
            print(game, '\n')
        elif val in ['n', 'N']:
            break
