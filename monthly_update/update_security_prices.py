import datetime as dt
from finance_data import YahooReader
from finance_database import Database

ts_today = int((dt.date.today() - dt.date(1970, 1, 1)).total_seconds())

db = Database()
con = db.connection
cur = db.cursor

securities = cur.execute(
    """
    SELECT id, ticker FROM securities
    WHERE
    discontinued IS NULL
    ORDER BY ticker
    """
).fetchall()
length = len(securities)

for index, (security_id, ticker) in enumerate(securities):
    print(f"{ticker}, {index} of {length}")
    try:
        reader = YahooReader(ticker=ticker).historical_data(
            frequency="1d",
            timestamps=True
        )
        df = reader["data"]
    except:
        print("\tfailed")
        cur.execute("UPDATE securities SET prices_updated = ? WHERE id = ?", (ts_today, security_id))
        continue

    currency = reader["information"]["currency"]
    offset = reader["information"]["utc_offset"]
    try:
        currency_id = cur.execute("SELECT id FROM currencies WHERE abbr = ?", (currency, )).fetchone()[0]
    except:
        print("\t no currency", currency)
        continue
    df["security id"] = security_id
    df["ts"] = df.index
    data = df.reindex(columns = ["security id", "ts", "open", "high", "low", "close", "adj_close", "volume", "dividends", "splits", "simple_returns", "log_returns"]).values

    cur.executemany("REPLACE INTO security_prices VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    cur.execute("UPDATE securities SET prices_updated = ?, currency_id = ?, utc_offset = ? WHERE id = ?", (ts_today, currency_id, offset, security_id))
    if index % 100 == 0:
        con.commit()

con.commit()
con.close()