import collections
import copy


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
        heuristic_one = 0
        heuristic_zero = 0
        property_value_zero = sum(
            prop.value for prop in zero.properties)
        rent_earned_zero = sum(
            prop.rent for prop in zero.properties)

        property_value_one = sum(prop.value for prop in one.properties)
        # calculate the total rent earned by player from properties
        rent_earned_one = sum(prop.rent for prop in one.properties)

        self.zero_value = heuristic_zero + property_value_zero + 10 * rent_earned_zero + zero.balance
        self.one_value = heuristic_one + property_value_one + 10 * rent_earned_one + one.balance

        if zero.balance < 200:
            self.zero_value = heuristic_zero + property_value_zero + 10 * rent_earned_zero + 10000 * zero.balance
        if one.balance < 200:
            self.one_value = heuristic_one + property_value_one + 10 * rent_earned_one + 10000 * one.balance
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

                new_node = Node(cp_properties, cp_current_player, cp_second_player, node_type="non-chance", parent=self)
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
            if cp_properties_sell[cp_current_player_sell.position].owner == cp_current_player_sell.ID:
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
                new_node = Node(cp_properties_rent, cp_second_player_rent, cp_current_player_rent, node_type="chance",
                                parent=self)
                self.action.append(("rent", new_node))
                self.children.append(new_node)

            # do nothing
            cp_properties_nothing = copy.deepcopy(self.properties)
            cp_current_player_nothing = copy.deepcopy(self.current_player)
            cp_second_player_nothing = copy.deepcopy(self.second_player)
            if cp_properties_nothing[cp_current_player_nothing.position].owner != (cp_current_player_rent.ID + 1) % 2:
                new_node = Node(cp_properties_nothing, cp_second_player_nothing, cp_current_player_nothing,
                                node_type="chance", parent=self)
                self.action.append(("nothing", new_node))
                self.children.append(new_node)

        return self.children
