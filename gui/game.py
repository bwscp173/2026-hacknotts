import pygame

from .graph import Graph
from get_me_data.loader import Stock

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Big money!!!!")

        # TODO: add screen data

        self.graph = Graph(int(self.width * (5 / 8)), int(self.height * (5 / 8)), Stock("AMD"))

        # TODO: add individual buttons
        #    - stock selector to switch graph
        #    - volume to buy/sell stock
        #    - buy/sell button
        #    - banzibuddy interactions
        #    - current profit

    def fill(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.fill((255, 255, 255))
            self.graph.draw(self.screen, 10, 10)
            self.update()

        pygame.quit()

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
