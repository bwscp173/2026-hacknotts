
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

    def calc_diffs_to_yesterday(self):
        diffs = {}
        for stock in self.stocks:
            diffs[stock] = (self.stocks[stock]["buy_price"] - self.stocks[stock]["yesterday_price"]) / self.stocks[stock]["yesterday_price"]
        return diffs

    def draw(self, screen, global_mouse, is_left_clicking):
        
