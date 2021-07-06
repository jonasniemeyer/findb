import pandas as pd
import numpy as np
import os
from selenium import webdriver
import datetime as dt
import time
from finance_database import Database

ts_today = int((dt.date.today() - dt.date(1970,1,1)).total_seconds())
url = 'https://markets.cboe.com/tradeable_products/vix/vix_futures/'

db = Database()
con = db.connection
cur = db.cursor

if dt.date.today().weekday() != 6 and dt.date.today().weekday() != 0:
    date = dt.date.today() - dt.timedelta(days=1)
        
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    html = driver.execute_script("return document.body.innerHTML")
    driver.quit()

    df = pd.read_html(html)[0][1:]
    df['Expiration'] = pd.Series([dt.datetime.strptime(item, '%m/%d/%Y').date() for item in df['Expiration']], index=df.index)
    df.set_index('Expiration', inplace=True)
    df.index = pd.to_datetime(df.index).date
    for col in df.columns:
        if col in ('Last', 'High', 'Low', 'Settlement'):
            df[col] = df[col].apply(lambda x: np.NaN if x in (0, "-") else x)
        if col not in "Symbol":
            df[col] = pd.to_numeric(df[col])    

    df["ts"] = ts_today - 86_400
    df["ts maturity"] = [
        int((item - dt.date(1970,1,1)).total_seconds())
        for item in df.index
    ]

    data = df.reindex(columns = ["ts maturity", "ts", "Settlement", "Volume"]).values

    cur.executemany("INSERT INTO vix_prices VALUES (?, ?, ?, ?)", data)
    con.commit()
    con.close()

