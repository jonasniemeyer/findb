import os
import pandas as pd
import json
from finance_database import Database

timestamp_today = int(pd.to_datetime(pd.to_datetime("today").date()).timestamp())

db = Database()
con = db.connection
cur = db.cursor

tickers = os.listdir("fundamentals/quarterly")
tickers = [ticker.strip(".json") for ticker in tickers]

for index, ticker in enumerate(tickers):
    print(f"{ticker}, {index} of {len(tickers)}")
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    with open(fr"fundamentals/quarterly/{ticker}.json", "r") as f:
        dct = json.load(f)
    for statement in dct.keys():
        for variable, data in dct[statement].items():
            var_id = cur.execute("SELECT id from fundamental_variables_macrotrends WHERE name = ?", (variable,)).fetchone()[0]
            data = data.items()
            financial_data = []
            for date, value in data:
                date = pd.to_datetime(date)
                year = date.year
                timestamp =  int(date.timestamp())
                try:
                    fiscal_year_end = cur.execute("SELECT ts FROM fundamental_data_macrotrends WHERE security_id = ? AND quarter = 0", (security_id,)).fetchone()[0]
                except:
                    break
                fiscal_year_end = pd.to_datetime(fiscal_year_end, unit="s")
                quarter = int(((date.month-fiscal_year_end.month)/3 + 3) % 4 + 1)
                date.month - fiscal_year_end.month
                financial_data.append((security_id, var_id, quarter, year, timestamp, value))
            cur.executemany("REPLACE INTO fundamental_data_macrotrends VALUES (?, ?, ?, ?, ?, ?)", financial_data)
    
    cur.execute("UPDATE companies SET macrotrends_fundamentals_updated = ? WHERE security_id = ?", (timestamp_today, security_id))
    #os.remove(f"fundamentals/quarterly/{ticker}.json")
    
con.commit()
con.close()