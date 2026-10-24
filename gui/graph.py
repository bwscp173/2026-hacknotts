import math

import pygame
from datetime import datetime, timedelta

from get_me_data.loader import Stock

class Graph:
    """
    The trading graph that attaches to the screen
    """

    def __init__(self, width, height, data: Stock):
        self.surface = pygame.Surface((width, height))
        self.__stock = data

        y, m, d = self.__stock.get_latest_date()
        self.update(d, m, y, 30)


    def update(self, current_day: int, current_month: int, current_year: int, history_days: int):
        self.surface.fill((0, 0, 0))

        data_points = []
        min_value = math.inf
        max_value = -math.inf

        date_str = f"{current_year:04d}-{current_month:02d}-{current_day:02d}"
        for day in range(history_days):
            if self.__stock.has_date(date_str):
                data = self.__stock.get_date_for_date(date_str)
                data_points.append(data)

                for key in ("open", "high", "low", "close"):
                    value = data[key]

                    if value < min_value: min_value = value
                    if value > max_value: max_value = value
            else:
                data_points.append(None)

            parsed = datetime.strptime(date_str, "%Y-%m-%d")
            date_str = (parsed - timedelta(days=1)).strftime("%Y-%m-%d")

        day_width = (self.surface.get_width() - 40) / len(data_points)

        font = pygame.font.SysFont("monospace", 10)

        step = (max_value - min_value) / 5
        for i in range(6):
            y_offset = (self.surface.get_height() - 32) * (1 - (i/5))

            rect = font.render(str(round(min_value + (step * i), 1)), True, (255, 255, 255))

            self.surface.blit(
                rect, (1, y_offset)
            )

            pygame.draw.line(
                self.surface,
                (40, 40, 40),
                (40, y_offset+5),
                (self.surface.get_width(), y_offset+5)
            )

        date_str = f"{current_year:04d}-{current_month:02d}-{current_day:02d}"

        for i in range(history_days//7 + 1):
            pygame.draw.line(
                self.surface,
                (40, 40, 40),
                (40 + (i * 7 * day_width), 0),
                (40 + (i * 7 * day_width), self.surface.get_height()-27),
            )

            rect = font.render(date_str, True, (255, 255, 255))

            self.surface.blit(
                rect, (self.surface.get_width() - (((i+1) * 7 * day_width) - rect.get_width()), self.surface.get_height()-15)
            )

            parsed = datetime.strptime(date_str, "%Y-%m-%d")
            date_str = (parsed - timedelta(days=7)).strftime("%Y-%m-%d")

        y_change = max_value - min_value
        y_scale = (self.surface.get_height() - 32) / y_change
        y_offset = min_value

        last_average = 0

        x_offset = 40
        for i in range(len(data_points)-1, -1, -1):
            data_point = data_points[i]

            missing_data = False
            if data_point is None:
                x_offset += day_width
                continue

            values = [data_point["high"], data_point["low"], data_point["close"], data_point["open"]]
            values.sort()

            high_y = (values[0] - y_offset)  * y_scale
            low_y = (values[3]  - y_offset) * y_scale

            open_y = (values[1]  - y_offset) * y_scale
            close_y = (values[2]  - y_offset) * y_scale

            average = (low_y + high_y) / 2
            colour = (255, 0, 0) if average < last_average else (0, 255, 0)

            if missing_data:
                colour = (247, 152, 25)

            pygame.draw.rect(
                self.surface,
                colour,
                (
                    x_offset+1, self.surface.get_height() - close_y - 30,
                    day_width-2, abs(open_y - close_y)
                )
            )

            line_x = x_offset + (day_width // 2)
            pygame.draw.line(
                self.surface,
                colour,
                (line_x, self.surface.get_height() - close_y - 30),
                (line_x, self.surface.get_height() - low_y - 30),
            )

            pygame.draw.line(
                self.surface,
                colour,
                (line_x, self.surface.get_height() - open_y - 30),
                (line_x, self.surface.get_height() - high_y - 30),
            )


            last_average = average
            x_offset += day_width




    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
