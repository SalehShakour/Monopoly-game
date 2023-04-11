# create players
import copy

from game import Game
from player import Player
from property import Property

player1 = Player(0)
player2 = Player(1)

# create properties


# create game and add players and properties
game = Game([player1, player2])

game.play_game()