from finance_database import Database
from finance_data import CMEReader
import pandas as pd
import datetime as dt

ts_today = int(pd.to_datetime(pd.to_datetime("today").date()).timestamp())

if dt.date.today().weekday() == 5:

    db = Database()
    con = db.connection
    cur = db.cursor

    data = {}
    for commodity in CMEReader.commodities.keys():
        data[commodity] = CMEReader(commodity, timestamps=True).read()

    for commodity in data.keys():
        if commodity != "Cotton":
            continue
        commodity_id = cur.execute("SELECT id FROM commodities WHERE name = ?", (commodity,)).fetchone()[0]
        for ts in data[commodity].keys():
            df = data[commodity][ts]
            df["commodity_id"] = commodity_id
            df["maturity_ts"] = df.index
            df["ts"] = ts
            df = df[["commodity_id", "maturity_ts", "ts", "Settle", "Volume", "Open Interest"]].to_numpy()
            cur.executemany("REPLACE INTO commodit_prices VALUES (?, ?, ?, ?, ?, ?)", df)

    con.commit()
    con.close()