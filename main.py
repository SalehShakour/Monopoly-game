# create players
import copy

import game
import player

player1 = player.Player(0)
player2 = player.Player(1,position=1)

# create properties


# create game and add players and properties
game = game.Game([player1, player2])

game.play_game()
