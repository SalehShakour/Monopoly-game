class Property:
    def __init__(self, name, value, rent, position, tax=0):
        self.name = name
        self.value = value
        self.rent = rent
        self.position = position
        self.owner = None
        self.tax = tax
