from datetime import timedelta, datetime

import pygame
from random import randint

from get_me_data import loader
from gui.right_panel import RightPanel
from .bottom_panel import BottomPanel

from .graph import Graph
from bonsai_buddy.main_v2 import bonsai_buddy, Animation
import time
import pyautogui
pyautogui.PAUSE = 0.03


pygame.init()

from get_me_data.loader import Stock


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.current_date = "2000-02-01"  # idk if this is even valid
        # stock_name: {buy_price: float, is_selected: bool, total_stocks_owned: int, total_investment: float}
        self.stock_objects: list[Stock] = []
        self.stocks: dict[str, dict] = self.initialise_stock_list(self.current_date)
        self.cash = 10_000.00  # 10k
        self.volume_to_buy_or_sell = 0
        pygame.display.set_caption("Big money!!!!")

        self.running = False
        self.cut_off_date = "2003-01-01"

        self.frames_per_day = 60
        self.min_frames_per_day = 20

        self.days_per_decay = 6

        # TODO: add screen data

        self.graph = Graph(int(self.width * (5 / 8)), int(self.height * (5 / 8)), Stock("IBM"), self)

        def change_volume(amt: int):
            self.volume_to_buy_or_sell += amt
            if self.volume_to_buy_or_sell < 0:
                self.volume_to_buy_or_sell = 0
            print(f"Volume to buy/sell: {self.volume_to_buy_or_sell}")

        def purchase_stock(stock: str):
            self.purchase_or_sell_stock(stock, self.volume_to_buy_or_sell)

        def sell_stock(stock: str):
            self.purchase_or_sell_stock(stock, -self.volume_to_buy_or_sell)


        self.right_panel = RightPanel(
            int(self.width * (5 / 8)) + 20,
            10,
            int(self.width * (3 / 8)) - 30,
            self.height - 20,
            self.stocks,
            self.graph,
            change_volume,
            purchase_stock,
            sell_stock
        )
        self.bottom_panel = BottomPanel(10, int(self.height * (5 / 8)) + 20, int(self.width * (5 / 8)),
                                        int(self.height * (3 / 8)) - 30)

        # TODO: add individual buttons
        #    - stock selector to switch graph
        #    - volume to buy/sell stock
        #    - buy/sell button
        #    - banzibuddy interactions
        #    - current profit
        self.bottom_panel.update_data(self.cash, self.cash)
        self.bb = bonsai_buddy(self.screen)
        self.bb.set_location((600, 400))
        self.update_graph()

    def purchase_or_sell_stock(self, stock: str, quantity: int):
        print(f"Attempting to purchase/sell {quantity} of {stock}")
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer!")

        if not self.stocks.get(stock):
            print("Stock does not exist!")
            return

        if quantity > 0 and self.cash < self.stocks[stock]["buy_price"] * quantity:
            print("Not enough cash to buy stock!")
            return
        elif quantity < 0 and self.stocks[stock]["total_stocks_owned"] < abs(quantity):
            quantity = min(0, -self.stocks[stock]["total_stocks_owned"])
            print(f"Not enough stock to sell! Selling {abs(quantity)} instead.")

        self.cash -= self.stocks[stock]["buy_price"] * quantity
        self.stocks[stock]["total_stocks_owned"] += quantity
        self.stocks[stock]["total_investment"] += self.stocks[stock]["buy_price"] * quantity
        if quantity > 0:
            print(
                f"Bought {quantity} of {stock} for ${self.stocks[stock]['buy_price'] * quantity:.2f}. Cash left: ${self.cash:.2f}")
        else:
            print(
                f"Sold {abs(quantity)} of {stock} for ${self.stocks[stock]['buy_price'] * abs(quantity):.2f}. Cash left: ${self.cash:.2f}")

        self.bottom_panel.update_data(None, self.cash)

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
            self.stock_objects.append(stock)
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

    def next_day(self):
        parsed = datetime.strptime(self.current_date, "%Y-%m-%d")
        next_day = parsed + timedelta(days=1)
        self.current_date = next_day.strftime("%Y-%m-%d")
        self.increment_trading_day()
        self.update_graph()

        if self.current_date == self.cut_off_date:
            self.running = False
            self.end_screen_loop()


    def end_screen_loop(self):
        sub_running = True



        while sub_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sub_running = False


            pygame.display.flip()

    def increment_trading_day(self):
        total_stock_worth = 0
        for stock_obj in self.stock_objects:
            # {date (str): {open: float, high: float, low: float, close: float, volume: int}}
            self.stocks[stock_obj.symbol]["yesterday_price"] = self.stocks[stock_obj.symbol]["buy_price"]
            if stock_obj.has_date(self.current_date):
                self.stocks[stock_obj.symbol]["buy_price"] = stock_obj.generate_reasonable_price_for(self.current_date)

            total_stock_worth += self.stocks[stock_obj.symbol]["buy_price"] * self.stocks[stock_obj.symbol]["total_stocks_owned"]

        self.bottom_panel.update_data(self.cash + total_stock_worth, self.cash)

    def update_graph(self):
        parsed = datetime.strptime(self.current_date, "%Y-%m-%d")
        self.graph.update(parsed.day, parsed.month, parsed.year, 30)

    def fill(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.flip()

    def run(self):
        self.running = True

        target_x = None
        target_y = None
        STEALMOUSE = False
        step = 0

        frame_counter = 0
        day_counter = 0

        clock = pygame.time.Clock()

        while self.running:
            mouse_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_HASH:
                        self.bb.select_random_animation()

                    if event.key == pygame.K_RETURN:
                        self.bb.handle_animation()

                    if event.key == pygame.K_F1:
                        self.next_day()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = True

            if self.bb.can_do_event():
                response = self.bb.random_event()
                if response == "STEALMOUSE":
                    STEALMOUSE=True
                    response = None


            if STEALMOUSE:
                self.bb.draw(self.screen)
                        
                steps = 30
                target_x = randint(0, self.width)
                target_y = randint(0, self.height)
                drag_x, drag_y = pygame.mouse.get_pos()

                dy = (drag_y - target_y)/steps
                dx = (drag_x - target_x)/steps
                self.bb.set_animation(Animation.HOLD_HAND)

                if target_x is not None:
                    step += 1
                    drag_x -= dx
                    drag_y -= dy
                    pygame.mouse.set_pos(drag_x, drag_y)
                    pyautogui.click()
                    self.bb.handle_animation()
                    self.bb.set_location((drag_x-160, drag_y-80))
                    if int(target_x) == int(drag_x) or step >= steps:
                        target_x = None
                        target_y = None
                        step = 0
                        self.bb.set_animation(Animation.DEFAULT)
                        self.bb.handle_animation()
                        self.bb.set_location((600, 400))
                        STEALMOUSE = False

            self.bb.handle_animation()

            self.fill((20, 20, 20))
            self.graph.draw(self.screen, 10, 10)
            # I cannot be bothered to update on stock change
            self.right_panel.on_volume_change(self.volume_to_buy_or_sell)
            self.right_panel.draw(self.screen, pygame.mouse.get_pos(), mouse_pressed)
            self.bottom_panel.draw(self.screen)
            self.bb.draw(self.screen)
            self.update()

            clock.tick(30)
            frame_counter += 1

            if frame_counter >= self.frames_per_day:
                frame_counter = 0
                self.next_day()

                day_counter += 1

                if day_counter >= self.days_per_decay:
                    day_counter = 0
                    self.frames_per_day = max(self.min_frames_per_day, self.frames_per_day - 5)

        pygame.quit()

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
