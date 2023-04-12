from typing import List, Dict

from node import Node


class MonopolyTree:
    def __init__(self, root_node):
        self.rootNode = root_node
        self.leafs: List[Node] = []

    def generate_tree(self, depth: int):
        self.generate_subtree(self.rootNode, depth, 0)
        return self.rootNode

    def generate_subtree(self, node: Node, depth: int, current_depth: int) -> None:
        if current_depth == depth:
            self.leafs.append(node)
            return

        next_states: List[Node] = node.get_children()

        if node.current_player.balance <= -500:
            self.leafs.append(node)
            return

        for n in next_states:
            n.round += 1
            self.generate_subtree(n, depth, current_depth + 1)
