# create players
import copy
import random

import game
import player

player_zero = player.Player(0)
player_one = player.Player(1)

# roll dies in start
dies_zero = random.randint(1, 6)


# set position
player_zero.position = dies_zero
print(f"player zero got {dies_zero}")

# create game and add players
game = game.Game([player_zero, player_one])

game.play_game()
