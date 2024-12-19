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
cycle_length = 120 # Duration of a cycle in ticks

# Garden
garden_size = {"x": 10, "y": 10} # Size of the garden in number of tiles
garden_tile_size = 50 # Width and height of a tile in pixels

# Probabilities
default_growth_rate = 0.5 # What to add each cycle (if probability is positive)
default_growth_probability = 0.8 # Probability to grow per cycle
default_max_growth = 5 # Growth until mature
default_max_health = 100 # Maximum value for the health of a seed/tree
default_seed_starting_health = 5 # Seeds start low and gain health slowly using the health regen. mult.
default_health_regeneration_multiplier = 1.25 # When health is below the max, it regenerates at d_h_r_m*health per cycle
default_sickness_propagation_probability = 0.2 # Probability to propagate a sickness each cycle
default_seed_propagation_probability = 0.5 # Probability to produce a seed
default_mutation_probability = 0.1 # Probability to produce a mutated seed
default_production = 1 # Default production per cycle

# DNA code influence
production_code_increase = 2 # Each production code in the DNA code increases by...
mutation_mutation_increase = 0.1 
