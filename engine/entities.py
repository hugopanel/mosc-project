# ENTITIES Module

# CONSTANTS
TYPE_EMPTY = 0
TYPE_SEED = 1
TYPE_TREE = 2
TYPE_WALL = 3

STATUS_EMPTY = 0
STATUS_HEALTHY = 1
STATUS_SICK = 2

# Code values
production = [x for x in range(0, 3)]
growth = [x for x in range(3, 6)]
mutation = [x for x in range(6, 9)]
protection = [x for x in range(9, 12)]
health = [x for x in range(12, 15)]

known_tree_species = [
    {"name": "Apple", "code": [0, 0, 0]},
    {"name": "Orange", "code": [3, 3, 3]},
    {"name": "Peach", "code": [6, 6, 6]},
    {"name": "Pear", "code": [9, 9, 9]},
    {"name": "Cherry", "code": [12, 12, 12]},
    {"name": "Lemon", "code": [0, 0, 3]},
    {"name": "Lime", "code": [0, 3, 3]},
    {"name": "Grapefruit", "code": [0, 3, 9]},
    {"name": "Banana", "code": [0, 3, 12]},
    {"name": "Pineapple", "code": [3, 9, 12]},
    {"name": "Coconut", "code": [0, 9, 9]},
    {"name": "Mango", "code": [0, 3, 6]},
    {"name": "Papaya", "code": [3, 3, 6]},
    {"name": "Guava", "code": [6, 6, 12]},
    {"name": "Kiwi", "code": [0, 6, 6]},
    {"name": "Avocado", "code": [6, 9, 12]},
    {"name": "Fig", "code": [9, 12, 12]},
    {"name": "Olive", "code": [6, 12, 12]}
]

def get_species_name(species_code):
    for species in known_tree_species:
        if species["code"] == species_code:
            return species["name"]
    return "Mutated"