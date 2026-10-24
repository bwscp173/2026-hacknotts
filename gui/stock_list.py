import pygame


class StockList:
    def __init__(self, stocks: dict[str, dict], x, y, width, height):
        # stock_name: {buy_price: float, yesterday_price: float, is_selected: bool, 
        # total_stocks_owned: int, total_investment: float}
        self.stocks = stocks
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.unselected_bg_colour = (255, 0, 0)
        self.selected_bg_colour = (0, 255, 0)

        self.font = pygame.font.SysFont("Monospace", (self.height//len(self.stocks))-4)
        self.font_small = pygame.font.SysFont("Monospace", (self.height // len(self.stocks)) // 2)

    def calc_diffs_to_yesterday(self):
        diffs = {}
        for stock in self.stocks:
            diffs[stock] = 100 * ((self.stocks[stock]["buy_price"] - self.stocks[stock]["yesterday_price"]) / self.stocks[stock]["yesterday_price"])
        return diffs

    def draw(self, screen, global_mouse, is_left_clicking):
        difs = self.calc_diffs_to_yesterday()
        for i, stock in enumerate(self.stocks):
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (self.x, self.y+(self.height//len(self.stocks)*i)+1, self.width, (self.height//len(self.stocks))-2),
            )

            name_rect = self.font.render(stock, True, (255, 255, 255))
            screen.blit(
                name_rect, (self.x, self.y+(self.height//len(self.stocks)*i))
            )

            current_price_rect = self.font_small.render(f"${self.stocks[stock]["buy_price"]:06.2f}", True, (255, 255, 255))
            screen.blit(
                current_price_rect, (self.x + 150 - current_price_rect.get_width(), self.y + (self.height // len(self.stocks) * i) + 1 + ((self.height // len(self.stocks)) - current_price_rect.get_height())//2)
            )

            dif = difs[stock]


            if dif > 0:
                colour = (0, 255, 0)
                char = "↑"

            elif dif == 0:
                colour = (200, 200, 200)
                char = " "
            else:
                colour = (255, 0, 0)
                char = "↓"

            text = f"{char}{dif:.2f}"

            dif_rect = self.font_small.render(text, True, colour)
            screen.blit(
                dif_rect, (self.x + 200,
                                     self.y + (self.height // len(self.stocks) * i) + 1 + ((self.height // len(
                                         self.stocks)) - dif_rect.get_height()) // 2)
            )


        
