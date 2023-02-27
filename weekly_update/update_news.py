from finance_database import Database
from finance_data import SANews, NasdaqNews
import datetime as dt

if dt.date.today().weekday() == 6:
    
    db = Database()
    con = db.connection
    cur = db.cursor

    tickers = cur.execute("SELECT security_id, ticker FROM security WHERE discontinued IS NULL AND is_sec_company NOT NULL ORDER BY ticker ASC").fetchall()

    cur.execute("INSERT OR IGNORE INTO news_source (name) VALUES (?)", ("Seeking Alpha",))
    cur.execute("INSERT OR IGNORE INTO news_type (name) VALUES (?)", (None,))

    length = len(tickers)
    trail = len(str(length))

    for index, (security_id, ticker) in enumerate(tickers):
        print(f"{index+1:>{trail}} of {length}: {ticker}")

        sa_news = SANews.rss_feed(ticker, timestamps=True)
        for item in sa_news:
            source_id = cur.execute("SELECT source_id FROM news_source WHERE name = ?", ("Seeking Alpha",)).fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO news_type (name) VALUES (?)", (item["type"],))
            news_type_id = cur.execute("SELECT type_id FROM news_type WHERE name = ?", (item["type"],)).fetchone()[0]
            cur.execute(
                """
                INSERT OR IGNORE INTO security_news (source_id, type_id, ts, header, url) VALUES (?, ?, ?, ?, ?)
                """,
                (source_id, news_type_id, item["datetime"], item["header"], item["url"])
            )
            news_id = cur.execute("SELECT news_id FROM security_news WHERE source_id = ? AND type_id = ? AND url = ?", (source_id, news_type_id, item["url"])).fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO security_news_match VALUES (?, ?)", (security_id, news_id))

        nasdaq_news = NasdaqNews.rss_feed(ticker, timestamps=True)
        for item in nasdaq_news:
            cur.execute("INSERT OR IGNORE INTO news_source (name) VALUES (?)", (item["source"],))
            source_id = cur.execute("SELECT source_id FROM news_source WHERE name = ?", (item["source"],)).fetchone()[0]
            news_type_id = cur.execute("SELECT type_id FROM news_type WHERE name IS NULL").fetchone()[0]
            cur.execute(
                """
                INSERT OR IGNORE INTO security_news (source_id, type_id, ts, header, description, url) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (source_id, news_type_id, item["datetime"], item["header"], item["description"], item["url"])
            )

            news_id = cur.execute("SELECT news_id FROM security_news WHERE source_id = ? AND type_id = ? AND url = ?", (source_id, news_type_id, item["url"])).fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO security_news_match VALUES (?, ?)", (security_id, news_id))
            for related_ticker in item["related_tickers"]:
                related_id = cur.execute("SELECT security_id FROM security WHERE ticker = ?", (related_ticker,)).fetchone()
                if related_id is not None:
                    cur.execute("INSERT OR IGNORE INTO security_news_match VALUES (?, ?)", (related_id[0], news_id))
        
        if index % 1000 == 0:
            con.commit()

    con.commit()
    con.close()