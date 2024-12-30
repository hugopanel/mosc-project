import pygame


class EventHandler:
    def __init__(self):
        self.handlers = {}
        self.handlers[pygame.KEYDOWN] = {}

    def add_handler(self, event_type: int, handler: callable) -> None:
        if event_type not in self.handlers.keys():
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def add_key_handler(self, key: int, handler: callable) -> None:
        if key not in self.handlers[pygame.KEYDOWN]:
            self.handlers[pygame.KEYDOWN][key] = []
        self.handlers[pygame.KEYDOWN][key].append(handler)

    def handle_event(self, event):
        event_type = event.type
        if event_type in self.handlers.keys():
            if event_type == pygame.KEYDOWN:
                key = event.key
                if key in self.handlers[event_type].keys():
                    for handler in self.handlers[event_type][key]:
                        handler(event)
            else:
                for handler in self.handlers[event_type]:
                    handler(event)

    def pump_events(self):
        for event in pygame.event.get():
            self.handle_event(event)
