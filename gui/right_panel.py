import pygame

from gui.button import Button
from gui.text_panel import TextPanel


class RightPanel:
    def __init__(self, x, y, width, height, current_stock):
        self.x = x
        self.y = y
        self.current_stock = current_stock
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill((200, 200, 200))
        self.to_draw = []
        self.volume_panel = TextPanel(
            "Volume to\nBuy/Sell", 10, self.height * 5 // 8 - 80, 120, 80
        )
        self.to_draw.append(self.volume_panel)

        do_plus_ten = lambda: print("Plus ten!")
        self.plus_ten = Button(
            x=140,
            y=self.height * 5 // 8 - 80,
            width=55,
            height=35,
            text="+10",
            call_on_click=do_plus_ten,
        )
        self.to_draw.append(self.plus_ten)

        do_minus_ten = lambda: print("Minus ten!")
        self.minus_ten = Button(
            x=205,
            y=self.height * 5 // 8 - 80,
            width=55,
            height=35,
            text="-10",
            call_on_click=do_minus_ten,
        )
        self.to_draw.append(self.minus_ten)

        do_plus_hundred = lambda: print("Plus hundred!")
        self.plus_hundred = Button(
            x=140,
            y=self.height * 5 // 8 - 35,
            width=55,
            height=35,
            text="+100",
            call_on_click=do_plus_hundred,
        )
        self.to_draw.append(self.plus_hundred)

        do_minus_hundred = lambda: print("Minus hundred!")
        self.minus_hundred = Button(
            x=205,
            y=self.height * 5 // 8 - 35,
            width=55,
            height=35,
            text="-100",
            call_on_click=do_minus_hundred,
        )
        self.to_draw.append(self.minus_hundred)

        self.buy_button = Button(
            x=10,
            y=self.height * 5 // 8 + 11,
            width=120,
            height=30,
            text="Buy",
            call_on_click=lambda: print("Buy button clicked"),
        )
        self.to_draw.append(self.buy_button)

        self.sell_button = Button(
            x=140,
            y=self.height * 5 // 8 + 11,
            width=120,
            height=30,
            text="Sell",
            call_on_click=lambda: print("Sell button clicked"),
        )
        self.to_draw.append(self.sell_button)

    def draw(self, screen, global_mouse, is_left_clicking: bool):
        local_mouse = (global_mouse[0] - self.x, global_mouse[1] - self.y)
        for element in self.to_draw:
            if isinstance(element, Button):
                element.draw(self.surface, local_mouse, is_left_clicking)
            elif isinstance(element, TextPanel):
                element.draw(self.surface)
            else:
                raise ValueError(f"Unknown element type: {type(element)}")
        screen.blit(self.surface, (self.x, self.y))
