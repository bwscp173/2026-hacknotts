from typing import Callable

import pygame

from get_me_data import loader
from gui.button import Button
from gui.text_panel import TextPanel
from gui.stock_list import StockList

class RightPanel:
    def __init__(self, x, y, width, height, stocks, graph, dec_or_inc_volume: Callable, purchase: Callable, sell: Callable):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))

        self.surface.fill((30, 30, 30))
        self.to_draw = []

        self.stocks_list = StockList(stocks, graph, 525, 15, 260, 250)

        self.volume_panel = TextPanel(
            "Volume to\nBuy/Sell", 10, self.height * 5 // 8 - 80, 120, 80
        )
        self.to_draw.append(self.volume_panel)

        self.plus_ten = Button(
            x=140,
            y=self.height * 5 // 8 - 80,
            width=55,
            height=35,
            text="+10",
            call_on_click=lambda: dec_or_inc_volume(10)
        )
        self.to_draw.append(self.plus_ten)

        self.minus_ten = Button(
            x=205,
            y=self.height * 5 // 8 - 80,
            width=55,
            height=35,
            text="-10",
            call_on_click=lambda : dec_or_inc_volume(-10)
        )
        self.to_draw.append(self.minus_ten)

        self.plus_hundred = Button(
            x=140,
            y=self.height * 5 // 8 - 35,
            width=55,
            height=35,
            text="+100",
            call_on_click=lambda: dec_or_inc_volume(100),
        )

        self.to_draw.append(self.plus_hundred)

        self.minus_hundred = Button(
            x=205,
            y=self.height * 5 // 8 - 35,
            width=55,
            height=35,
            text="-100",
            call_on_click=lambda: dec_or_inc_volume(-100),
        )
        self.to_draw.append(self.minus_hundred)

        self.buy_button = Button(
            x=10,
            y=self.height * 5 // 8 + 11,
            width=120,
            height=30,
            text="Buy",
            call_on_click=lambda: purchase(self.stocks_list.get_selected_stock()),
        )
        self.to_draw.append(self.buy_button)

        self.sell_button = Button(
            x=140,
            y=self.height * 5 // 8 + 11,
            width=120,
            height=30,
            text="Sell",
            call_on_click=lambda: sell(self.stocks_list.get_selected_stock()),
        )
        self.to_draw.append(self.sell_button)

    def on_volume_change(self, new_quantity: int):
        self.volume_panel.change_text(f"{new_quantity}\n${new_quantity * self.stocks_list.get_cur_stock_buy():.2f}")

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
        self.stocks_list.draw(screen, global_mouse, is_left_clicking)
