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


    def update(self, current_day: int, current_month: int, current_year: int, history_dats: int):
        self.surface.fill((0, 0, 0))

        data_points = []
        min_value = math.inf
        max_value = -math.inf

        date_str = f"{current_year:04d}-{current_month:02d}-{current_day:02d}"
        for day in range(history_dats):
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

        day_width = self.surface.get_width() / len(data_points)

        y_change = max_value - min_value
        y_scale = self.surface.get_height() / y_change
        y_offset = min_value

        last_average = 0
        last_datapoint = None

        x_offset = 0
        for i in range(len(data_points)-1, -1, -1):
            data_point = data_points[i]

            missing_data = False
            if data_point is None:
                x_offset += day_width
                continue

                data_point = last_datapoint
                missing_data = True

            values = [data_point["high"], data_point["low"], data_point["close"], data_point["open"]]
            values.sort()

            last_datapoint = data_point
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
                    x_offset, self.surface.get_height() - close_y,
                    day_width, abs(open_y - close_y)
                )
            )

            line_x = x_offset + (day_width // 2)
            pygame.draw.line(
                self.surface,
                colour,
                (line_x, self.surface.get_height() - close_y),
                (line_x, self.surface.get_height() - low_y),
            )

            pygame.draw.line(
                self.surface,
                colour,
                (line_x, self.surface.get_height() - open_y),
                (line_x, self.surface.get_height() - high_y),
            )


            last_average = average
            x_offset += day_width




    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
