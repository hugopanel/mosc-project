# COMMON module

# PyGame
screen = None
clock = None
running = False
screen_width = 1280 # Width of the window in pixels
screen_height = 720 # Height of the window in pixels
font_big = None
font_heading = None
font_small = None

# Time
cycle_length = 10 # Duration of a cycle in ticks

# Garden
garden_size = {"x": 30, "y": 30} # Size of the garden in number of tiles
garden_tile_size = 20 # Width and height of a tile in pixels

# garden_size = {"x": 11, "y": 11} # Size of the garden in number of tiles
# garden_tile_size = 50 # Width and height of a tile in pixels

# Probabilities
default_growth_rate = 0.5 # What to add each cycle (if probability is positive)
default_growth_probability = 0.8 # Probability to grow per cycle
default_max_growth = 5 # Growth until mature
default_max_health = 500 # Maximum value for the health of a seed/tree
default_seed_starting_health = 5 # Seeds start low and gain health slowly using the health regen. mult.
default_health_regeneration_multiplier = 1.25 # When health is below the max, it regenerates at d_h_r_m*health per cycle
default_sickness_health_penalty = 1 # Each cycle, a sickness deals X damage to an infected node, no matter the DNA code
default_sickness_propagation_probability = 0.9 # Probability to propagate a sickness each cycle
default_sickness_heal_probability = 0.7 # Probability for each node to heal from a sickness
default_sickness_immunity_probability = 0.1 # Probability for each node to become immune to one of the sicknesses it has
default_random_sickness_appearance_probability = 0.1 # Probability of a new sickness appearing somewhere random per node per cycle (0/1000)
default_seed_propagation_probability = 0.5 # Probability to produce a seed
default_mutation_probability = 0.1 # Probability to produce a mutated seed
# default_mutation_probability = 0 # Probability to produce a mutated seed
default_production = 2 # Default production per cycle
wall_sickness_multiplier = 0.2 # By what to multiply the probability of being sick / spreading a sickness for walls. Healing for walls is the inverse or this (1-value)

default_max_sicknesses = 5 # Maximum number of sicknesses per wall/seed/tree at the same time.

# DNA code
sickness_number_of_codes = 3 # Length of the sickness' DNA code 
production_code_increase = 2 # Each production code in the DNA code increases production by...
growth_code_increase = 1 # Each growth code in the DNA code increases growth by...
mutation_mutation_increase = 0.1 # Each mutation code in the DNA code increases probability of mutation by...
# mutation_mutation_increase = 0 # Each mutation code in the DNA code increases probability of mutation by...
matching_code_impact_sickness_heal = 0.2 # Each matching code in the DNA code DECREASES the chance of healing by...
health_code_increase = 100 # Each health code increases the maximum health by...