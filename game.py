import random

from node import Node
from player import Player
from property import Property
from tree import MonopolyTree


class Game:
    def __init__(self, players):
        self.players: list[Player] = players
        self.current_player = players[0]
        self.turn = 0
        self.properties = []  # Add this line to define the 'board' attribute
        # Add all properties to the board list
        prop1 = Property("Boardwalk", 400, 50, 100, 1)
        prop2 = Property("Park Place", 350, 35, 70, 2)
        prop3 = Property("Baltic Avenue", 60, 4, 20, 3)
        prop4 = Property("Mediterranean Avenue", 60, 2, 10, 4)
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
        root = Node(self.properties, self.players[0], self.players[1], "max", "chance", "chance")
        mono_tree = MonopolyTree(root)
        mono_tree.generate_tree(3)
        dep = 0
        print(root.action, "turn:", root.current_player.ID)
        for c in root.children:
            print(c.action, "turn:", c.current_player.ID)

            for j in c.children:
                print(j.action, "turn:", j.current_player.ID)
            print("------------")










    # def ExpectiMiniMax(self, node: Node, Depth, currentplayer: int):
    #     bestmove = None
    #     if Depth == 0:
    #         return bestmove, self.EvalFunc(node)
    #
    #     if node.current_player.player_type == "max":
    #         max_value = float('-inf')
    #         for successor in node.get_children():
    #             bestmove, value = self.ExpectiMiniMax(successor, Depth - 1, self.getNextPlayer(currentplayer))
    #             if value > max_value:
    #                 bestmove = successor
    #                 max_value = value
    #         return bestmove, max_value
    #
    #     elif node.node_type == "chance":
    #         ExpectedValue = 0
    #         for successor in node.get_successors("chance"):
    #             bestmove, value = ExpectiMiniMax(successor, Depth - 1, self.GetNextPlayer(currentplayer))
    #             ExpectedValue += value * successor.Probability()
    #
    #         return bestmove, ExpectedValue
    #     # for min player
    #     else:
    #         min_value = float('inf')
    #         for successor in node.get_successors("min"):
    #             bestmove, value = ExpectiMiniMax(successor, Depth - 1, self.getNextPlayer(currentplayer))
    #             if value < min_value:
    #                 bestmove = successor
    #                 min_value = value
    #         return bestmove, min_value
    #
    # def EvalFunc(self, node):
    #     pass
    #
    # def getNextPlayer(self, currentplayer):
    #     if self.players[currentplayer].player_type
