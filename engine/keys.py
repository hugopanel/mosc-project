import pygame


class Command:
    def __init__(self, key: int, action: callable):
        self.key = key
        self.action = action

    def execute(self):
        pass
