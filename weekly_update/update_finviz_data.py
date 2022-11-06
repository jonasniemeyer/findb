from finance_data import FinvizReader
from finance_database import Database
import pandas as pd
import datetime as dt
from time import sleep

if dt.date.today().weekday() == 6:

    db = Database()
    con = db.connection
    cur = db.cursor

    tickers = cur.execute("SELECT ticker FROM securities WHERE discontinued IS NULL AND is_sec_company NOT NULL ORDER BY ticker").fetchall()
    tickers = [item[0] for item in tickers]
    length = len(tickers)

    for index, ticker in enumerate(tickers):
        if index % 100 == 0:
            con.commit()
        print(f"{index+1} of {length}: {ticker}")

        security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]

        fetched = False
        while not fetched:
            try:
                reader = FinvizReader(ticker)
                fetched = True
            except PermissionError:
                sleep(1)

        recommendations = reader.analyst_recommendations(timestamps=True)
        for rec in recommendations:
            ts = rec["date"]
            name = rec["company"]
            rating_old = rec["rating_old"]
            rating_new = rec["rating_new"]
            price_old = rec["price_old"]
            price_new = rec["price_new"]
            change = rec["change"]

            cur.execute("INSERT OR IGNORE INTO finviz_analyst_companies (name) VALUES (?)", (name,))
            analyst_id = cur.execute("SELECT id FROM finviz_analyst_companies WHERE name = ?", (name,)).fetchone()[0]
            
            if rating_old is None:
                old_id = None
            else:  
                cur.execute("INSERT OR IGNORE INTO finviz_ratings (name) VALUES (?)", (rating_old,))
                old_id = cur.execute("SELECT id FROM finviz_ratings WHERE name = ?", (rating_old,)).fetchone()[0]

            cur.execute("INSERT OR IGNORE INTO finviz_ratings (name) VALUES (?)", (rating_new,))
            new_id = cur.execute("SELECT id FROM finviz_ratings WHERE name = ?", (rating_new,)).fetchone()[0]

            cur.execute("INSERT OR IGNORE INTO finviz_ratings (name) VALUES (?)", (change,))
            change_id = cur.execute("SELECT id FROM finviz_ratings WHERE name = ?", (change,)).fetchone()[0]

            cur.execute(
                "REPLACE INTO finviz_analyst_recommendations VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (analyst_id, security_id, ts, old_id, new_id, change_id, price_old, price_new)
            )
        
        news = reader.news(timestamps=True)
        for article in news:
            ts = article["date"]
            source = article["source"]
            title = article["title"]
            url = article["url"]

            cur.execute("INSERT OR IGNORE INTO news_source (name) VALUES (?)", (source,))
            source_id = cur.execute("SELECT id FROM news_source WHERE name = ?", (source,)).fetchone()[0]

            type_id = cur.execute("SELECT id FROM news_type WHERE name = ?", ("News",)).fetchone()[0]

            cur.execute(
                """
                REPLACE INTO security_news (source_id, type_id, ts, header, url) VALUES (?, ?, ?, ?, ?)
                """,
                (source_id, type_id, ts, title, url)
            )
            news_id = cur.execute("SELECT id FROM security_news WHERE source_id = ? AND type_id = ? AND url = ?", (source_id, type_id, url)).fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO security_news_match VALUES (?, ?)", (security_id, news_id))

    con.commit()
    con.close()