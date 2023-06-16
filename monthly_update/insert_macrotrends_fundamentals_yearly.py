import os
import pandas as pd
import json
from findb import Database

timestamp_today = int(pd.to_datetime(pd.to_datetime("today").date()).timestamp())

db = Database()
con = db.connection
cur = db.cursor

tickers = os.listdir("fundamentals/yearly")
tickers = [ticker.strip(".json") for ticker in tickers]

for index, ticker in enumerate(tickers):
    print(f"{ticker}, {index} of {len(tickers)}")
    security_id = cur.execute("SELECT security_id FROM security WHERE ticker = ?", (ticker,)).fetchone()[0]
    with open(fr"fundamentals/yearly/{ticker}.json", "r") as f:
        dct = json.load(f)
    for statement in dct.keys():
        for variable, data in dct[statement].items():
            var_id = cur.execute("SELECT id from macrotrends_fundamental_variable WHERE name = ?", (variable,)).fetchone()[0]
            data = data.items()
            financial_data = []
            for date, value in data:
                date = pd.to_datetime(date)
                year = date.year
                timestamp =  int(date.timestamp())
                financial_data.append((security_id, var_id, 0, year, timestamp, value))
            cur.executemany("REPLACE INTO macrotrends_fundamental_data VALUES (?, ?, ?, ?, ?, ?)", financial_data)
    
    cur.execute("UPDATE company SET macrotrends_fundamentals_updated = ?, fiscal_year_end = ? WHERE security_id = ?", (timestamp_today, date.month, security_id))
    
con.commit()
con.close()


