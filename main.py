import networkx
import pygame
import engine.ui
import engine.graph
import engine.config
import engine.events
import engine.config


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


def main():
    pygame.init()
    engine.config.screen = pygame.display.set_mode((1280, 720))
    engine.config.clock = pygame.time.Clock()
    engine.config.running = True
    pygame.display.set_caption("Treevolution")

    # Initialize event handler
    event_handler = engine.events.EventHandler()

    # Add event to quit game when window is closed
    def quit_game(event):
        engine.config.running = False
    event_handler.add_handler(pygame.QUIT, quit_game)

    # x = 0
    # y = 0
    # 
    # def move_right(event):
    #     nonlocal x
    #     x += 1
    # event_handler.add_key_event(pygame.K_d, move_right)
    # 
    # def move_down(event):
    #     nonlocal y
    #     y += 1
    # event_handler.add_key_event(pygame.K_s, move_down)

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

    event_handler.add_key_event(pygame.K_1, select_item_wall)
    event_handler.add_key_event(pygame.K_2, select_item_2)
    event_handler.add_key_event(pygame.K_3, select_item_3)
    event_handler.add_key_event(pygame.K_4, select_item_4)
    event_handler.add_key_event(pygame.K_5, select_item_5)
    event_handler.add_key_event(pygame.K_6, select_item_eraser)

    while engine.config.running:
        event_handler.pump_events()

        engine.config.screen.fill("white")
        # pygame.draw.rect(engine.config.screen, "black", (x, y, 30, 30),
        #                  border_radius=10)
        inventory.draw()
        pygame.display.flip()
        engine.config.clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
