import pygame

from gui.button import Button


class RightPanel:
    def __init__(self, x, y, width, height, current_stock):
        self.x = x
        self.y = y
        self.current_stock = current_stock
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill((200, 200, 200))
        # self.volume_size_panel =
        self.buy_button = Button(
            x=10,
            y=self.height * 5 // 8 + 11,
            width=80,
            height=30,
            text="Buy",
            call_on_click=lambda: print("Buy button clicked"),
        )
        self.sell_button = Button(
            x=10,
            y=self.height * 5 // 8 + 51,
            width=80,
            height=30,
            text="Sell",
            call_on_click=lambda: print("Sell button clicked"),
        )

    def draw(self, screen, mouse, is_left_clicking: bool):
        self.buy_button.draw(
            self.surface, ((mouse[0] - self.x), (mouse[1] - self.y)), is_left_clicking
        )
        self.sell_button.draw(
            self.surface, ((mouse[0] - self.x), (mouse[1] - self.y)), is_left_clicking
        )
        screen.blit(self.surface, (self.x, self.y))
