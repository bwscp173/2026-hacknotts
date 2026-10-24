import pygame

class BottomPanel:
    def __init__(self, x:int, y:int, width:int, height:int, net_worth: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.net_worth = net_worth

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((30, 30, 30))

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))