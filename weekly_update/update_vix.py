import datetime as dt
import json
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from finance_database import Database
from io import StringIO
from sqlite3 import register_adapter

register_adapter(np.int64, lambda val: int(val))
register_adapter(np.float64, lambda val: float(val))

db = Database()
con = db.connection
cur = db.cursor

base_url = "https://markets.cboe.com/us/futures/market_statistics/historical_data/"

html = requests.get(base_url).text
url_dict = html.split("TX.defaultProductList = ")[1].split("CTX.productTypes = ")[0]
url_dict = json.loads(url_dict)

urls = [f"https://cdn.cboe.com/{item['path']}" for year in url_dict for item in url_dict[year]]
length = len(urls)
trail = len(str(length))

for index, url in enumerate(urls):
    items = []
    print(f"{index+1: >{trail}} of {length}: {url}")
    data = requests.get(url).text
    df = pd.read_csv(StringIO(data), index_col=0)
    df.index = pd.to_datetime(df.index)
    maturity_date = dt.date.fromisoformat(url.split("/")[-1].split("VX_")[1].split(".csv")[0])
    maturity_ts = int((maturity_date - dt.date(1970,1,1)).total_seconds())
    for index in df.index:
        ts = int((index.date() - dt.date(1970,1,1)).total_seconds())
        price = df.loc[index, "Settle"]
        volume = df.loc[index, "Total Volume"]
        if isinstance(price, pd.Series): #some data is duplicate
            price = price.iloc[0]
            volume = volume.iloc[0]
        items.append((maturity_ts, ts, price, volume))
    cur.executemany(
        """
        REPLACE INTO cboe_vix_data VALUES(?, ?, ?, ?)
        """,
        items
    )
con.commit()
con.close()

