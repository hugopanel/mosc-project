# GUI Module
import os
from abc import abstractmethod, ABC

import pygame
from networkx.classes import Graph

import engine.config
import engine.entities


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
        type_name = engine.entities.get_species_name(node_properties['code']) + " {type} [{code}]".format(type="Seed" if node_properties["type"] == engine.entities.TYPE_SEED else "Tree", code="".join(str(c) for c in node_properties['code'])) 
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
        if node_properties["growth"] >= engine.config.default_max_growth:
            rows.append(engine.config.font_small.render("Age: {age}".format(age=node_properties["age"]), True, "gray"))
        else:
            rows.append(engine.config.font_small.render("Age: {age}, Growth: {growth}".format(age=node_properties["age"], growth=node_properties["growth"]), True, "gray"))
        rows.append(engine.config.font_small.render(f"Health: {round(node_properties["health"], 1)}", True, "gray"))
        rows.append(engine.config.font_small.render("Production: +5/cycle", True, "gray"))

    box_width = 10 + max(row.get_width() for row in rows)
    box_height = 10 + rows[0].get_height() + 5 + sum((5 + row.get_height()) for row in rows[1:])
    
    tooltip_box = pygame.Surface((box_width, box_height))
    position = pygame.mouse.get_pos()[0] + 10, pygame.mouse.get_pos()[1] + 10
    
    # Check if tooltip will render outside the window
    if position[0] + box_width > engine.config.screen_width:
        position = pygame.mouse.get_pos()[0] - 10 - box_width, position[1]
    if position[1] + box_height > engine.config.screen_height - 10:
        position = position[0], engine.config.screen_height - box_height - 10
    
    screen.blit(tooltip_box, position)
    for i in range(len(rows)):
        screen.blit(rows[i], (position[0] + 5, position[1] + 5 + sum(5 + row.get_height() for row in rows[:i])))


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

    def draw(self, position_x = None, position_y = None, width = None, height = None):
        offset_x = position_x if position_x is not None else self.position_x
        offset_y = position_y if position_y is not None else self.position_y
        width = width if width is not None else engine.config.garden_tile_size * self.size_x
        height = height if height is not None else engine.config.garden_tile_size * self.size_y
        
        for y in range(self.size_y):
            for x in range(self.size_x):
                tile: GardenTile = self.garden_tiles[y][x]
                image = tile.draw()
                image = pygame.transform.scale(image, (engine.config.garden_tile_size, engine.config.garden_tile_size))
                engine.config.screen.blit(image, (offset_x + x*(width/self.size_x), offset_y + y*(height/self.size_y)))
