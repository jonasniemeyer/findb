import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import datetime as dt
from finance_database import Database

db = Database()
con = db.connection
cur = db.cursor

base_url = "https://markets.cboe.com/us/futures/market_statistics/historical_data/"

html = requests.get(base_url).text
soup = BeautifulSoup(html, "lxml")
tags = soup.find_all("a", {"class": "link"})

urls = [base_url + tag.get("href") for tag in tags if "products/csv/VX" in tag.get("href")]

items = []
for url in urls:
    print(url)
    data = requests.get(url).text
    df = pd.read_csv(StringIO(data), index_col=0)
    df.index = pd.to_datetime(df.index)
    maturity_date = dt.date.fromisoformat(url.split("/")[-2])
    maturity_ts = int((maturity_date - dt.date(1970,1,1)).total_seconds())
    for index in df.index:
        ts = int((index.date() - dt.date(1970,1,1)).total_seconds())
        price = df.loc[index, "Settle"]
        volume = df.loc[index, "Total Volume"]
        if isinstance(price, pd.Series):
            price = price.iloc[0]
        items.append((maturity_ts, ts, price, volume))
cur.executemany(
    """
    INSERT INTO vix_prices VALUES(?, ?, ?, ?)
    """,
    items
)
con.commit()
con.close()

