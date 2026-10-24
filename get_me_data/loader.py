import dotenv
from random import random, randrange
import os
import sqlite3

from datetime import datetime

dotenv.load_dotenv()

DB_PATH = os.getenv("DB_PATH")

if DB_PATH is None:
    raise Exception("No DB path provided")


def get_symbols():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT symbol FROM stocks")
    results = cursor.fetchall()

    conn.close()

    return [result[0] for result in results]


class Stock:
    def __init__(self, symbol):
        self.__symbol = symbol

        # {date (str): {open: float, high: float, low: float, close: float, volume: int}}
        self.__data = {}
        self.__load()

    def get_dates(self):
        return list(self.__data.keys())

    def dates(self):
        """Iterates over all dates / months"""
        for date in self.get_dates():
            yield date

        return

    def get_date_for_date(self, date):
        return self.__data[date]

    def has_date(self, date_string):
        return date_string in self.__data

    def __load(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM stocks WHERE symbol = ?", (self.__symbol,))
        results = cursor.fetchall()

        conn.close()

        self.__data = {
            date: {
                "open": s_open,
                "high": s_high,
                "low": s_low,
                "close": s_close,
                "volume": s_volume,
            }
            for _, __, date, s_open, s_high, s_low, s_close, s_volume in results
        }

    def get_latest_date(self):
        date_str = list(self.__data.keys())[0]

        datetime_date = datetime.strptime(date_str, "%Y-%m-%d")
        return datetime_date.year, datetime_date.month, datetime_date.day

    def generate_reasonable_price_for(self, date: str):
        return round(self.__data[date]["low"] + self.__data[date]["high"] / 2, 2)
