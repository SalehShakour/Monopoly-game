import copy

import player
import property


class Node:
    def __init__(self, properties, current_player: player.Player, second_player: player.Player, node_type, next_type,
                 previous_type):
        self.current_player = current_player
        self.second_player = second_player
        self.properties = properties
        self.node_type = node_type
        self.children: list[Node] = []
        self.next_type: str = next_type
        self.previous_type = previous_type
        self.action = None
        self.zero_value = 0
        self.one_value = 0

    def utility(self):
        one = self.second_player if self.second_player.ID == 1 else self.current_player
        zero = self.current_player if self.current_player.ID == 0 else self.second_player

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

        num_turns_left = (one.balance - rent_earned + 500) / rent_earned

        # calculate the average rent earned by the player per turn
        avg_rent_per_turn = rent_earned / (2 * num_turns_left)

        # calculate the heuristic value of the player
        heuristic_value = net_worth + avg_rent_per_turn * num_properties

        self.zero_value = heuristic_value
        #--------------
        properties = one.properties
        cash = one.balance
        property_value = sum(prop.value for prop in properties)
        rent_earned = sum(prop.rent for prop in properties)
        net_worth = cash + property_value
        num_properties = len(properties)
        num_turns_left = (zero.balance - rent_earned + 500) / rent_earned
        avg_rent_per_turn = rent_earned / (2 * num_turns_left)
        heuristic_value = net_worth + avg_rent_per_turn * num_properties
        self.one_value = heuristic_value

        return self.zero_value, self.one_value


    def eval(self):
        if len(self.children) == 0:
            self.utility()
        else:
            if self.node_type == "chance":
                for child in self.children:
                    self.zero_value += child.zero_value / 6
                    self.one_value += child.one_value / 6
            else:
                if self.node_type == "min":


    def get_children(self):
        if self.node_type == "chance":
            for i in range(1, 7):
                cp_properties = copy.deepcopy(self.properties)
                cp_current_player = copy.deepcopy(self.current_player)
                cp_second_player = copy.deepcopy(self.second_player) # max
                cp_current_player.position = (cp_current_player.position + i) % len(cp_properties)
                if self.previous_type == "max":
                    t = "min"
                else:
                    t = "max"

                new_node = Node(cp_properties, cp_current_player, cp_second_player,  node_type=self.next_type,
                                next_type=t, previous_type=self.node_type)
                new_node.action = i
                self.children.append(new_node)

        else:
            # buy
            cp_properties_buy: list[property.Property] = copy.deepcopy(self.properties)
            cp_current_player_buy = copy.deepcopy(self.current_player)
            cp_second_player_buy = copy.deepcopy(self.second_player)
            if cp_properties_buy[cp_current_player_buy.position].owner is None and cp_current_player_buy.balance >= \
                    cp_properties_buy[cp_current_player_buy.position].value:
                cp_current_player_buy.buy(cp_properties_buy[cp_current_player_buy.position])
                if self.node_type == "max":
                    t = "min"
                else:
                    t = "max"
                new_node = Node(cp_properties_buy, cp_second_player_buy, cp_current_player_buy, node_type="chance",
                                next_type=t, previous_type=self.node_type)
                new_node.action = f"after buying action of player {cp_current_player_buy.ID}"
                self.children.append(new_node)

            # sell
            cp_properties_sell: list[property.Property] = copy.deepcopy(self.properties)
            cp_current_player_sell = copy.deepcopy(self.current_player)
            cp_second_player_sell = copy.deepcopy(self.second_player)
            if cp_properties_sell[cp_current_player_buy.position].owner == cp_current_player_sell.ID:
                cp_current_player_sell.sell(cp_properties_sell[cp_current_player_sell.position])
                if self.node_type == "max":
                    t = "min"
                else:
                    t = "max"
                new_node = Node(cp_properties_sell, cp_second_player_sell, cp_current_player_sell, node_type="chance",
                                next_type=t, previous_type=self.node_type)
                new_node.action = f"after selling action of player {cp_current_player_buy.ID}"
                self.children.append(new_node)

            # rent
            cp_properties_rent: list[property.Property] = copy.deepcopy(self.properties)
            cp_current_player_rent = copy.deepcopy(self.current_player)
            cp_second_player_rent = copy.deepcopy(self.second_player)
            if cp_properties_rent[cp_current_player_rent.position].owner == (cp_current_player_rent.ID + 1) % 2:
                cp_current_player_rent.pay_rent(cp_properties_rent[cp_current_player_rent.position].rent,
                                                cp_second_player_rent)
                if self.node_type == "max":
                    t = "min"
                else:
                    t = "max"
                new_node = Node(cp_properties_sell, cp_second_player_sell, cp_current_player_sell, node_type="chance",
                                next_type=t, previous_type=self.node_type)
                new_node.action = f"after paying rent action of player {cp_current_player_buy.ID}"
                self.children.append(new_node)

            # do nothing
            cp_properties_nothing: list[property.Property] = copy.deepcopy(self.properties)
            cp_current_player_nothing = copy.deepcopy(self.current_player)
            cp_second_player_nothing = copy.deepcopy(self.second_player)
            if self.node_type == "max":
                t = "min"
            else:
                t = "max"
            new_node = Node(cp_properties_nothing, cp_second_player_nothing, cp_current_player_nothing,
                            node_type="chance",
                            next_type=t, previous_type=self.node_type)
            new_node.action = f"after do nothing action of player {cp_current_player_buy.ID}"
            self.children.append(new_node)

        return self.children
