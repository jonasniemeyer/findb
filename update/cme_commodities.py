import datetime as dt
from findb import Database
from findata import CMEReader
import numpy as np
import pandas as pd
from sqlite3 import register_adapter

def insert_commododity_data(db):
    register_adapter(np.int64, int)
    register_adapter(np.float64, float)
    ts_today = int(pd.to_datetime(pd.to_datetime("today").date()).timestamp())

    data = {}
    length = len(CMEReader.commodities)
    trail = len(str(length))

    for index, commodity in enumerate(CMEReader.commodities.keys()):
        print(f"{index+1:{trail}} of {length}: {commodity}")
        data[commodity] = CMEReader(commodity, timestamps=True).read()

    for commodity in data.keys():
        commodity_id = db.cur.execute("SELECT commodity_id FROM cme_commodity WHERE name = ?", (commodity,)).fetchone()[0]
        for ts in data[commodity].keys():
            df = data[commodity][ts]
            df["commodity_id"] = commodity_id
            df["maturity_ts"] = df.index
            df["ts"] = ts
            df = df[["commodity_id", "maturity_ts", "ts", "Settle", "Volume", "Open Interest"]]
            db.cur.executemany("REPLACE INTO cme_commodity_data VALUES (?, ?, ?, ?, ?, ?)", df.to_numpy())
        db.cur.execute("UPDATE cme_commodity SET prices_updated = ? WHERE name = ?", (ts_today, commodity))

    db.connection.commit()

if __name__ == "__main__":
    with Database() as db:
        insert_commododity_data()