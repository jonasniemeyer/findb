from finance_data import TipranksReader
from finance_database import Database
from finance_database.utils import headers
import pandas as pd
import requests

date_today = pd.to_datetime("today").date()
ts_today = int(pd.to_datetime(date_today).timestamp())
ts_today_month_start = int(pd.to_datetime(f"{date_today.year}-{date_today.month}-01").timestamp())

db = Database()
con = db.connection
cur = db.cursor

forms = (
    "10-K",
    "10-K405",
    "10-K/A",
    "10-K405/A",
    "10-Q",
    "10-Q405",
    "10-Q/A",
    "10-Q405/A",
    "20-F",
    "20-F/A",
    "6-K",
    "6-K/A"  
)

form_ids = cur.execute(
    f"SELECT id FROM form_types WHERE name IN {forms}",
).fetchall()
form_ids = tuple([item[0] for item in form_ids])

tickers = cur.execute(
    """
    SELECT ticker FROM securities
    WHERE
    discontinued IS NULL
    ORDER BY ticker
    """
).fetchall()
tickers = [item[0] for item in tickers]

length = len(tickers)
for index, ticker in enumerate(tickers):
    if index % 100 == 0:
        con.commit()
    print(ticker, index, "of", length)
    reader = TipranksReader(ticker)

    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    
    try:
        isin = reader.isin
        cur.execute("UPDATE securities SET isin = ? WHERE ticker = ?", (isin, ticker))
    except:
        pass

    #analysts
    try:
        analysts = reader.covering_analysts(include_retail=False, timestamps=True)
    except:
        pass
    else:
        for dct in analysts:
            rank_data = dct["analyst_ranking"]

            if dct["image_url"] is None:
                image = b"\n"
            else:
                image = requests.get(url=dct["image_url"], headers=headers).content
            
            cur.execute("INSERT OR IGNORE INTO analyst_companies_tipranks (name) VALUES (?)", (dct["company"], ))
            company_id = cur.execute("SELECT id FROM analyst_companies_tipranks WHERE name = ?", (dct["company"], )).fetchone()[0]

            cur.execute("INSERT OR IGNORE INTO analysts_tipranks (name) VALUES (?)", (dct["name"], ))
            analyst_id = cur.execute("SELECT id FROM analysts_tipranks WHERE name = ?", (dct["name"], )).fetchone()[0]

            cur.execute(
                """
                UPDATE analysts_tipranks SET image = ?, analyst_company_id = ?, rank = ?, stars = ?, successful_recommendations = ?,
                total_recommendations = ?, percentage_successful_recommendations = ?, average_rating_return = ? WHERE id = ?
                """,
                (
                    image, company_id, rank_data["rank"], rank_data["stars"], rank_data["successful_recommendations"], rank_data["total_recommendations"],
                    rank_data["percentage_successful_recommendations"], rank_data["average_rating_return"], analyst_id
                )
            )

            cur.execute(
                "REPLACE INTO analyst_stock_summary_tipranks VALUES (?, ?, ?, ?, ?, ?)",
                (analyst_id, security_id, dct["stock_success_rate"], dct["average_rating_return_stock"], dct["total_recommendations_stock"], dct["positive_recommendations_stock"])
            )

            for rating in dct["ratings"]:
                cur.execute(
                    "REPLACE INTO analyst_recommendations_tipranks VALUES (?, ?, ?, ?, ?, ?)",
                    (analyst_id, security_id, rating["date"], rating["price_target"], rating["news_title"], rating["news_url"])
                )

    #recommendation trend
    try:
        analysts = reader.recommendation_trend(timestamps=True)["all_analysts"]
    except:
        pass
    else:
        for week, dct in analysts.items():
            cur.execute(
                "REPLACE INTO recommendation_trend_tipranks VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (security_id, week, dct["count"], dct["average"], dct["buy"], dct["hold"], dct["sell"], dct["average_price_target"])
            )
    
    #news sentiment
    try:
        sentiment = reader.news_sentiment(timestamps=True)["articles"]
    except:
        pass
    else:
        for dct in sentiment:
            cur.execute(
                "REPLACE INTO news_sentiment_tipranks VALUES(?, ?, ?, ?, ?, ?, ?)",
                (security_id, dct["week"], dct["count"], dct["average"], dct["buy"], dct["hold"], dct["sell"])
            )

    #institutional ownership
    try:
        ownership = reader.institutional_ownership()
    except:
        pass
    else:
        for dct in ownership:
            if dct["image_url"] is None:
                image = b"\n"
            else:
                image = requests.get(url=dct["image_url"], headers=headers).content
            
            cur.execute("INSERT OR IGNORE INTO institutionals_tipranks (name, manager) VALUES (?, ?)", (dct["company"], dct["name"]))
            institutional_id = cur.execute("SELECT id FROM institutionals_tipranks WHERE name = ? and manager = ?", (dct["company"], dct["name"])).fetchone()[0]

            cur.execute(
                "UPDATE institutionals_tipranks SET image = ?, rank = ?, stars = ? WHERE name = ? AND manager = ?",
                (image, dct["rank"], dct["stars"], dct["company"], dct["name"])
            )
            cur.execute(
                "REPLACE INTO institutional_holdings_tipranks VALUES (?, ?, ?, ?, ?, ?)",
                (institutional_id, security_id, ts_today_month_start, dct["value"], dct["change"], dct["percentage_of_portfolio"])
            )

    cur.execute("UPDATE companies SET tipranks_data_updated = ? WHERE security_id = ?", (ts_today, security_id))

con.commit()
con.close()