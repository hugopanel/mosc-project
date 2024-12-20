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
production_codes = [x for x in range(0, 3)]
growth_codes = [x for x in range(3, 6)]
mutation_codes = [x for x in range(6, 9)]
protection_codes = [x for x in range(9, 12)]
health_codes = [x for x in range(12, 15)]
codes = [
    production_codes,
    growth_codes,
    mutation_codes,
    protection_codes,
    health_codes
]
max_codes = 15

production = production_codes[0]
growth = growth_codes[0]
mutation = mutation_codes[0]
protection = protection_codes[0]
health = health_codes[0]

known_tree_species = [
    {"name": "Apple", "code": [production, production, production]},
    {"name": "Orange", "code": [growth, growth, growth]},
    {"name": "Peach", "code": [mutation, mutation, mutation]},
    {"name": "Pear", "code": [protection, protection, protection]},
    {"name": "Cherry", "code": [health, health, health]},
    {"name": "Lemon", "code": [production, production, growth]},
    {"name": "Lime", "code": [production, growth, growth]},
    {"name": "Grapefruit", "code": [production, growth, protection]},
    {"name": "Banana", "code": [production, growth, health]},
    {"name": "Pineapple", "code": [growth, protection, health]},
    {"name": "Coconut", "code": [production, protection, protection]},
    {"name": "Mango", "code": [production, growth, mutation]},
    {"name": "Papaya", "code": [growth, growth, mutation]},
    {"name": "Guava", "code": [mutation, mutation, health]},
    {"name": "Kiwi", "code": [production, mutation, mutation]},
    {"name": "Avocado", "code": [mutation, protection, health]},
    {"name": "Fig", "code": [protection, health, health]},
    {"name": "Olive", "code": [mutation, health, health]}
]

def get_species_name(species_code):
    for species in known_tree_species:
        if species["code"] == species_code:
            return species["name"]
    return "Mutated"