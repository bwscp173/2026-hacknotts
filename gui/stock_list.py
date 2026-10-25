import pygame

from get_me_data.loader import Stock
from gui.graph import Graph


class StockList:
    def __init__(self, stocks: dict[str, dict], graph, x, y, width, height):
        # stock_name: {buy_price: float, yesterday_price: float, is_selected: bool, 
        # total_stocks_owned: int, total_investment: float}
        self.stocks = stocks
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graph = graph

        self.unselected_bg_colour = (255, 0, 0)
        self.selected_bg_colour = (0, 255, 0)

        self.font = pygame.font.Font("fonts/IBMPlexMono-Regular.ttf", (self.height//len(self.stocks))-4)
        self.font_small = pygame.font.Font("fonts/IBMPlexMono-Regular.ttf", (self.height // len(self.stocks)) // 2)

    def calc_diffs_to_yesterday(self):
        diffs = {}
        for stock in self.stocks:
            diffs[stock] = 100 * ((self.stocks[stock]["buy_price"] - self.stocks[stock]["yesterday_price"]) / self.stocks[stock]["yesterday_price"])
        return diffs

    def get_selected_stock(self):
        for stock in self.stocks:
            if self.stocks[stock]["is_selected"]:
                return stock
        raise ValueError("No selected stock??????")

    def get_cur_stock_buy(self):
        stock_str = self.get_selected_stock()
        return self.stocks[stock_str]["buy_price"]

    def set_selected_stock(self, symbol: str):
        for stock_vals in self.stocks.values():
            stock_vals["is_selected"] = False
        self.stocks[symbol]["is_selected"] = True
        self.graph.change_stock(Stock(symbol))

    def draw(self, screen, global_mouse, is_left_clicking):
        difs = self.calc_diffs_to_yesterday()
        for i, stock in enumerate(self.stocks):
            collision_rect = pygame.Rect(
                self.x, self.y+(self.height//len(self.stocks)*i)+1,
                self.width, (self.height//len(self.stocks))-2
            )

            bg_colour = (50, 50, 50)
            if collision_rect.collidepoint(*global_mouse):
                if is_left_clicking:
                    self.set_selected_stock(stock)

                bg_colour = (70, 70, 70)

            if stock == self.graph.symbol():
                bg_colour = (80, 80, 80)

            pygame.draw.rect(
                screen,
                bg_colour,
                collision_rect,
            )


            name_rect = self.font_small.render(stock, True, (255, 255, 255))
            screen.blit(
                name_rect, (self.x+2, self.y+(self.height//len(self.stocks)*i)+5)
            )

            current_price_rect = self.font_small.render(f"${self.stocks[stock]["buy_price"]:06.2f}", True,
                                                        (255, 255, 255))
            screen.blit(
                current_price_rect, (
                    self.x + 120 - current_price_rect.get_width(),
                    self.y + (self.height // len(self.stocks) * i) + 1 + ((self.height // len(self.stocks)) - current_price_rect.get_height()) // 2)
            )

            dif = difs[stock]
            if dif > 0:
                colour = (74,246,195)
                char = "↑"

            elif dif == 0:
                colour = (200, 200, 200)
                char = " "
            else:
                colour = (255,67,61)
                char = "↓"

            text = f"{char}{abs(dif):.2f}"

            dif_rect = self.font_small.render(text, True, colour)
            screen.blit(
                dif_rect, (self.x + 130,
                                     self.y + (self.height // len(self.stocks) * i) + 1 + ((self.height // len(
                                         self.stocks)) - dif_rect.get_height()) // 2)
            )

            amt_owned = int(self.stocks[stock]["total_stocks_owned"])
            amt_owned_rect = self.font_small.render(f"{amt_owned}x", True, (255, 255, 255))
            screen.blit(
                amt_owned_rect, (self.x + 255 - amt_owned_rect.get_width(),
                                 self.y + (self.height // len(self.stocks) * i) + 1 + ((self.height // len(
                                     self.stocks)) - amt_owned_rect.get_height()) // 2)
            )



