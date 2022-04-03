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
    try:
        fiscal_year_end = cur.execute("SELECT ts FROM fundamental_data_macrotrends WHERE security_id = ? AND quarter = 0", (security_id,)).fetchone()[0]
    except:
        continue
    fiscal_year_end = pd.to_datetime(fiscal_year_end, unit="s")
    fiscal_year_end_quarter = fiscal_year_end.quarter
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
                quarter = (date.quarter+3-fiscal_year_end_quarter)%4+1
                year = year + 1 if (fiscal_year_end_quarter < 4 and date.quarter > fiscal_year_end_quarter) else year
                financial_data.append((security_id, var_id, quarter, year, timestamp, value))
            cur.executemany("REPLACE INTO fundamental_data_macrotrends VALUES (?, ?, ?, ?, ?, ?)", financial_data)
    
    cur.execute("UPDATE companies SET macrotrends_fundamentals_updated = ?, fiscal_year_end = ? WHERE security_id = ?", (timestamp_today, fiscal_year_end.month, security_id))
    
con.commit()
con.close()