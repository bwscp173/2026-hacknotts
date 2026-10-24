import pygame


class Graph:
    """
    The trading graph that attaches to the screen
    """

    def __init__(self, width, height, data):
        self.surface = pygame.Surface((width, height))

    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
