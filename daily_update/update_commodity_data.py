import pandas as pd
from selenium import webdriver
import numpy as np
import re
import datetime as dt
import time
from finance_database import Database, variables

ts_today = int((dt.date.today() - dt.date(1970,1,1)).total_seconds())

db = Database()
con = db.connection
cur = db.cursor

if dt.date.today().weekday() != 6 and dt.date.today().weekday() != 0:
    commodities = variables.commodities
    for comm in commodities:
        print(comm)
        if cur.execute("SELECT prices_updated FROM commodities WHERE name = ?", (comm, )).fetchone()[0] != ts_today:
            url = "https://www.cmegroup.com/trading/{}/{}/{}_quotes_globex.html".format(
                commodities[comm]["sector"], 
                commodities[comm]["group"],
                commodities[comm]["name"]
            )
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(1)
            html = driver.execute_script("return document.body.innerHTML")
            driver.quit()

            df = pd.read_html(html)[0]
            df.set_index("Month", inplace=True)
            df.index.name = "Months"
            df.index = [
                dt.datetime.strptime(item[:8].lower(), "%b %Y").date() for item in df.index
            ]

            if "PriorSettle" in df.columns:
                df = df.rename(columns = {"PriorSettle": "Prior Settle"})

            df = df[["Last", "Change", "Prior Settle", "Open", "High", "Low", "Volume"]]

            for col in df.columns:
                if col == "Change":
                    df[col] = df[col].apply(lambda x: re.sub("(.+)\(.+\)", r"\1", x))
                df[col] = df[col].apply(lambda x: np.NaN if x == "-" else x)
                df[col] = df[col].apply(lambda x: 0 if isinstance(x, str) and "UNCH" in x else x)
                df[col] = df[col].apply(lambda x: x.replace("'", "") if isinstance(x, str) else x)
                df[col] = pd.to_numeric(df[col])

            df["year"] = [item.year for item in df.index]
            df["month"] = [item.month for item in df.index]
            df["ts"] = ts_today - 86_400
            df["id"] = cur.execute("SELECT id FROM commodities WHERE name = ?", (comm,)).fetchone()[0]
            df["ts maturity"] = [
                int((dt.date(item.year, item.month, 1) - dt.date(1970,1,1)).total_seconds())
                for item in df.index
            ]

            data = df.reindex(columns = ["id", "month", "year", "ts maturity", "ts", "Prior Settle", "Volume"]).values

            cur.executemany("INSERT INTO commodity_prices VALUES (?, ?, ?, ?, ?, ?, ?)", data)
            cur.execute("UPDATE commodities SET prices_updated = ? WHERE name = ?", (ts_today, comm))
            con.commit()
    con.close()
