from finance_database import Database
from finance_data import CMEReader
import pandas as pd
import numpy as np
from sqlite3 import register_adapter
import datetime as dt

register_adapter(np.int64, lambda val: int(val))
register_adapter(np.float64, lambda val: float(val))

ts_today = int(pd.to_datetime(pd.to_datetime("today").date()).timestamp())

if dt.date.today().weekday() == 6:

    db = Database()
    con = db.connection
    cur = db.cursor

    data = {}
    for commodity in CMEReader.commodities.keys():
        data[commodity] = CMEReader(commodity, timestamps=True).read()

    for commodity in data.keys():
        commodity_id = cur.execute("SELECT id FROM commodities WHERE name = ?", (commodity,)).fetchone()[0]
        for ts in data[commodity].keys():
            df = data[commodity][ts]
            df["commodity_id"] = commodity_id
            df["maturity_ts"] = df.index
            df["ts"] = ts
            df = df[["commodity_id", "maturity_ts", "ts", "Settle", "Volume", "Open Interest"]].to_numpy()
            cur.executemany("REPLACE INTO commodity_prices VALUES (?, ?, ?, ?, ?, ?)", df)
        
        cur.execute("UPDATE commodities SET prices_updated = ? WHERE name = ?", (ts_today, commodity))

    con.commit()
    con.close()