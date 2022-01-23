from finance_database import Database
from finance_data import RSSReader
import datetime as dt

if dt.date.today().weekday() == 6:
    
    db = Database()
    con = db.connection
    cur = db.cursor

    tickers = cur.execute("SELECT id, ticker FROM securities WHERE discontinued IS NULL ORDER BY ticker ASC").fetchall()

    cur.execute("INSERT OR IGNORE INTO news_source (name) VALUES (?)", ("seeking alpha",))
    source_id = cur.execute("SELECT id FROM news_source WHERE name = ?", ("seeking alpha",)).fetchone()[0]

    length = len(tickers)

    for index, (security_id, ticker) in enumerate(tickers):
        print(f"{index} of {length}: {ticker}")
        news = RSSReader.seekingalpha(ticker, timestamps=True)
        for item in news:
            header = item["header"]
            url = item["url"]
            ts = item["date"]
            news_type = item["type"]
            cur.execute("INSERT OR IGNORE INTO news_type (name) VALUES (?)", (news_type,))
            type_id = cur.execute("SELECT id FROM news_type WHERE name = ?", (news_type,)).fetchone()[0]
            cur.execute(
                """
                INSERT OR IGNORE INTO security_news (source_id, type_id, ts, header, url) VALUES (?, ?, ?, ?, ?)
                """,
                (source_id, type_id, ts, header, url)
            )
            news_id = cur.execute("SELECT id FROM security_news WHERE source_id = ? AND type_id = ? AND url = ?", (source_id, type_id, url)).fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO security_news_match VALUES (?, ?)", (security_id, news_id))
        
        if index % 1000 == 0:
            con.commit()

    con.commit()
    con.close()