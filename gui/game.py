import pygame
from random import randint

from .graph import Graph
from bonsai_buddy.main_v2 import bonsai_buddy

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

        self.bb = bonsai_buddy(self.screen)

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
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("SPACE DOWN")
                        self.bb.draw(self.screen)
                        self.bb.moveTo(randint(0, self.width), randint(0, self.height))
                    if event.key == pygame.K_RETURN:
                        print("RETURN DOWN")
                        self.bb.increment_frame()

                if event.type == pygame.MOUSEMOTION:
                    self.bb.set_location(pygame.mouse.get_pos())

            self.fill((255, 255, 255))
            self.graph.draw(self.screen, 10, 10)
            self.bb.draw(self.screen)
            self.update()

        pygame.quit()

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
