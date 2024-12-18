# ENTITIES Module

# CONSTANTS
TYPE_EMPTY = 0
TYPE_SEED = 1
TYPE_TREE = 2
TYPE_WALL = 3

STATUS_EMPTY = 0
STATUS_HEALTHY = 1
STATUS_SICK = 2

known_tree_species = [
    {"name": "Apple tree", "code": [0, 0, 0]},
    {"name": "Orange tree", "code": [3, 3, 3]},
    {"name": "Peach tree", "code": [6, 6, 6]},
    {"name": "Pear tree", "code": [9, 9, 9]},
    {"name": "Cherry tree", "code": [12, 12, 12]},
    {"name": "Lemon tree", "code": [0, 0, 3]},
    {"name": "Lime tree", "code": [0, 3, 3]},
    {"name": "Grapefruit tree", "code": [0, 3, 9]},
    {"name": "Banana tree", "code": [0, 3, 12]},
    {"name": "Pineapple tree", "code": [3, 9, 12]},
    {"name": "Coconut tree", "code": [0, 9, 9]},
    {"name": "Mango tree", "code": [0, 3, 6]},
    {"name": "Papaya tree", "code": [3, 3, 6]},
    {"name": "Guava tree", "code": [6, 6, 12]},
    {"name": "Kiwi tree", "code": [0, 6, 6]},
    {"name": "Avocado tree", "code": [6, 9, 12]},
    {"name": "Fig tree", "code": [9, 12, 12]},
    {"name": "Olive tree", "code": [6, 12, 12]}
]

def get_species_name(species_code):
    for species in known_tree_species:
        if species["code"] == species_code:
            return species["name"]
    return "Mutated Tree"