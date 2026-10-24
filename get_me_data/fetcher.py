import requests
import dotenv
import os
import sqlite3
import time

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")
DB_PATH = os.getenv("DB_PATH")

if DB_PATH is None:
    raise Exception("No DB path provided")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL,
            date DATETIME NOT NULL,
            
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def fetch(symbol: str, year: int, month: int, interval: str = "5min"):
    time.sleep(1)
    month_string = f"{year:04d}-{month:02d}"

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&interval={interval}&month={month_string}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()


    print(data)

    trading_data = data['Time Series (Daily)']

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"Fetching {symbol} @ {month_string}... 0.0%", end="")
    for i, date in enumerate(trading_data.keys()):
        stat_open, stat_high, stat_low, stat_close, stat_volume = trading_data[date].values()
        cursor.execute("""
        INSERT INTO stocks (symbol, date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (symbol, date, stat_open, stat_high, stat_low, stat_close, stat_volume))

        print(f"\rFetching {symbol} @ {month_string}... {round(((i+1) / len(trading_data)) * 100, 1)}%", end="")

    conn.commit()
    conn.close()

    print(f"\rFetching {symbol} @ {month_string}... Done!  ")
