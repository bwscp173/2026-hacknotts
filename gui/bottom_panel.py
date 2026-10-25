import pygame

from gui.text_panel import TextPanel

class BottomPanel:
    def __init__(self, x:int, y:int, width:int, height:int, net_worth: float = 0, cash: float = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.net_worth = net_worth
        self.cash = cash

        self.to_draw = []
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((30, 30, 30))

        self.net_worth_panel = TextPanel(
            f"Net value: ${self.net_worth:.2f}", 10, 10, 230, 40
        )
        self.to_draw.append(self.net_worth_panel)

        self.cash_panel = TextPanel(
            f"Cash: ${self.cash:.2f}", 250, 10, 240, 40
        )
        self.to_draw.append(self.cash_panel)

    def update_data(self, new_net_worth: float | None, new_cash: float | None):
        if new_net_worth is not None:
            self.net_worth = new_net_worth
        if new_cash is not None:
            self.cash = new_cash
        self.net_worth_panel.change_text(f"Net value: ${self.net_worth:.2f}")
        self.cash_panel.change_text(f"Cash: ${self.cash:.2f}")

    def draw(self, screen):
        for to_draw in self.to_draw:
            to_draw.draw(self.surface)
        screen.blit(self.surface, (self.x, self.y))