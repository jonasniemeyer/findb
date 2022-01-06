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

for index, (security_id, ticker) in enumerate(securities):
    print(f"{ticker}, {index} of {len(securities)}")
    try:
        reader = YahooReader(ticker=ticker).historical_data(
            frequency="1d",
            start="1900-01-01",
            timestamps=False,
            rounded=False
        )
        df = reader["data"]
    except:
        print("\tfailed")
        cur.execute("UPDATE securities SET prices_updated = ? WHERE id = ?", (ts_today, security_id))
        continue

    currency = reader["information"]["currency"]
    try:
        currency_id = cur.execute("SELECT id FROM currencies WHERE abbr = ?", (currency, )).fetchone()[0]
    except:
        print("\t no currency", currency)
        continue
    df.index = [((date - dt.date(1970,1,1)).total_seconds()) for date in df.index]
    df["security id"] = security_id
    df["date"] = df.index
    data = df.reindex(columns = ["security id", "date", "open", "high", "low", "close", "adj close", "volume", "dividends", "stock splits", "simple returns", "log returns"]).values
    cur.executemany(
        "REPLACE INTO security_prices VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (data)
    )
    cur.execute("UPDATE securities SET prices_updated = ?, currency_id = ? WHERE id = ?", (ts_today, currency_id, security_id))
    if index % 100 == 0:
        con.commit()

con.commit()
con.close()