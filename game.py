import random

import player
import property
import tree
from node import Node


class Game:
    def __init__(self, players):
        self.players: list[player.Player] = players
        self.current_player = players[0]
        self.turn = 0
        self.properties = []  # Add this line to define the 'board' attribute
        # Add all properties to the board list
        prop1 = property.Property("Boardwalk", 400, 50, 100, 1)
        prop2 = property.Property("Park Place", 350, 35, 70, 2)
        prop3 = property.Property("Baltic Avenue", 60, 4, 20, 3)
        prop4 = property.Property("Mediterranean Avenue", 60, 2, 10, 4)
        self.properties.append(prop1)
        self.properties.append(prop2)
        self.properties.append(prop3)
        self.properties.append(prop4)

        # Add more properties to the board list

    def roll_dice(self):
        die = random.randint(1, 6)
        return die

    def next_player(self):
        index = self.players.index(self.current_player)
        self.current_player = self.players[(index + 1) % len(self.players)]

    def play_game(self):
        root = Node(self.properties, self.players[0], self.players[1], "non-chance", None)
        mono_tree = tree.MonopolyTree(root)
        mono_tree.generate_tree(2)
        Node.Eval(mono_tree)
        temp = root
        print(root.levelOrderTraversal())
