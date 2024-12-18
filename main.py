import os
from math import floor

import pygame
import engine.ui
import engine.graph
import engine.config
import engine.events
import engine.config
import engine.entities
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
            if inventory.selected_item == 0: # Place wall
                selected_tile.tile_number = 3
                garden.graph.nodes[(selected_tile_x, selected_tile_y)]["type"] = engine.entities.TYPE_WALL
                garden.graph.nodes[(selected_tile_x, selected_tile_y)]["status"] = engine.entities.STATUS_EMPTY
            elif inventory.selected_item in [1, 2, 3, 4]: # Place tree
                selected_tile.tile_number = 2
                garden.graph.nodes[(selected_tile_x, selected_tile_y)]["type"] = engine.entities.TYPE_TREE
                garden.graph.nodes[(selected_tile_x, selected_tile_y)]["status"] = engine.entities.STATUS_HEALTHY
                if inventory.selected_item == 1:
                    garden.graph.nodes[(selected_tile_x, selected_tile_y)]["species"] = engine.entities.known_tree_species[0]
                elif inventory.selected_item == 2:
                    garden.graph.nodes[(selected_tile_x, selected_tile_y)]["species"] = engine.entities.known_tree_species[1]
                elif inventory.selected_item == 3:
                    garden.graph.nodes[(selected_tile_x, selected_tile_y)]["species"] = engine.entities.known_tree_species[2]
                elif inventory.selected_item == 4:
                    garden.graph.nodes[(selected_tile_x, selected_tile_y)]["species"] = engine.entities.known_tree_species[3]
            elif inventory.selected_item == 5:
                selected_tile.tile_number = 0
                garden.graph.nodes[(selected_tile_x, selected_tile_y)]["type"] = engine.entities.TYPE_EMPTY
                garden.graph.nodes[(selected_tile_x, selected_tile_y)]["status"] = engine.entities.STATUS_EMPTY

    # KEY MAPPING
    event_handler.add_key_handler(pygame.K_1, select_item_wall)
    event_handler.add_key_handler(pygame.K_2, select_item_2)
    event_handler.add_key_handler(pygame.K_3, select_item_3)
    event_handler.add_key_handler(pygame.K_4, select_item_4)
    event_handler.add_key_handler(pygame.K_5, select_item_5)
    event_handler.add_key_handler(pygame.K_6, select_item_eraser)
    event_handler.add_handler(pygame.MOUSEBUTTONDOWN, begin_placing)
    event_handler.add_handler(pygame.MOUSEBUTTONUP, end_placing)

    sprite_sheet = pygame.image.load(os.path.join("assets", "Tileset.png")).convert()
    
    while engine.config.running:
        event_handler.pump_events()

        engine.config.screen.fill("white")
        
        if placing:
            place_tree()
        
        garden.position_x = floor((engine.config.screen_width - engine.config.garden_size["x"] * engine.config.garden_tile_size)/2)
        garden.position_y = floor((engine.config.screen_height - engine.config.garden_size["y"] * engine.config.garden_tile_size)/2)
        garden.draw()
        inventory.draw()
        
        selected_tile_x, selected_tile_y = get_current_selected_tile(garden)
        
        for row in garden.garden_tiles:
            for tile in row:
                tile.variant = False
        
        if 0 <= selected_tile_x < garden.size_x and 0 <= selected_tile_y < garden.size_y:
            garden.garden_tiles[selected_tile_y][selected_tile_x].variant = True
            draw_tree_tooltip(engine.config.screen, (selected_tile_x, selected_tile_y), garden.graph.nodes[(selected_tile_x, selected_tile_y)])
        
        pygame.display.flip()
        engine.config.clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
