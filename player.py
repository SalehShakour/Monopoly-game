import property


class Player:
    def __init__(self, player_id: int, balance=1500, position=0, properties=None):
        self.balance = balance
        self.position = position
        self.properties: list[property.Property] = properties or []
        self.ID = player_id

    def __str__(self):
        return self.ID

    def move(self, num_spaces):
        self.position = (self.position + num_spaces) % len(self.properties)

    def pay_rent(self, amount, recipient):
        self.balance -= amount
        recipient.balance += amount

    def buy(self, property):
        self.balance -= property.value
        self.properties.append(property)
        property.owner = self.ID

    def sell(self, property):
        # try:
            for item in self.properties:
                if item.position == property.position:
                    self.properties.remove(item)
                    item.owner = None
                    self.balance += (item.value * .9)
        #
        # except:
        #     for i in self.properties:
        #         print(i.position)
        #     print("---------")
        #     print(property.position)
