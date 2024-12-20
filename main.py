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
from engine.config import production_code_increase, default_max_growth, mutation_mutation_increase, \
    matching_code_impact_sickness_heal
from engine.entities import growth_codes
from engine.ui import draw_tree_tooltip


class Inventory:
    def __init__(self):
        self.items = ["[0, 0, 0]", "[3, 3, 3]", "[6, 6, 6]", "[9, 9, 9]", "W", "E"]
        self.selected_item = 0
        self.position = (0, 0)
        self.min_width = 50
        self.height = 50
        self.presets = [
            {"type": "Tree", "code": [engine.entities.production, engine.entities.production, engine.entities.production]},
            {"type": "Tree", "code": [engine.entities.growth, engine.entities.growth, engine.entities.growth]},
            {"type": "Tree", "code": [engine.entities.mutation, engine.entities.mutation, engine.entities.mutation]},
            {"type": "Sickness", "code": [engine.entities.protection, engine.entities.protection, engine.entities.protection]},
            {"type": "Wall", "code": []},
            {"type": "Eraser", "code": []}
        ]
        self.sprite_sheet = pygame.image.load(os.path.join("assets", "inventory_tileset.png")).convert()
        self.sprite_sheet_size_x = 3
        self.sprite_sheet_size_y = 2
        self.sprite_size_x = 16
        self.sprite_size_y = 16
        
    def select_item(self, item_number):
        self.selected_item = item_number % len(self.items)
    
    def change_preset(self, preset, item=None):
        item = item if item is not None else self.selected_item
        if item < 4:
            self.presets[item]["code"] = preset["code"]
            self.items[item] = preset["code"]

    def draw(self):
        if self.selected_item == 4:
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
        width = max(self.min_width, (text.get_width() + 20))

        if self.selected_item < 4:
            width += 50
            
        pygame.draw.rect(engine.config.screen, bg_color, (self.position[0], self.position[1], width, self.height))
        
        engine.config.screen.blit(text,
                                  (
                                      self.position[0] + round(width / 2) - round(text.get_width() / 2) + 20 if self.selected_item < 4 else 0,
                                      self.position[1] + round(self.height / 2) - round(text.get_height()) / 2
                                  )
                                  )  # center the text
        
        rect = pygame.Rect(self.sprite_size_x * (self.selected_item % (self.sprite_sheet_size_x)), self.sprite_size_y * round(self.selected_item / (self.sprite_sheet_size_x + 1)), self.sprite_size_x, self.sprite_size_y)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sprite_sheet, (0, 0), rect)
        image.set_colorkey(pygame.Color(0, 0, 0, 0), pygame.RLEACCEL)
        image = pygame.transform.scale(image, (50, 50))
        engine.config.screen.blit(image, (0, 0))


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

    # Overlay
    # 0: No overlay
    # 1: Mutation overlay
    # 2: Sicknesses overlay
    # 3: Origin group overlay
    current_overlay = 0
    
    def select_no_overlay(event):
        nonlocal current_overlay
        current_overlay = 0
    def select_overlay_1(event):
        nonlocal current_overlay
        current_overlay = 1
    def select_overlay_2(event):
        nonlocal current_overlay
        current_overlay = 2
    def select_overlay_3(event):
        nonlocal current_overlay
        current_overlay = 3

    # Generate garden graph
    garden_graph = None
    garden = None
    
    def generate_garden():
        nonlocal garden_graph
        nonlocal garden
        garden_graph = engine.graph.generate_garden(engine.config.garden_size["x"], engine.config.garden_size["y"])
        garden = engine.ui.Garden(garden_graph, engine.config.garden_size["x"], engine.config.garden_size["y"], floor((engine.config.screen_width - engine.config.garden_size["x"] * engine.config.garden_tile_size)/2), floor((engine.config.screen_height - engine.config.garden_size["y"] * engine.config.garden_tile_size)/2))

    generate_garden()

    def reset_garden(event):
        # Reset garden
        nonlocal garden_graph
        nonlocal garden
        del garden_graph
        del garden
        generate_garden()
        
        # Reset properties
        nonlocal cycle_count
        nonlocal cycle_production
        nonlocal total_production
        cycle_count = 0
        cycle_production = 0
        total_production = 0
        

    def reset_node_properties(node_properties):
        node_properties["type"] = engine.entities.TYPE_EMPTY
        node_properties["sicknesses"] = []
        node_properties["age"] = 0
        node_properties["code"] = []
        node_properties["growth"] = 0
        node_properties["health"] = engine.config.default_seed_starting_health
        node_properties["greatest_ancestor"] = None

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
            
            # Update node property
            item = inventory.presets[inventory.selected_item]

            if item["type"] == "Sickness":
                if len(node["sicknesses"]) < engine.config.default_max_sicknesses:
                    if item["code"] not in node["sicknesses"]:
                        node["sicknesses"].append(item["code"])
                return
            
            # Reset node
            reset_node_properties(node)
            
            if item["type"] == "Wall":
            # if inventory.selected_item == 0: # Place wall
                selected_tile.tile_number = 3
                node["type"] = engine.entities.TYPE_WALL
            elif item["type"] == "Eraser":
                selected_tile.tile_number = 0
                node["type"] = engine.entities.TYPE_EMPTY
            elif item["type"] == "Tree":
                selected_tile.tile_number = 1
                node["type"] = engine.entities.TYPE_SEED
                node["code"] = item["code"]

    simulation_running = False
    cycle_count = 0
    time_to_next_cycle = engine.config.cycle_length
    
    def toggle_simulation_running(event):
        nonlocal simulation_running
        simulation_running = not simulation_running

    menu_stack = []
    def open_custom_tree_menu(event):
        if inventory.selected_item < 4:
            menu = engine.ui.CreateTreeMenu()
            menu_stack.append(menu)
            menu.open(event_handler, inventory)
    def open_probability_settings_menu(event):
        menu = engine.ui.ChangeProbabilitiesMenu()
        menu_stack.append(menu)
        menu.open(event_handler)
    
    # KEY MAPPING
    # Inventory
    event_handler.add_key_handler(pygame.K_1, select_item_wall)
    event_handler.add_key_handler(pygame.K_2, select_item_2)
    event_handler.add_key_handler(pygame.K_3, select_item_3)
    event_handler.add_key_handler(pygame.K_4, select_item_4)
    event_handler.add_key_handler(pygame.K_5, select_item_5)
    event_handler.add_key_handler(pygame.K_6, select_item_eraser)
    # Overlay
    event_handler.add_key_handler(pygame.K_q, select_no_overlay)
    event_handler.add_key_handler(pygame.K_w, select_overlay_1)
    event_handler.add_key_handler(pygame.K_e, select_overlay_2)
    event_handler.add_key_handler(pygame.K_r, select_overlay_3)
    # Simulation
    event_handler.add_key_handler(pygame.K_p, toggle_simulation_running)
    event_handler.add_key_handler(pygame.K_BACKQUOTE, reset_garden)
    # Placing trees
    event_handler.add_handler(pygame.MOUSEBUTTONDOWN, begin_placing)
    event_handler.add_handler(pygame.MOUSEBUTTONUP, end_placing)
    # UI menus
    event_handler.add_key_handler(pygame.K_SPACE, open_custom_tree_menu) # TODO: Change key
    event_handler.add_key_handler(pygame.K_TAB, open_probability_settings_menu) # TODO: Change key

    total_production = 0
    cycle_production = 0
    
    while engine.config.running:
        event_handler.pump_events()

        if len(menu_stack) == 0:
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
                    cycle_production = 0
                    
                    # Update nodes
                    for node_name in garden.graph.nodes:
                        node = garden.graph.nodes[node_name]
                        
                        # Increase node age
                        node["age"] += 1
                        
                        # Walls, seeds and trees
                        if node["type"] in [engine.entities.TYPE_WALL, engine.entities.TYPE_SEED, engine.entities.TYPE_TREE]:
                            # Heal from a sickness
                            if len(node["sicknesses"]) > 0:
                                for sickness in node["sicknesses"]:
                                    if node["type"] == engine.entities.TYPE_WALL:
                                        probability = (engine.config.default_sickness_heal_probability * (1 + 1 - engine.config.wall_sickness_multiplier))*100
                                    else:
                                        probability = (engine.config.default_sickness_heal_probability - matching_code_impact_sickness_heal*sum(node["code"].count(x) for x in sickness))*100
                                    if randint(1, 100) <= probability:
                                        node["sicknesses"].remove(sickness)
                                        # TODO: Add immunity
    
                            # Become sick from a random sickness
                            if len(node["sicknesses"]) < engine.config.default_max_sicknesses:
                                if node["type"] == engine.entities.TYPE_WALL:
                                    probability = engine.config.default_random_sickness_appearance_probability * engine.config.wall_sickness_multiplier * 1000
                                else:
                                    probability = engine.config.default_random_sickness_appearance_probability*1000
                                if randint(1, 1000) <= probability:
                                    new_sickness = [randint(0, engine.entities.max_codes) for _ in range(engine.config.sickness_number_of_codes)]
                                    new_sickness.sort()
                                    if new_sickness not in node["sicknesses"]:
                                        node["sicknesses"].append(new_sickness)
                            
                            # Spread a sickness to a neighbor
                            if len(node["sicknesses"]) > 0:
                                if node["type"] == engine.entities.TYPE_WALL:
                                    probability = engine.config.default_sickness_propagation_probability * engine.config.wall_sickness_multiplier * 100
                                else:
                                    probability = engine.config.default_sickness_propagation_probability * 100
                                if randint(1, 100) <= probability:
                                    sickness_to_spread = choice(node["sicknesses"])
                                    neighbor = choice([node for node in networkx.neighbors(garden.graph, node_name)])
                                    if (garden.graph.nodes.get(neighbor)["type"] != engine.entities.TYPE_EMPTY) & (len(garden.graph.nodes.get(neighbor)["sicknesses"]) < engine.config.default_max_sicknesses):
                                        if not sickness_to_spread in garden.graph.nodes.get(neighbor)["sicknesses"]:
                                            garden.graph.nodes.get(neighbor)["sicknesses"].append(sickness_to_spread)
                        
                        # Seeds and trees
                        if node["type"] in [engine.entities.TYPE_SEED, engine.entities.TYPE_TREE]:
                            # Decrease health if sick
                            if len(node["sicknesses"]) > 0:
                                for sickness in node["sicknesses"]:
                                    # Decrease health
                                    node["health"] -= (
                                            engine.config.default_sickness_health_penalty # Base penalty for every sickness
                                            + engine.config.default_sickness_health_penalty*sum(node["code"].count(x) for x in sickness) # Increase the penalty if the sickness' code matches with that of the seed/tree 
                                            - engine.config.default_sickness_health_penalty*sum(node["code"].count(x) for x in engine.entities.protection_codes)) # Cancel penalties for each protection code in the seed/tree DNA code
                            
                            # Regenerate health
                            max_health = engine.config.default_max_health + engine.config.health_code_increase * sum(node["code"].count(x) for x in engine.entities.health_codes)
                            if node["health"] < max_health:
                                node["health"] += engine.config.default_health_regeneration_multiplier 
                                if node["health"] > max_health: node["health"] = max_health
                            
                            # Remove node if health <= 0
                            if node["health"] <= 0:
                                reset_node_properties(node)
                                garden.garden_tiles[node_name[1]][node_name[0]].tile_number = 0
                                continue
                        
                        # Seeds
                        if node["type"] == engine.entities.TYPE_SEED:
                            # Grow seed
                            if randint(1, 100) <= (engine.config.default_growth_probability*100):
                                node["growth"] += 1 + engine.config.growth_code_increase*(sum(node["code"].count(x) for x in growth_codes))
                                if node["growth"] >= default_max_growth:
                                    node["type"] = engine.entities.TYPE_TREE
                                    garden.garden_tiles[node_name[1]][node_name[0]].tile_number = 2
    
                        # Trees
                        if node["type"] == engine.entities.TYPE_TREE:
                            # Production
                            tree_production = engine.config.default_production + production_code_increase*(sum(node["code"].count(x) for x in engine.entities.production_codes))
                            total_production += tree_production # Total production
                            cycle_production += tree_production # Production from this cycle, to display
                            
                            # Propagate seed
                            if randint(1, 100) <= (engine.config.default_seed_propagation_probability * 100):
                                # Choose a random node among the empty ones, if any
                                empty_neighbors = [n for n in networkx.neighbors(garden.graph, node_name) if garden.graph.nodes[n]["type"] == engine.entities.TYPE_EMPTY]
                                if len(empty_neighbors) > 0:
                                    chosen_node_name = choice(empty_neighbors)
                                    chosen_node = garden.graph.nodes[chosen_node_name]
                                    
                                    # Update node for logic
                                    chosen_node["type"] = engine.entities.TYPE_SEED
                                    chosen_node["health"] = engine.config.default_seed_starting_health # TODO: Remove if unnecessary
                                    chosen_node["code"] = node["code"].copy()
                                    chosen_node["greatest_ancestor"] = node["greatest_ancestor"] if node["greatest_ancestor"] is not None else {
                                        "name": f"{engine.entities.get_species_name(node["code"])} Tree", "coordinates": node_name}
                                    
                                    # Try to mutate seed
                                    if randint(1, 100) <= (engine.config.default_mutation_probability + (mutation_mutation_increase * sum(node["code"].count(x) for x in engine.entities.mutation_codes)))*100:
                                        # Choose a random code to mutate
                                        i = randint(0, len(chosen_node["code"]) - 1)
                                        chosen_node["code"][i] = randint(0, engine.entities.max_codes - 1)
                                        chosen_node["code"].sort()
                                    
                                    # Update tile for drawing
                                    chosen_tile = garden.garden_tiles[chosen_node_name[1]][chosen_node_name[0]]
                                    chosen_tile.tile_number = 1 

        # DRAWING
        engine.config.screen.fill("white")
        
        # Update garden position according to window size
        garden.position_x = floor((engine.config.screen_width - engine.config.garden_size["x"] * engine.config.garden_tile_size)/2)
        garden.position_y = floor((engine.config.screen_height - engine.config.garden_size["y"] * engine.config.garden_tile_size)/2)
        
        garden.draw(overlay=current_overlay)
        inventory.draw()
        
        # Show hovered tile as variant
        selected_tile_x, selected_tile_y = get_current_selected_tile(garden)
        
        for row in garden.garden_tiles:
            for tile in row:
                tile.variant = False
            
        if len(menu_stack) == 0:
            if 0 <= selected_tile_x < garden.size_x and 0 <= selected_tile_y < garden.size_y:
                garden.garden_tiles[selected_tile_y][selected_tile_x].variant = True
                draw_tree_tooltip(engine.config.screen, (selected_tile_x, selected_tile_y), garden.graph.nodes[(selected_tile_x, selected_tile_y)])
        
        # Display time
        engine.ui.display_status_bar(simulation_running, cycle_count, time_to_next_cycle, cycle_production, total_production)
        
        # Display menus
        if len(menu_stack) > 0:
            while len(menu_stack) > 0: 
                if menu_stack[-1].is_open():
                    break
                menu_stack.pop()
                
            # Check if we just removed every menu or if there is still at least one
            if len(menu_stack) > 0:
                menu_stack[-1].draw() # If there is, draw it.
        
        pygame.display.flip() # Flip buffer
        engine.config.clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
