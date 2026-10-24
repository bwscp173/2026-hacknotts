import pygame

from get_me_data import loader
from gui.right_panel import RightPanel

from .graph import Graph

pygame.init()

from get_me_data.loader import Stock


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.current_date = "2002-12-17"  # idk if this is even valid
        # stock_name: {buy_price: float, is_selected: bool, total_stocks_owned: int, total_investment: float}
        self.stocks: dict[str, dict] = self.initialise_stock_list(self.current_date)
        pygame.display.set_caption("Big money!!!!")

        self.graph = Graph(
            int(self.width * (5 / 8)), int(self.height * (5 / 8)), Stock("AMD")
        )
        self.right_panel = RightPanel(
            int(self.width * (5 / 8)) + 20,
            10,
            int(self.width * (3 / 8)) - 30,
            self.height - 20,
            self.stocks,
        )

        # TODO: add individual buttons
        #    - stock selector to switch graph
        #    - volume to buy/sell stock
        #    - buy/sell button
        #    - banzibuddy interactions
        #    - current profit

    def initialise_stock_list(self, date):
        """
        stock_name: {buy_price: float, yesterday_price: float, is_selected: bool,
        total_stocks_owned: int, total_investment: float}
        since you can't have bought anything before the first day (right?)
        """
        stock_syms = loader.get_symbols()
        stocks = {}
        has_selected = False
        for sym in stock_syms:
            stock = loader.Stock(sym)  # this is so slow  TODO: fix?
            stocks[sym] = {}
            stocks[sym]["buy_price"] = stock.generate_reasonable_price_for(date)
            stocks[sym]["yesterday_price"] = stocks[sym][
                "buy_price"
            ]  # so it says +0.00% day 1
            stocks[sym]["is_selected"] = not has_selected
            has_selected = True
            stocks[sym]["total_stocks_owned"] = 0.0
            stocks[sym]["total_investment"] = 0.0

        return stocks

    def fill(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            mouse_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = True

            self.fill((255, 255, 255))
            self.graph.draw(self.screen, 10, 10)
            self.right_panel.draw(self.screen, pygame.mouse.get_pos(), mouse_pressed)
            self.update()

        pygame.quit()

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
