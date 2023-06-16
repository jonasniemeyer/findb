from findata import TipranksAnalystReader, TipranksStockReader
from findata.utils import DatasetError
from findb import Database
from findb.utils import HEADERS
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
    f"SELECT type_id FROM sec_form_type WHERE name IN {forms}",
).fetchall()
form_ids = tuple([item[0] for item in form_ids])

tickers = [item["ticker"] for item in db.companies()]
length = len(tickers)
trail = len(str(length))

for index, ticker in enumerate(tickers):
    if index % 100 == 0:
        con.commit()
    print(f"{index+1:{trail}} of {length}: {ticker}")

    reader = TipranksStockReader(ticker)

    security_id = cur.execute("SELECT security_id FROM security WHERE ticker = ?", (ticker,)).fetchone()[0]
    
    try:
        isin = reader.isin
        isin_stored = cur.execute("SELECT isin FROM security ticker = ?", (ticker,)).fetchone()[0]
        if isin_stored is None:
            cur.execute("UPDATE security SET isin = ? WHERE ticker = ?", (isin, ticker))
    except:
        pass

    #covering analysts
    try:
        analysts = reader.covering_analysts(include_retail=False, timestamps=True)
    except:
        pass
    else:
        for dct in analysts:
            rank_data = dct["analyst_ranking"]
            
            if dct["name"] is None:
                analyst_id = None
            else:
                cur.execute("INSERT OR IGNORE INTO tipranks_analyst (name) VALUES (?)", (dct["name"],))
                analyst_id = cur.execute("SELECT analyst_id FROM tipranks_analyst WHERE name = ?", (dct["name"],)).fetchone()[0]
            
            cur.execute("INSERT OR IGNORE INTO tipranks_analyst_company (name) VALUES (?)", (dct["company"],))
            company_id = cur.execute("SELECT company_id FROM tipranks_analyst_company WHERE name = ?", (dct["company"],)).fetchone()[0]

            if dct["image_url"] is None:
                image = b"\n"
            else:
                image = requests.get(url=dct["image_url"], headers=HEADERS).content

            cur.execute(
                """
                UPDATE tipranks_analyst SET image = ?, company_id = ?, rank = ?, stars = ?, successful_recommendations = ?,
                total_recommendations = ?, success_rate = ?, average_rating_return = ? WHERE analyst_id = ?
                """,
                (
                    image, company_id, rank_data["rank"], rank_data["stars"], rank_data["successful_recommendations"], rank_data["total_recommendations"],
                    rank_data["success_rate"], rank_data["average_rating_return"], analyst_id
                )
            )

            cur.execute(
                "REPLACE INTO tipranks_analyst_stock_summary VALUES (?, ?, ?, ?, ?, ?)",
                (analyst_id, security_id, dct["successful_recommendations_stock"], dct["total_recommendations_stock"], dct["success_rate_stock"], dct["average_rating_return_stock"])
            )

            for rating in dct["ratings"]:
                cur.execute("INSERT OR IGNORE INTO tipranks_analyst_recommendation (analyst_id, security_id, ts) VALUES (?, ?, ?)", (analyst_id, security_id, rating["date"]))
                cur.execute(
                    "UPDATE tipranks_analyst_recommendation SET price_target = ?, title = ?, url = ? WHERE analyst_id = ? AND security_id = ? AND ts = ?",
                    (rating["price_target"], rating["news_title"], rating["news_url"], analyst_id, security_id, rating["date"])
                )

    #recommendation trend
    try:
        analysts = reader.recommendation_trend(timestamps=True)["all_analysts"]
    except:
        pass
    else:
        for week, dct in analysts.items():
            cur.execute(
                "REPLACE INTO tipranks_recommendation_trend VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
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
                "REPLACE INTO tipranks_news_sentiment VALUES(?, ?, ?, ?, ?, ?, ?)",
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
                image = requests.get(url=dct["image_url"], headers=HEADERS).content
            
            cur.execute("INSERT OR IGNORE INTO tipranks_institutional (name, manager) VALUES (?, ?)", (dct["company"], dct["name"]))
            institutional_id = cur.execute("SELECT institutional_id FROM tipranks_institutional WHERE name = ? and manager = ?", (dct["company"], dct["name"])).fetchone()[0]

            cur.execute(
                "UPDATE tipranks_institutional SET image = ?, rank = ?, stars = ? WHERE name = ? AND manager = ?",
                (image, dct["rank"], dct["stars"], dct["company"], dct["name"])
            )
            cur.execute(
                "REPLACE INTO tipranks_institutional_holding VALUES (?, ?, ?, ?, ?, ?)",
                (institutional_id, security_id, ts_today_month_start, dct["value"], dct["change"], dct["percentage_of_portfolio"])
            )

    cur.execute("UPDATE company SET tipranks_data_updated = ? WHERE security_id = ?", (ts_today, security_id))

con.commit()

analysts = cur.execute("SELECT name FROM tipranks_analysts ORDER BY name").fetchall()
analysts = [item[0] for item in analysts]
length = len(analysts)

for index, analyst in enumerate(analysts):
    if index % 100 == 0:
        con.commit()
    print(f"{index} of {length}: {analyst}")

    reader = TipranksAnalystReader(analyst)

    # profile
    try:
        profile = reader.profile()
    except DatasetError:
        print("failed")
        continue
    cur.execute("INSERT OR IGNORE INTO tipranks_analysts (name) VALUES (?)", (profile["name"],))
    analyst_id = cur.execute("SELECT id FROM tipranks_analysts WHERE name = ?", (profile["name"],)).fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO tipranks_analyst_companies (name) VALUES (?)", (profile["company"], ))
    company_id = cur.execute("SELECT id FROM tipranks_analyst_companies WHERE name = ?", (profile["company"], )).fetchone()[0]

    if profile["image_url"] is None:
        image = b"\n"
    else:
        image = requests.get(url=profile["image_url"], headers=HEADERS).content

    if profile["sector"] is None:
        sector_id = None
    else:
        cur.execute("INSERT OR IGNORE INTO tipranks_sectors (name) VALUES (?)", (profile["sector"],))
        sector_id = cur.execute("SELECT id FROM tipranks_sectors WHERE name = ?", (profile["sector"],)).fetchone()[0]

    if profile["country"] is None:
        country_id = None
    else:
        cur.execute("INSERT OR IGNORE INTO tipranks_countries (name) VALUES (?)", (profile["country"],))
        country_id = cur.execute("SELECT id FROM tipranks_countries WHERE name = ?", (profile["country"],)).fetchone()[0]

    cur.execute(
        """
        UPDATE tipranks_analysts SET image = ?, analyst_company_id = ?, sector_id = ?, country_id = ?, rank = ?, successful_recommendations = ?,
        total_recommendations = ?, success_rate = ?, average_rating_return = ?, buy_percentage = ?, hold_percentage = ?, sell_percentage = ? WHERE id = ?
        """,
        (
            image, company_id, sector_id, country_id, profile["rank"], profile["successful_recommendations"], profile["total_recommendations"],
            profile["success_rate"], profile["average_rating_return"], profile["buy_percentage"], profile["hold_percentage"], profile["sell_percentage"], analyst_id
        )
    )

    # ratings
    ratings = reader.ratings(timestamps=True)
    for rating in ratings:
        security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (rating["ticker"],)).fetchone()
        if security_id is None:
            print(f"\tno security_id for ticker {rating['ticker']}")
            continue
        else:
            security_id = security_id[0]
        
        splits = cur.execute("SELECT ts, split_ratio FROM yahoo_security_prices WHERE security_id = ? AND split_ratio NOT NULL ORDER BY ts DESC", (security_id,)).fetchall()

        cur.execute("INSERT OR IGNORE INTO tipranks_ratings (name) VALUES (?)", (rating["rating"],))
        rating_id = cur.execute("SELECT id FROM tipranks_ratings WHERE name = ?", (rating["rating"],)).fetchone()[0]
    
        cur.execute("INSERT OR IGNORE INTO tipranks_ratings (name) VALUES (?)", (rating["change"],))
        change_id = cur.execute("SELECT id FROM tipranks_ratings WHERE name = ?", (rating["change"],)).fetchone()[0]

        cur.execute("INSERT OR IGNORE INTO tipranks_analyst_recommendations (analyst_id, security_id, ts) VALUES (?, ?, ?)", (analyst_id, security_id, rating["date"]))

        price_target = rating["price_target"]
        date = rating["date"]
        if price_target is not None:
            split_ratio = 1
            for item in splits:
                if date < item[0]:
                    split_ratio *= item[1]
            adjusted_target = price_target * split_ratio
        else:
            adjusted_target = None

        cur.execute(
            "UPDATE tipranks_analyst_recommendations SET rating_id = ?, change_id = ?, price_target = ? WHERE analyst_id = ? AND security_id = ? AND ts = ?",
            (rating_id, change_id, adjusted_target, analyst_id, security_id, date)
        )

con.commit()
con.close()