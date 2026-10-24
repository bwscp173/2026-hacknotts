import pygame


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Big money!!!!")

        # TODO: add screen data
        self.graph = Graph(int(self.width * (5 / 8)), int(self.height * (5 / 8)), None)

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

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
