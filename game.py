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
        self.properties = property.properties  # Add this line to define the 'board' attribute
        # Add all properties to the board list
        # prop1 = property.Property("Boardwalk", 400, 50, 100, 1)
        # prop2 = property.Property("Park Place", 350, 35, 70, 2)
        # prop3 = property.Property("Baltic Avenue", 60, 4, 20, 3)
        # prop4 = property.Property("Mediterranean Avenue", 60, 2, 10, 4)
        # self.properties.append(prop1)
        # self.properties.append(prop2)
        # self.properties.append(prop3)
        # self.properties.append(prop4)

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
        mono_tree.generate_tree(8)
        Node.Eval(mono_tree)

        current_node = root
        while True:
            if current_node.current_player.balance > 2000 or current_node.second_player.balance == 0:
                print(f"player {current_node.current_player.ID} win !")
                break
            elif current_node.current_player.balance < -500 or current_node.second_player.balance == 0:
                print(f"player {current_node.second_player.ID} win !")
                break

            if len(current_node.action) == 0:
                mono_tree = tree.MonopolyTree(current_node)
                mono_tree.generate_tree(8)
                Node.Eval(mono_tree)
            if current_node.node_type == "chance":
                dice = self.roll_dice()
                name = "zero" if current_node.current_player.ID == 0 else "one"
                print(f"player {name} got {dice}")
                current_node = current_node.action[dice - 1][1]
            else:
                if current_node.current_player.ID == 0:
                    current_node.action.sort(key=lambda tup: tup[1].zero_value, reverse=True)
                    print(
                        f"zero {current_node.action[0][0]} ( position: {current_node.properties[current_node.current_player.position].name} ) (cash:{current_node.current_player.balance})")
                    current_node = current_node.action[0][1]

                else:
                    current_node.action.sort(key=lambda tup: tup[1].one_value, reverse=True)
                    print(
                        f"one {current_node.action[0][0]} ( position: {current_node.properties[current_node.current_player.position].name} ) (cash:{current_node.current_player.balance})")
                    current_node = current_node.action[0][1]
