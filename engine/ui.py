# GUI Module
from abc import abstractmethod

import pygame


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
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y))
