from bs4 import BeautifulSoup
import sqlite3

DB_PATH = "../data_2000/stocks.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS stocks
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY,
                    symbol
                    TEXT
                    NOT
                    NULL,
                    date
                    DATETIME
                    NOT
                    NULL,

                    open
                    REAL
                    NOT
                    NULL,
                    high
                    REAL
                    NOT
                    NULL,
                    low
                    REAL
                    NOT
                    NULL,
                    close
                    REAL
                    NOT
                    NULL,
                    volume
                    REAL
                    NOT
                    NULL
                )
                """)

    conn.commit()
    conn.close()


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

init_db()

while True:
    symbol = input("Symbol: ")
    src = input("Source: ")

    soup = BeautifulSoup(src, "html.parser")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for element in soup.find_all("tr"):
        values = [
            child.text
            for child in element.children
        ][:-1]

        if not values[0][0].isdigit():
            continue

        if values[1] == " ":
            continue

        # Date, Open, High, Low, Closed, _, vol
        print(values)

        day_str, month_str, year_str = values[0].split()

        date_str = f"{int(year_str):04d}-{months.index(month_str)+1:02d}-{int(day_str):02d}"

        cursor.execute("""
                       INSERT INTO stocks (symbol, date, open, high, low, close, volume)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       """, (symbol, date_str, float(values[1]), float(values[2]), float(values[3]), float(values[4]), int(values[6].replace(",", ""))))


    conn.commit()
    conn.close()