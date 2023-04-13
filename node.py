import collections
import copy
import sys


class Node:
    def __init__(self, properties, current_player, second_player, node_type, parent):
        self.current_player = current_player
        self.second_player = second_player
        self.properties = properties
        self.node_type = node_type
        self.children: list[Node] = []
        self.parent: Node = parent
        self.action = []
        self.zero_value = 0
        self.one_value = 0
        self.round = 0

    def utility(self):
        one = self.second_player if self.second_player.ID == 1 else self.current_player
        zero = self.current_player if self.current_player.ID == 0 else self.second_player
        total_cash = one.balance + zero.balance
        total_cash_gain_zero = zero.balance - 1500
        total_cash_gain_one = one.balance - 1500
        if self.round == 0 or total_cash == 0:
            avg_cash_per_round = 0
        else:
            avg_cash_per_round = ((total_cash_gain_one + total_cash_gain_zero) / 2) / self.round

        PctDiff = 100 * abs(one.balance - zero.balance) / total_cash
        if avg_cash_per_round == 0:
            num_turns_left = -1
        else:
            num_turns_left = (total_cash / avg_cash_per_round) * (1 - PctDiff / 100) - 400

        if num_turns_left == 0:
            if self.current_player.balance == 0:
                print(f"player with id={self.second_player.ID} win ! (Remaining cash ={self.second_player.balance})")
            else: print(f"player with id={self.current_player.ID} win ! (Remaining cash ={self.current_player.balance})")

            sys.exit(0)

        properties = zero.properties
        cash = zero.balance

        # calculate the total value of player's properties
        property_value = sum(prop.value for prop in properties)

        # calculate the total rent earned by player from properties
        rent_earned = sum(prop.rent for prop in properties)

        # calculate the net worth of the player
        net_worth = cash + property_value

        # calculate the number of properties owned by the player
        num_properties = len(properties)

        # calculate the number of turns left in the game

        # calculate the average rent earned by the player per turn
        avg_rent_per_turn = rent_earned / (2 * num_turns_left)

        # calculate the heuristic value of the player
        heuristic_value = net_worth + avg_rent_per_turn * num_properties

        self.zero_value = 1500 - heuristic_value
        # --------------
        properties = one.properties
        cash = one.balance
        property_value = sum(prop.value for prop in properties)
        rent_earned = sum(prop.rent for prop in properties)
        net_worth = cash + property_value
        num_properties = len(properties)
        avg_rent_per_turn = rent_earned / (2 * num_turns_left)
        heuristic_value = net_worth + avg_rent_per_turn * num_properties
        self.one_value = 1500 - heuristic_value

        return self.zero_value, self.one_value

    @staticmethod
    def Eval(tree):
        for node in tree.leafs:
            node.utility()
        parent_nodes = set(i.parent for i in tree.leafs)
        while len(parent_nodes) > 0:

            new_parent_node: set[Node] = set()
            for node in parent_nodes:
                if node.node_type == "chance":
                    for child in node.children:
                        node.zero_value += child.zero_value / 6
                        node.one_value += child.one_value / 6

                else:
                    node.zero_value = float('-inf')
                    node.one_value = float('-inf')
                    for child in node.children:
                        node.zero_value = max(node.zero_value, child.zero_value)
                        node.one_value = max(node.one_value, child.one_value)
                        new_parent_node.add(child)

            parent_nodes = set(i.parent for i in parent_nodes)
            if len(parent_nodes) == 1 and None in parent_nodes:
                break

    def levelOrderTraversal(self):
        ans = []

        # Return Null if the tree is empty
        if self is None:
            return ans

        # Initialize queue
        queue: collections.deque[Node] = collections.deque()
        queue.append(self)

        # Iterate over the queue until it's empty
        while queue:
            # Check the length of queue
            currSize = len(queue)
            currList = []

            while currSize > 0:
                # Dequeue element
                currNode = queue.popleft()
                currList.append(currNode)
                currSize -= 1

                # Check for left child
                for node in currNode.children:
                    if node is not None:
                        queue.append(node)

            # Append the currList to answer after each iteration
            ans.append(currList)

        # Return answer list
        return ans

    def get_children(self):
        if self.node_type == "chance":
            for i in range(1, 7):
                cp_properties = copy.deepcopy(self.properties)
                cp_current_player = copy.deepcopy(self.current_player)
                cp_second_player = copy.deepcopy(self.second_player)
                cp_current_player.position = (cp_current_player.position + i) % len(cp_properties)

                new_node = Node(cp_properties, cp_current_player, cp_second_player, node_type="not-chance", parent=self)
                self.action.append((i, new_node))
                self.children.append(new_node)

        else:
            # buy
            cp_properties_buy = copy.deepcopy(self.properties)
            cp_current_player_buy = copy.deepcopy(self.current_player)
            cp_second_player_buy = copy.deepcopy(self.second_player)
            if cp_properties_buy[cp_current_player_buy.position].owner is None and cp_current_player_buy.balance >= \
                    cp_properties_buy[cp_current_player_buy.position].value:
                cp_current_player_buy.buy(cp_properties_buy[cp_current_player_buy.position])

                new_node = Node(cp_properties_buy, cp_second_player_buy, cp_current_player_buy, node_type="chance",
                                parent=self)
                self.action.append(("buy", new_node))

                self.children.append(new_node)

            # sell
            cp_properties_sell = copy.deepcopy(self.properties)
            cp_current_player_sell = copy.deepcopy(self.current_player)
            cp_second_player_sell = copy.deepcopy(self.second_player)
            if cp_properties_sell[cp_current_player_sell.position] in cp_current_player_sell.properties:
                cp_current_player_sell.sell(cp_properties_sell[cp_current_player_sell.position])

                new_node = Node(cp_properties_sell, cp_second_player_sell, cp_current_player_sell, node_type="chance",
                                parent=self)
                self.action.append(("sell", new_node))
                self.children.append(new_node)

            # rent
            cp_properties_rent = copy.deepcopy(self.properties)
            cp_current_player_rent = copy.deepcopy(self.current_player)
            cp_second_player_rent = copy.deepcopy(self.second_player)
            if cp_properties_rent[cp_current_player_rent.position].owner == (cp_current_player_rent.ID + 1) % 2:
                cp_current_player_rent.pay_rent(cp_properties_rent[cp_current_player_rent.position].rent,
                                                cp_second_player_rent)
                new_node = Node(cp_properties_sell, cp_second_player_sell, cp_current_player_sell, node_type="chance",
                                parent=self)
                self.action.append(("rent", new_node))
                self.children.append(new_node)

            # do nothing
            cp_properties_nothing = copy.deepcopy(self.properties)
            cp_current_player_nothing = copy.deepcopy(self.current_player)
            cp_second_player_nothing = copy.deepcopy(self.second_player)

            new_node = Node(cp_properties_nothing, cp_second_player_nothing, cp_current_player_nothing,
                            node_type="chance", parent=self)
            self.action.append(("nothing", new_node))
            self.children.append(new_node)

        return self.children
