import pygame


class EventHandler:
    def __init__(self):
        self.handlers = {}
        self.handlers[pygame.KEYDOWN] = {}

    def add_handler(self, event_type: int, handler: callable) -> None:
        self.handlers[event_type] = handler

    def add_key_handler(self, key: int, handler: callable) -> None:
        self.handlers[pygame.KEYDOWN][key] = handler

    def handle_event(self, event):
        event_type = event.type
        if event_type in self.handlers:
            if event_type == pygame.KEYDOWN:
                key = event.key
                if key in self.handlers[event_type]:
                    self.handlers[event_type][key](event)
            else:
                self.handlers[event_type](event)

    def pump_events(self):
        for event in pygame.event.get():
            self.handle_event(event)
