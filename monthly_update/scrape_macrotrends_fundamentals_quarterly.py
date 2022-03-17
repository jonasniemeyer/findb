from finance_data import MacrotrendsReader
from finance_database import Database
import os
import json
import concurrent.futures
import selenium

db = Database()
con = db.connection
cur = db.cursor

tickers = cur.execute("SELECT ticker FROM securities WHERE id IN (SELECT security_id FROM companies) ORDER BY ticker ASC").fetchall()
tickers = [item[0] for item in tickers]

def scrape_data(ticker):
    if f"{ticker}.json" in os.listdir("fundamentals/quarterly"):
        return
    reader = MacrotrendsReader(ticker, frequency="Q")
    try:
        data = reader.read()
    except:
        data = {}
    with open(f"fundamentals/quarterly/{ticker}.json", "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    print(len(tickers))
    if not os.path.exists("fundamentals/quarterly"):
        os.mkdir("fundamentals/quarterly")
    with concurrent.futures.ProcessPoolExecutor(4) as p:
        p.map(scrape_data, tickers)
