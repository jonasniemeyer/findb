import os
import datetime as dt
import json
from finance_database import Database

timestamp_today = int((dt.date.today() - dt.date(1970, 1, 1)).total_seconds())

db = Database()
con = db.connection
cur = db.cursor

tickers = os.listdir("fundamentals/yearly")
tickers = [ticker.strip(".json") for ticker in tickers]

for index, ticker in enumerate(tickers):
    print(f"{ticker}, {index} of {len(tickers)}")
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    with open(fr"fundamentals/yearly/{ticker}.json", "r") as f:
        dct = json.load(f)
    for statement in dct.keys():
        for variable, data in dct[statement].items():
            var_id = cur.execute("SELECT id from fundamental_variables_macrotrends WHERE name = ?", (variable,)).fetchone()[0]
            data = data.items()
            financial_data = []
            for date, value in data:
                date = dt.date.fromisoformat(date)
                year = date.year
                timestamp =  int((date - dt.date(1970, 1, 1)).total_seconds())
                financial_data.append((security_id, var_id, 0, year, timestamp, value))
            cur.executemany("REPLACE INTO fundamental_data_macrotrends VALUES (?, ?, ?, ?, ?, ?)", financial_data)
    
    cur.execute("UPDATE companies SET macrotrends_fundamentals_updated = ? WHERE security_id = ?", (timestamp_today, security_id))
    os.remove(f"fundamentals/yearly/{ticker}.json")
    
    if index % 100 == 0:
        con.commit()

con.close()


