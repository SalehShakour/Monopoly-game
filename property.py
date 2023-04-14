import random


class Property:
    def __init__(self, name, value, position):
        self.name = name
        self.value = value
        self.position = position
        self.tax = 0
        self.rent = value * 0.1
        self.owner = None


property_names = ["Mediterranean Avenue", "Baltic Avenue", "Oriental Avenue", "Vermont Avenue",
                  "Connecticut Avenue",
                  "St. Charles Place", "States Avenue", "Virginia Avenue", "St. James Place", "Tennessee Avenue",
                  "New York Avenue", "Kentucky Avenue", "Indiana Avenue", "Illinois Avenue", "Atlantic Avenue",
                  "Ventnor Avenue", "Marvin Gardens", "Pacific Avenue", "North Carolina Avenue",
                  "Pennsylvania Avenue",
                  "Park Place", "Boardwalk", "Reading Railroad", "Pennsylvania Railroad", "B&O Railroad",
                  "Short Line Railroad",
                  "Electric Company", "Water Works", "Community Chest", "Chance"]
properties = []

# Randomly select 5 properties to have tax
properties_with_tax = random.sample(property_names, 5)

for i in range(len(property_names)):
    if property_names[i] in properties_with_tax:
        tax = random.randint(10, 50)  # random tax between 10 and 50
        property_obj = Property(property_names[i], i * 10 + 50, i)
        property_obj.tax = tax
    else:
        property_obj = Property(property_names[i], i * 10 + 50, i)
    properties.append(property_obj)
