# GUI Module
import os
from abc import abstractmethod, ABC
from math import floor
from random import choice

import pygame
from networkx.classes import Graph

import engine.config
import engine.entities
from engine.entities import codes
from engine.events import EventHandler

time_display_height = 30


def display_status_bar(simulation_running, cycle_count, time_to_next_cycle, production_per_cycle, total_production):
    height = time_display_height
    position_y = engine.config.screen_height - height
    left_text = engine.config.font_big.render(f"Simulation Running: {simulation_running} | Cycle: {round(cycle_count + (engine.config.cycle_length-time_to_next_cycle)/engine.config.cycle_length, 2)}", True, "white")
    right_text = engine.config.font_big.render(f"Current production per cycle: {production_per_cycle} Total production: {total_production}", True, "white")
    pygame.draw.rect(engine.config.screen, "black", (0, position_y, engine.config.screen_width, height))
    engine.config.screen.blit(left_text, (10, position_y + round(height / 2) - round(left_text.get_height()) / 2))
    engine.config.screen.blit(right_text, (engine.config.screen_width - right_text.get_width() - 10, position_y + round(height / 2) - round(left_text.get_height()) / 2))
    

class UIComponent:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @abstractmethod
    def draw(self, screen):
        pass

    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def set_size(self, new_width, new_height):
        self.width = new_width
        self.height = new_height


class Label(UIComponent):
    def __init__(self, x, y, text):
        super().__init__(x, y, 0, 0)
        self.x = x
        self.y = y
        self.text = text

    def draw(self, screen):
        font = engine.config.font_big
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y))


def draw_tree_tooltip(screen, node_coordinates: tuple, node_properties: dict):
    if node_properties['type'] == engine.entities.TYPE_EMPTY:
        return
    if node_properties['type'] in [engine.entities.TYPE_SEED, engine.entities.TYPE_TREE]:
        type_name = engine.entities.get_species_name(node_properties['code']) + " {type} [{code}]".format(type="Seed" if node_properties["type"] == engine.entities.TYPE_SEED else "Tree", code=" ".join(str(c) for c in node_properties['code'])) 
    else:
        type_name = "Wall"
    
    if len(node_properties["sicknesses"]) > 0:
        status = "Sick {0}".format(node_properties["sicknesses"])
    else:
        status = "healthy"

    rows = []
    rows.append(engine.config.font_heading.render("{coordinates} {type_name}".format(coordinates=node_coordinates, type_name=type_name), True, "white"))
    rows.append(engine.config.font_small.render("Status: {status}".format(status=status), True, "gray"))
    if node_properties['type'] in [engine.entities.TYPE_SEED, engine.entities.TYPE_TREE]:
        rows.append(engine.config.font_small.render(f"Greatest ancestor: {node_properties["greatest_ancestor"]["name"]} {node_properties["greatest_ancestor"]["coordinates"]}" if node_properties["greatest_ancestor"] is not None else "Original Tree", True, "gray"))
        if node_properties["growth"] >= engine.config.default_max_growth:
            rows.append(engine.config.font_small.render("Age: {age}".format(age=node_properties["age"]), True, "gray"))
        else:
            rows.append(engine.config.font_small.render("Age: {age}, Growth: {growth}".format(age=node_properties["age"], growth=node_properties["growth"]), True, "gray"))
        rows.append(engine.config.font_small.render(f"Health: {round(node_properties["health"], 1)}", True, "gray"))
    if node_properties["type"] == engine.entities.TYPE_TREE:
        rows.append(engine.config.font_small.render(f"Production: +{engine.config.default_production + engine.config.production_code_increase*(sum(node_properties["code"].count(x) for x in engine.entities.production_codes))}/cycle", True, "gray"))

    box_width = 10 + max(row.get_width() for row in rows)
    box_height = 10 + rows[0].get_height() + 5 + sum((5 + row.get_height()) for row in rows[1:])
    
    tooltip_box = pygame.Surface((box_width, box_height))
    position = pygame.mouse.get_pos()[0] + 10, pygame.mouse.get_pos()[1] + 10
    
    # Check if tooltip will render outside the window
    if position[0] + box_width > engine.config.screen_width:
        position = pygame.mouse.get_pos()[0] - 10 - box_width, position[1]
    if position[1] + box_height > engine.config.screen_height - 10 - time_display_height:
        position = position[0], engine.config.screen_height - box_height - 10 - time_display_height
    
    screen.blit(tooltip_box, position)
    for i in range(len(rows)):
        screen.blit(rows[i], (position[0] + 5, position[1] + 5 + sum(5 + row.get_height() for row in rows[:i])))


class UIMenu:
    _is_open = False
    
    @abstractmethod
    def open(self, event_handler: EventHandler):
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass
    
    def is_open(self) -> bool:
        return self._is_open
    

class CreateTreeMenu(UIMenu):
    def __init__(self):
        self._old_handlers = None
        self.event_handler = None
        self._inventory = None
        self._current_selection = 0
        self._current_configuration = {
            0: 0, # Production
            1: 0, # Growth
            2: 0, # Mutation
            3: 0, # Protection
            4: 0  # Health
        }

    def open(self, event_handler: EventHandler, inventory):
        # Copy event handler
        self._old_handlers = event_handler.handlers
        
        # Reset event handler
        event_handler.handlers = {}
        event_handler.handlers[pygame.KEYDOWN] = {}
        self.event_handler = event_handler
        
        # Copy inventory
        self._inventory = inventory
        
        # Add new mappings
        event_handler.add_key_handler(pygame.K_ESCAPE, self.close_event)
        event_handler.add_key_handler(pygame.K_DOWN, self.select_next_item)
        event_handler.add_key_handler(pygame.K_UP, self.select_previous_item)
        event_handler.add_key_handler(pygame.K_RIGHT, self.increase_current_item)
        event_handler.add_key_handler(pygame.K_LEFT, self.decrease_current_item)
        event_handler.add_key_handler(pygame.K_RETURN, self.save_to_inventory)
        
        self._is_open = True

    def close_event(self, event):
        self.close()
        
    def close(self):
        self._is_open = False
        # Return to old event handler
        self.event_handler.handlers = self._old_handlers

    def select_next_item(self, event):
        self._current_selection += 1
        self._current_selection %= 5
    
    def select_previous_item(self, event):
        self._current_selection -= 1
        self._current_selection %= 5
    
    def increase_current_item(self, event):
        current_count = sum(self._current_configuration[x] for x in self._current_configuration)
        if current_count < 3:
            self._current_configuration[self._current_selection] += 1
    
    def decrease_current_item(self, event):
        if self._current_configuration[self._current_selection] > 0:
            self._current_configuration[self._current_selection] -= 1  
    
    def save_to_inventory(self, event):
        # Generate code
        code = []
        for i in range(5):
            if self._current_configuration[i] > 0:
                for j in range(self._current_configuration[i]):
                    code.append(choice(codes[i]))
        self._inventory.change_preset({"type": "Tree", "code": code})
        self.close()
        
    def draw(self):        
        rows = []
        rows.append(engine.config.font_big.render(f"Production: {self._current_configuration[0]}", True, (255, 255 - (60*self._current_configuration[0]), 255)))
        rows.append(engine.config.font_big.render(f"Growth: {self._current_configuration[1]}", True, (255 - (60*self._current_configuration[1]), 255, 255)))
        rows.append(engine.config.font_big.render(f"Mutation: {self._current_configuration[2]}", True, (255, 255, 255 - (60*self._current_configuration[2]))))
        rows.append(engine.config.font_big.render(f"Protection: {self._current_configuration[3]}", True, (*[255 - (60*self._current_configuration[3]) for _ in range(2)], 255)))
        rows.append(engine.config.font_big.render(f"Health: {self._current_configuration[4]}", True, (255, *[255 - (60*self._current_configuration[4]) for _ in range(2)])))

        # Create a background rectangle
        # box_width = engine.config.screen_width - 40
        box_width = (20 + 5 + max(row.get_width() for row in rows) + 20 + 5)
        box_height = (20 + 5 + sum(row.get_height() for row in rows) + 20 + 5)

        bg_rect = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        bg_rect.fill((0, 0, 0, 240))

        engine.config.screen.blit(bg_rect, (0, 50))
        
        for i in range(len(rows)):
            offset_x = 0
            if i == self._current_selection:
                offset_x = 20
            engine.config.screen.blit(rows[i], (20 + offset_x, 70 + i*5 + sum(row.get_height() for row in rows[:i])))


class ChangeProbabilitiesMenu(UIMenu):
    def __init__(self):
        self._old_handlers = None
        self.event_handler = None
        self._current_selection = 0
        self._current_configuration = [
            [10, engine.config.cycle_length, 1, 1000],
            [0.1, engine.config.default_growth_rate, 0, 1],
            [0.1, engine.config.default_growth_probability, 0, 1],
            [1, engine.config.default_max_growth, 1, 1000],
            [50, engine.config.default_max_health, 1, 1000],
            [1, engine.config.default_seed_starting_health, 0, 1000],
            [0.5, engine.config.default_health_regeneration_multiplier, 1, 1000],
            [0.5, engine.config.default_sickness_health_penalty, 0, 1000],
            [0.1, engine.config.default_sickness_propagation_probability, 0, 1],
            [0.1, engine.config.default_sickness_heal_probability, 0, 1],
            [0, engine.config.default_sickness_immunity_probability, 0, 1],
            [0.1, engine.config.default_random_sickness_appearance_probability, 0, 1],
            [0.1, engine.config.default_seed_propagation_probability, 0, 1],
            [0.1, engine.config.default_mutation_probability, 0, 1],
            [1, engine.config.default_production, 0, 1000],
            [0.1, engine.config.wall_sickness_multiplier, 0, 1],
            [1, engine.config.default_max_sicknesses, 0, 1000],
            [0, engine.config.sickness_number_of_codes, 1, 1000],
            [1, engine.config.production_code_increase, 0, 1000],
            [1, engine.config.growth_code_increase, 0, 1000],
            [0.1, engine.config.mutation_mutation_increase, 0, 1],
            [0.1, engine.config.matching_code_impact_sickness_heal, 0, 1],
            [25, engine.config.health_code_increase, 0, 1000]
        ]

    def open(self, event_handler: EventHandler):
        # Copy event handler
        self._old_handlers = event_handler.handlers

        # Reset event handler
        event_handler.handlers = {}
        event_handler.handlers[pygame.KEYDOWN] = {}
        self.event_handler = event_handler

        # Add new mappings
        event_handler.add_key_handler(pygame.K_ESCAPE, self.close_event)
        event_handler.add_key_handler(pygame.K_DOWN, self.select_next_item)
        event_handler.add_key_handler(pygame.K_UP, self.select_previous_item)
        event_handler.add_key_handler(pygame.K_RIGHT, self.increase_current_item)
        event_handler.add_key_handler(pygame.K_LEFT, self.decrease_current_item)
        event_handler.add_key_handler(pygame.K_RETURN, self.save_configuration)

        self._is_open = True

    def close_event(self, event):
        self.close()

    def close(self):
        self._is_open = False
        # Return to old event handler
        self.event_handler.handlers = self._old_handlers
    
    def save_configuration(self, event):
        # Save configuration
        engine.config.cycle_length = self._current_configuration[0][1]
        engine.config.default_growth_rate = self._current_configuration[1][1]
        engine.config.default_growth_probability = self._current_configuration[2][1]
        engine.config.default_max_growth = self._current_configuration[3][1]
        engine.config.default_max_health = self._current_configuration[4][1]
        engine.config.default_seed_starting_health = self._current_configuration[5][1]
        engine.config.default_health_regeneration_multiplier = self._current_configuration[6][1]
        engine.config.default_sickness_health_penalty = self._current_configuration[7][1]
        engine.config.default_sickness_propagation_probability = self._current_configuration[8][1]
        engine.config.default_sickness_heal_probability = self._current_configuration[9][1]
        engine.config.default_sickness_immunity_probability = self._current_configuration[10][1]
        engine.config.default_random_sickness_appearance_probability = self._current_configuration[11][1]
        engine.config.default_seed_propagation_probability = self._current_configuration[12][1]
        engine.config.default_mutation_probability = self._current_configuration[13][1]
        engine.config.default_production = self._current_configuration[14][1]
        engine.config.wall_sickness_multiplier = self._current_configuration[15][1]
        engine.config.default_max_sicknesses = self._current_configuration[16][1]
        engine.config.sickness_number_of_codes = self._current_configuration[17][1]
        engine.config.production_code_increase = self._current_configuration[18][1]
        engine.config.growth_code_increase = self._current_configuration[19][1]
        engine.config.mutation_mutation_increase = self._current_configuration[20][1]
        engine.config.matching_code_impact_sickness_heal = self._current_configuration[21][1]
        engine.config.health_code_increas = self._current_configuration[22][1]
        
        self.close()

    def select_next_item(self, event):
        self._current_selection += 1
        self._current_selection %= len(self._current_configuration)

    def select_previous_item(self, event):
        self._current_selection -= 1
        self._current_selection %= len(self._current_configuration)

    def increase_current_item(self, event):
        self._current_configuration[self._current_selection][1] = round(self._current_configuration[self._current_selection][1] + self._current_configuration[self._current_selection][0], 3)
        if self._current_configuration[self._current_selection][1] > self._current_configuration[self._current_selection][3]:
            self._current_configuration[self._current_selection][1] = self._current_configuration[self._current_selection][3]

    def decrease_current_item(self, event):
        if self._current_configuration[self._current_selection][1] > 0:
            self._current_configuration[self._current_selection][1] = round(self._current_configuration[self._current_selection][1] - self._current_configuration[self._current_selection][0], 3)
        if self._current_configuration[self._current_selection][1] < self._current_configuration[self._current_selection][2]:
            self._current_configuration[self._current_selection][1] = self._current_configuration[self._current_selection][2]

    def draw(self):
        rows = []
        rows.append(engine.config.font_small.render(f"Cycle duration: {self._current_configuration[0][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Growth rate: {self._current_configuration[1][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Growth probability: {self._current_configuration[2][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Max growth: {self._current_configuration[3][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Max health: {self._current_configuration[4][1]}", True, "white"))
        rows.append(engine.config.font_small.render(f"Seed starting health: {self._current_configuration[5][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Health regen multiplier: {self._current_configuration[6][1]}", True, "white"))
        rows.append(engine.config.font_small.render(f"Sickness health penalty: {self._current_configuration[7][1]}", True, "white"))
        rows.append(engine.config.font_small.render(f"Sickness propagation probability: {self._current_configuration[8][1]}", True, "white"))
        rows.append(engine.config.font_small.render(f"Sickness heal probability: {self._current_configuration[9][1]}", True, "white"))
        rows.append(engine.config.font_small.render(f"Sickness immunity probability: {self._current_configuration[10][1]}", True, (40, 40, 40)))
        rows.append(engine.config.font_small.render(f"Random sickness appearance probability: {self._current_configuration[11][1]}", True, "white"))
        rows.append(engine.config.font_small.render(f"Seed propagation probability: {self._current_configuration[12][1]}", True, "white"))
        rows.append(engine.config.font_small.render(f"Seed mutation probability: {self._current_configuration[13][1]}", True, "white"))
        rows.append(engine.config.font_small.render(f"Default production: {self._current_configuration[14][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Wall sickness multiplier: {self._current_configuration[15][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Max number of sicknesses: {self._current_configuration[16][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Sickness DNA length: {self._current_configuration[17][1]}", True, (40, 40, 40)))
        rows.append(engine.config.font_small.render(f"Production code increase: {self._current_configuration[18][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Growth code increase: {self._current_configuration[19][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Mutation code increase: {self._current_configuration[20][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Matching code impact sickness health: {self._current_configuration[21][1]}", True, "gray"))
        rows.append(engine.config.font_small.render(f"Health code increase: {self._current_configuration[22][1]}", True, "gray"))

        # Create a background rectangle
        # box_width = engine.config.screen_width - 40
        box_width = (20 + 5 + max(row.get_width() for row in rows) + 20 + 5)
        box_height = (20 + sum(row.get_height() for row in rows) + 5 * len(rows) + 20)

        bg_rect = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        bg_rect.fill((0, 0, 0, 240))

        engine.config.screen.blit(bg_rect, (0, 50))

        for i in range(len(rows)):
            offset_x = 0
            if i == self._current_selection:
                offset_x = 20
            engine.config.screen.blit(rows[i], (20 + offset_x, 70 + i*5 + sum(row.get_height() for row in rows[:i])))
        

class GardenTile(pygame.sprite.Sprite):
    def __init__(self, tileset_path, tile_number, size: int, *groups):
        super().__init__(*groups)
        self.sprite_sheet = pygame.image.load(tileset_path).convert()
        self.size = size
        self.variant = False
        self.tile_number = tile_number

    def draw(self):
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(self.size * self.tile_number, 0 if self.variant is False else self.size, self.size, self.size)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sprite_sheet, (0, 0), rect)
        image.set_colorkey(pygame.Color(0, 0, 0, 0), pygame.RLEACCEL)
        return image

    def toggle_variant(self):
        self.variant = not self.variant


class Garden:
    def __init__(self, graph: Graph, size_x, size_y, position_x, position_y):
        self.graph = graph
        self.size_x = size_x
        self.size_y = size_y
        self.position_x = position_x
        self.position_y = position_y

        self.garden_tiles = []
        self.garden_tiles_group = pygame.sprite.Group()
        for y in range(size_y):
            self.garden_tiles.append([])
            for x in range(size_x):
                node = graph.nodes[(x, y)]
                self.garden_tiles[y].append(GardenTile(os.path.join("assets", "Tileset.png"), node["type"], 16))

    def draw(self, overlay, position_x = None, position_y = None, width = None, height = None):
        offset_x = position_x if position_x is not None else self.position_x
        offset_y = position_y if position_y is not None else self.position_y
        width = width if width is not None else engine.config.garden_tile_size * self.size_x
        height = height if height is not None else engine.config.garden_tile_size * self.size_y
        
        for y in range(self.size_y):
            for x in range(self.size_x):
                tile: GardenTile = self.garden_tiles[y][x]
                node_properties = self.graph.nodes.get((x, y))
                image = tile.draw()
                image = pygame.transform.scale(image, (engine.config.garden_tile_size, engine.config.garden_tile_size))
                engine.config.screen.blit(image, (offset_x + x*(width/self.size_x), offset_y + y*(height/self.size_y)))
                
                # Draw overlay
                if (overlay == 1) & (node_properties["type"] in [engine.entities.TYPE_SEED, engine.entities.TYPE_TREE]):
                    s = pygame.Surface((engine.config.garden_tile_size, engine.config.garden_tile_size), pygame.SRCALPHA)
                    node_code = node_properties["code"]
                    s.fill((
                        node_code[0]*(255/engine.entities.max_codes),
                        node_code[1]*(255/engine.entities.max_codes),
                        node_code[2]*(255/engine.entities.max_codes), 
                        128))
                    engine.config.screen.blit(s, (offset_x + x*(width/self.size_x), offset_y + y*(height/self.size_y)))
                if (overlay == 2) & (node_properties["type"] in [engine.entities.TYPE_WALL, engine.entities.TYPE_SEED, engine.entities.TYPE_TREE]):
                    sicknesses = node_properties["sicknesses"]
                    number_of_sicknesses = len(sicknesses)
                    for i in range(number_of_sicknesses):
                        sickness = sicknesses[i]
                        s = pygame.Surface((floor(engine.config.garden_tile_size/number_of_sicknesses), engine.config.garden_tile_size), pygame.SRCALPHA)
                        s.fill((
                            sickness[0]*(255/engine.entities.max_codes),
                            sickness[1]*(255/engine.entities.max_codes),
                            sickness[2]*(255/engine.entities.max_codes),
                        128))
                        engine.config.screen.blit(s, (offset_x + x*(width/self.size_x) + (i*floor(engine.config.garden_tile_size/number_of_sicknesses)), offset_y + y*(height/self.size_y)))
                if (overlay == 3) & (node_properties["type"] in [engine.entities.TYPE_SEED, engine.entities.TYPE_TREE]):
                    s = pygame.Surface((engine.config.garden_tile_size, engine.config.garden_tile_size), pygame.SRCALPHA)
                    ancestor_node = node_properties["greatest_ancestor"]
                    if ancestor_node is not None:
                        ancestor_node_coordinates = ancestor_node["coordinates"]
                        ancestor_node = self.graph.nodes.get(ancestor_node["coordinates"])
                    else:
                        ancestor_node_coordinates = (x, y)
                        ancestor_node = self.graph.nodes.get((x, y))
                    s.fill((
                        ancestor_node_coordinates[0]*(255/engine.config.garden_size["x"]),
                        ancestor_node_coordinates[1]*(255/engine.config.garden_size["y"]),
                        sum(ancestor_node["code"])*(255/(engine.entities.max_codes*3)),
                        128))
                    engine.config.screen.blit(s, (offset_x + x*(width/self.size_x), offset_y + y*(height/self.size_y)))
