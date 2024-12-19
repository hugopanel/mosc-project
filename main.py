import os
from math import floor
from random import randint, choice

import networkx
import pygame
import engine.ui
import engine.graph
import engine.config
import engine.events
import engine.config
import engine.entities
from engine.config import production_code_increase, default_max_growth, mutation_mutation_increase
from engine.entities import growth
from engine.ui import draw_tree_tooltip


class Inventory:
    def __init__(self):
        self.items = ["M", "A", "B", "C", "D", "G"]
        self.selected_item = 0
        self.position = (0, 0)
        self.width = 50
        self.height = 50

    def select_item(self, item_number):
        self.selected_item = item_number % len(self.items)

    def draw(self):
        if self.selected_item == 0:
            fg_color = "white"
            bg_color = "black"
        elif self.selected_item == 5:
            fg_color = "white"
            bg_color = "red"
        else:
            fg_color = "black"
            bg_color = "gray"

        font = pygame.font.SysFont("default", 50, False, False)
        text = font.render(str(self.items[self.selected_item]), True, fg_color)
        pygame.draw.rect(engine.config.screen, bg_color, (self.position[0], self.position[1], self.width, self.height))
        engine.config.screen.blit(text,
                                  (
                                      self.position[0] + round(self.width / 2) - round(text.get_width() / 2),
                                      self.position[1] + round(self.height / 2) - round(text.get_height()) / 2
                                  )
                                  )  # center the text


def get_current_selected_tile(garden):
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    selected_tile_x = floor((mouse_x - garden.position_x)/engine.config.garden_tile_size)
    selected_tile_y = floor((mouse_y - garden.position_y)/engine.config.garden_tile_size)
    return selected_tile_x, selected_tile_y


def main():
    pygame.init()
    engine.config.screen = pygame.display.set_mode((engine.config.screen_width, engine.config.screen_height), pygame.RESIZABLE)
    engine.config.clock = pygame.time.Clock()
    engine.config.running = True
    pygame.display.set_caption("Treevolution")
    
    # Initialize fonts
    engine.config.font_big = pygame.font.Font(None, 36)
    engine.config.font_heading = pygame.font.Font(None, 30)
    engine.config.font_small = pygame.font.Font(None, 24)


    # Initialize event handler
    event_handler = engine.events.EventHandler()

    # Add event to quit game when window is closed
    def quit_game(event):
        engine.config.running = False
    event_handler.add_handler(pygame.QUIT, quit_game)
    
    # Window resize event
    def resize_window(event):
        engine.config.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        engine.config.screen_width = event.w
        engine.config.screen_height = event.h
    event_handler.add_handler(pygame.VIDEORESIZE, resize_window)

    # Create inventory and inventory navigation functions
    inventory = Inventory()

    def select_item_wall(event):
        inventory.select_item(0)

    def select_item_2(event):
        inventory.select_item(1)

    def select_item_3(event):
        inventory.select_item(2)

    def select_item_4(event):
        inventory.select_item(3)

    def select_item_5(event):
        inventory.select_item(4)

    def select_item_eraser(event):
        inventory.select_item(5)

    # Generate garden graph
    garden_graph = engine.graph.generate_garden(engine.config.garden_size["x"], engine.config.garden_size["y"])
    garden = engine.ui.Garden(garden_graph, engine.config.garden_size["x"], engine.config.garden_size["y"], floor((engine.config.screen_width - engine.config.garden_size["x"] * engine.config.garden_tile_size)/2), floor((engine.config.screen_height - engine.config.garden_size["y"] * engine.config.garden_tile_size)/2))

    # Place a tree in the garden
    placing = False
    def begin_placing(event):
        nonlocal placing
        placing = True

    def end_placing(event):
        nonlocal placing
        placing = False
        
    def place_tree():
        selected_tile_x, selected_tile_y = get_current_selected_tile(garden)
        if 0 <= selected_tile_x < garden.size_x and 0 <= selected_tile_y < garden.size_y:
            selected_tile = garden.garden_tiles[selected_tile_y][selected_tile_x]
            node = garden.graph.nodes[(selected_tile_x, selected_tile_y)]
            
            # Reset node
            node["sicknesses"] = []
            node["age"] = 0
            node["code"] = []
            node["growth"] = 0
            node["health"] = engine.config.default_seed_starting_health
            
            # Update node property
            if inventory.selected_item == 0: # Place wall
                selected_tile.tile_number = 3
                node["type"] = engine.entities.TYPE_WALL
            elif inventory.selected_item in [1, 2, 3, 4]: # Place seed
                selected_tile.tile_number = 1
                node["type"] = engine.entities.TYPE_SEED
                if inventory.selected_item == 1:
                    node["code"] = engine.entities.known_tree_species[0]["code"]
                elif inventory.selected_item == 2:
                    node["code"] = engine.entities.known_tree_species[1]["code"]
                elif inventory.selected_item == 3:
                    node["code"] = engine.entities.known_tree_species[2]["code"]
                elif inventory.selected_item == 4:
                    node["code"] = engine.entities.known_tree_species[3]["code"]
            elif inventory.selected_item == 5:
                selected_tile.tile_number = 0
                node["type"] = engine.entities.TYPE_EMPTY

    simulation_running = False
    cycle_count = 0
    time_to_next_cycle = engine.config.cycle_length
    
    def toggle_simulation_running(event):
        nonlocal simulation_running
        simulation_running = not simulation_running
    
    # KEY MAPPING
    event_handler.add_key_handler(pygame.K_1, select_item_wall)
    event_handler.add_key_handler(pygame.K_2, select_item_2)
    event_handler.add_key_handler(pygame.K_3, select_item_3)
    event_handler.add_key_handler(pygame.K_4, select_item_4)
    event_handler.add_key_handler(pygame.K_5, select_item_5)
    event_handler.add_key_handler(pygame.K_6, select_item_eraser)
    event_handler.add_key_handler(pygame.K_p, toggle_simulation_running)
    event_handler.add_handler(pygame.MOUSEBUTTONDOWN, begin_placing)
    event_handler.add_handler(pygame.MOUSEBUTTONUP, end_placing)

    
    while engine.config.running:
        event_handler.pump_events()

        # LOGIC
        # Allow player to place tiles
        if placing:
            place_tree()
        
        # Handle time    
        if simulation_running:
            time_to_next_cycle -= 1
            if time_to_next_cycle <= 0:
                # Update time
                time_to_next_cycle = engine.config.cycle_length
                cycle_count += 1
                
                # Update nodes
                for node_name in garden.graph.nodes:
                    node = garden.graph.nodes[node_name]
                    
                    # Increase node age
                    node["age"] += 1
                    
                    # Seeds and trees
                    if node["type"] in [engine.entities.TYPE_SEED, engine.entities.TYPE_TREE]:
                        # Regenerate health
                        if node["health"] < engine.config.default_max_health:
                            node["health"] = round(node["health"] * engine.config.default_health_regeneration_multiplier, 1) 
                            if node["health"] > engine.config.default_max_health: node["health"] = engine.config.default_max_health 
                    
                    # Seeds
                    if node["type"] == engine.entities.TYPE_SEED:
                        # Grow seed
                        if randint(0, 100) > (engine.config.default_growth_probability*100):
                            node["growth"] += 1 + production_code_increase*(sum(node["code"].count(x) for x in growth))
                            if node["growth"] >= default_max_growth:
                                node["type"] = engine.entities.TYPE_TREE
                                garden.garden_tiles[node_name[1]][node_name[0]].tile_number = 2

                    # Trees
                    if node["type"] == engine.entities.TYPE_TREE:
                        # Propagate seed
                        if randint(0, 100) > (engine.config.default_seed_propagation_probability * 100):
                            # Choose a random node among the empty ones, if any
                            empty_neighbors = [n for n in networkx.neighbors(garden.graph, node_name) if garden.graph.nodes[n]["type"] == engine.entities.TYPE_EMPTY]
                            if len(empty_neighbors) > 0:
                                chosen_node_name = choice(empty_neighbors)
                                chosen_node = garden.graph.nodes[chosen_node_name]
                                
                                # Update node for logic
                                chosen_node["type"] = engine.entities.TYPE_SEED
                                chosen_node["health"] = engine.config.default_seed_starting_health # TODO: Remove if unnecessary
                                chosen_node["code"] = node["code"].copy()
                                
                                # Try to mutate seed
                                if randint(0, 100) > (engine.config.default_mutation_probability + (mutation_mutation_increase * sum(node["code"].count(x) for x in engine.entities.mutation)))*100:
                                    # Choose a random code to mutate
                                    i = randint(0, len(chosen_node["code"]) - 1)
                                    chosen_node["code"][i] = randint(0, engine.entities.max_codes)
                                
                                # Update tile for drawing
                                chosen_tile = garden.garden_tiles[chosen_node_name[1]][chosen_node_name[0]]
                                chosen_tile.tile_number = 1

        # DRAWING
        engine.config.screen.fill("white")
        
        # Update garden position according to window size
        garden.position_x = floor((engine.config.screen_width - engine.config.garden_size["x"] * engine.config.garden_tile_size)/2)
        garden.position_y = floor((engine.config.screen_height - engine.config.garden_size["y"] * engine.config.garden_tile_size)/2)
        
        garden.draw()
        inventory.draw()
        
        # Show hovered tile as variant
        selected_tile_x, selected_tile_y = get_current_selected_tile(garden)
        
        for row in garden.garden_tiles:
            for tile in row:
                tile.variant = False
        
        if 0 <= selected_tile_x < garden.size_x and 0 <= selected_tile_y < garden.size_y:
            garden.garden_tiles[selected_tile_y][selected_tile_x].variant = True
            draw_tree_tooltip(engine.config.screen, (selected_tile_x, selected_tile_y), garden.graph.nodes[(selected_tile_x, selected_tile_y)])
        
        # Display time
        engine.ui.display_time(simulation_running, cycle_count, time_to_next_cycle)
        
        pygame.display.flip() # Flip buffer
        engine.config.clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
