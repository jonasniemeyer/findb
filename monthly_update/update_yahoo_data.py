from finance_data import YahooReader
from finance_data.utils import TickerError, DatasetError
from finance_database import Database
import pandas as pd
from dateutil.relativedelta import relativedelta
import time

def update_yahoo_data(reader: YahooReader, db: Database) -> None:
    security_id = db.cur.execute("SELECT security_id FROM security WHERE ticker = ?", (reader.ticker,)).fetchone()[0]
    ts_today = int(pd.to_datetime(pd.to_datetime("today").date()).timestamp())

    db.cur.execute("INSERT OR IGNORE INTO yahoo_security_type (name) VALUES (?)", (reader.security_type,))
    type_id = db.cur.execute("SELECT type_id FROM yahoo_security_type WHERE name = ?", (reader.security_type,)).fetchone()[0]

    logo = reader.logo()
    try:
        description = reader.profile()["description"]
    except:
        description = None

    db.cur.execute(
        "UPDATE security SET yahoo_name = ?, logo = ?, type_id = ?, description = ? WHERE security_id = ?",
        (reader.name, logo, type_id, description, security_id)
    )

    if reader.security_type == "EQUITY":
        db.cur.execute("INSERT OR IGNORE INTO company (security_id) VALUES (?)", (security_id,))
        update_yahoo_profile(reader, db)
        update_yahoo_executives(reader, db)
        update_yahoo_fundamentals(reader, db)
        update_yahoo_analyst_recommendations(reader, db)
        update_yahoo_recommendation_trend(reader, db)
        db.cur.execute("UPDATE company SET yahoo_data_updated = ? WHERE security_id = ?", (ts_today, security_id))

    db.cur.execute("UPDATE security SET profile_updated = ? WHERE security_id = ?", (ts_today, security_id))

    try:
        update_yahoo_prices(reader, db)
    except DatasetError:
        print(f'Could not fetch prices for security with ticker "{reader.ticker}"')

def update_yahoo_profile(reader: YahooReader, db: Database) -> None:
    profile = reader.profile()

    security_id = db.cur.execute("SELECT security_id FROM security WHERE ticker = ?", (reader.ticker,)).fetchone()[0]

    data = {}
    for var in (
        "website",
        "country",
        "city",
        "address1",
        "address2",
        "address3",
        "zip",
        "employees",
        "industry",
        "sector"
    ):
        try:
            data[var] = profile[var]
        except:
            data[var] = None

    #industry
    if data["industry"] is None:
        industry_id = None
    else:
        db.cur.execute("INSERT OR IGNORE INTO yahoo_gics_sector (name) VALUES (?)", (data["sector"],))
        sector_id = db.cur.execute("SELECT sector_id FROM yahoo_gics_sector WHERE name = ?", (data["sector"],)).fetchone()[0]
        db.cur.execute("INSERT OR IGNORE INTO yahoo_gics_industry (name, sector_id) VALUES (?, ?)", (data["industry"], sector_id))
        industry_id = db.cur.execute("SELECT industry_id FROM yahoo_gics_industry WHERE name = ?", (data["industry"],)).fetchone()[0]
    
    #profile data
    if data["country"] == "Bahamas":
        data["country"] = "The Bahamas"
    elif data["country"] == "Netherlands Antilles":
        print(f"{ticker}: Netherlands Antilles not in Database country table")
        return

    if data["country"] is None:
        country_id = None
    else:
        country_id = db.cur.execute("SELECT country_id FROM country WHERE name = ?", (data["country"],)).fetchone()[0]

    if data["city"] is None:
        city_id = None
    else:
        db.cur.execute("INSERT OR IGNORE INTO yahoo_city (name, country_id) VALUES (?, ?)", (data["city"], country_id))
        city_id = db.cur.execute("SELECT city_id FROM yahoo_city WHERE name = ? AND country_id = ?", (data["city"], country_id)).fetchone()[0]

    db.cur.execute(
        """
        UPDATE
            company
        SET
            gics_industry_id = ?,
            website = ?,
            country_id = ?,
            city_id = ?,
            address1 = ?,
            address2 = ?,
            address3 = ?,
            zip = ?,
            employees = ?
        WHERE
            security_id = ?
        """,
        (industry_id, data["website"], country_id, city_id, data["address1"], data["address2"], data["address3"], data["zip"], data["employees"], security_id)
    )

def update_yahoo_executives(reader: YahooReader, db: Database) -> None:
    profile = reader.profile()
    if "executives" not in profile:
        return

    security_id = db.cur.execute("SELECT security_id FROM security WHERE ticker = ?", (reader.ticker,)).fetchone()[0]
    ts_today = int(pd.to_datetime(pd.to_datetime("today").date()).timestamp())

    executives = {}
    for item in profile["executives"]:
        name = item["name"]
        position = item["position"]
        salary = item["salary"]
        age = item["age"]
        born = item["born"]

        db.cur.execute("REPLACE INTO yahoo_executive (name, age, born) VALUES (?, ?, ?)", (name, age, born))
        executive_id = db.cur.execute("SELECT executive_id FROM yahoo_executive WHERE name = ?", (name,)).fetchone()[0]

        db.cur.execute("INSERT OR IGNORE INTO yahoo_executive_position (name) VALUES (?)", (position,))
        position_id = db.cur.execute("SELECT position_id FROM yahoo_executive_position WHERE name = ?", (position,)).fetchone()[0]

        executives[(security_id, executive_id, position_id)] = salary

    # check if the executives in the databse are still executives. If not, discontinue them and if yes, update the salary
    for (security_id, executive_id, position_id, salary) in \
        db.cur.execute(
            "SELECT security_id, executive_id, position_id, salary FROM yahoo_company_executive_match WHERE security_id = ? AND executive_id = ? AND position_id = ?",
            (security_id, executive_id, position_id)
        ).fetchall():
        if (security_id, executive_id, position_id) not in executives.keys():
            if db.cur.execute(
                "SELECT discontinued FROM yahoo_company_executive_match WHERE security_id = ? AND security_id = ? AND position_id = ?",
                (security_id, executive_id, position_id)
            ).fetchone()[0] is None:
                db.cur.execute(
                    "UPDATE yahoo_company_executive_match SET discontinued = ? WHERE security_id = ? AND executive_id = ? AND position_id = ?", 
                    (ts_today, security_id, executive_id, position_id)
                )
            elif executives[(security_id, executive_id, position_id)] != salary:
                db.cur.execute(
                    "UPDATE yahoo_company_executive_match SET salary = ? WHERE security_id = ? AND executive_id = ? AND position_id = ?",
                    (executives[(security_id, executive_id, position_id)], security_id, executive_id, position_id)
                )

    # insert new executives or set discontinued to Null if they had a position in a company before
    entries = db.cur.execute("SELECT security_id, executive_id, position_id FROM yahoo_company_executive_match").fetchall()
    for (security_id, executive_id, position_id), salary in executives.items():
        if (security_id, executive_id, position_id) not in entries:
            db.cur.execute(
                "INSERT INTO yahoo_company_executive_match (security_id, executive_id, position_id, salary, added) VALUES (?, ?, ?, ?, ?)",
                (security_id, executive_id, position_id, salary, ts_today)
            )
        else:
            db.cur.execute(
                "UPDATE yahoo_company_executive_match SET discontinued = NULL WHERE security_id = ? AND executive_id = ? AND position_id = ?",
                (security_id, executive_id, position_id)
            )

def update_yahoo_fundamentals(reader: YahooReader, db: Database) -> None:
    security_id = db.cur.execute("SELECT security_id FROM security WHERE ticker = ?", (reader.ticker,)).fetchone()[0]

    try:
        statements = reader.financial_statement()
    except:
        return
    
    if all(list(statements[type_].keys()) in (["TTM"], []) for type_ in statements.keys()):
        return

    for statement in statements.keys():
        for date_iso in statements[statement].keys():
            if date_iso == "TTM":
                continue
            date = pd.to_datetime(date_iso)
            year = date.year
            ts_statement = int(date.timestamp())
            for variable in statements[statement][date_iso]:
                statement_id = db.cur.execute("SELECT statement_id FROM financial_statement WHERE internal_name = ?", (statement.upper(),)).fetchone()[0]
                db.cur.execute("INSERT OR IGNORE INTO yahoo_fundamental_variable (name, statement_id) VALUES (?, ?)", (variable, statement_id))
                variable_id = db.cur.execute("SELECT variable_id FROM yahoo_fundamental_variable WHERE name = ? AND statement_id = ?", (variable, statement_id)).fetchone()[0]
                db.cur.execute(
                    "REPLACE INTO yahoo_fundamental_data VALUES (?, ?, ?, ?, ?, ?)",
                    (security_id, variable_id, 0, year, ts_statement, statements[statement][date_iso][variable])
                )
    fiscal_year_end_quarter = date.quarter
    db.cur.execute("UPDATE company SET fiscal_year_end = ? WHERE security_id = ?", (date.month ,security_id))

    try:
        statements = reader.financial_statement(quarterly=True)
    except:
        return

    for statement in statements.keys():
        for date_iso in statements[statement].keys():
            date = pd.to_datetime(date_iso)
            year = date.year
            ts_statement = int(date.timestamp())
            quarter = (date.quarter+3-fiscal_year_end_quarter)%4+1
            year = year + 1 if (fiscal_year_end_quarter < 4 and date.quarter > fiscal_year_end_quarter) else year
            for variable in statements[statement][date_iso]:
                statement_id = db.cur.execute("SELECT statement_id FROM financial_statement WHERE internal_name = ?", (statement.upper(),)).fetchone()[0]
                db.cur.execute("INSERT OR IGNORE INTO yahoo_fundamental_variable (name, statement_id) VALUES (?, ?)", (variable, statement_id))
                variable_id = db.cur.execute("SELECT variable_id FROM yahoo_fundamental_variable WHERE name = ? AND statement_id = ?", (variable, statement_id)).fetchone()[0]
                db.cur.execute(
                    "REPLACE INTO yahoo_fundamental_data VALUES (?, ?, ?, ?, ?, ?)",
                    (security_id, variable_id, quarter, year, ts_statement, statements[statement][date_iso][variable])
                )

def update_yahoo_analyst_recommendations(reader: YahooReader, db: Database) -> None:
    try:
        recommendations = reader.analyst_recommendations()
    except:
        return

    security_id = db.cur.execute("SELECT security_id FROM security WHERE ticker = ?", (reader.ticker,)).fetchone()[0]

    for dct in recommendations:
        ts_rated = int(pd.to_datetime(dct["date"]).timestamp())
        name = dct["company"]
        old = dct["old"]
        new = dct["new"]
        change = dct["change"]
        
        db.cur.execute("INSERT OR IGNORE INTO yahoo_analyst_company (name) VALUES (?)", (name,))
        analyst_id = db.cur.execute("SELECT company_id FROM yahoo_analyst_company WHERE name = ?", (name,)).fetchone()[0]
        
        if old is None:
            old_id = None
        else:
            db.cur.execute("INSERT OR IGNORE INTO yahoo_rating (name) VALUES (?)", (old,))
            old_id = db.cur.execute("SELECT rating_id FROM yahoo_rating WHERE name = ?", (old,)).fetchone()[0]

        if new is None:
            new_id = None
        else:
            db.cur.execute("INSERT OR IGNORE INTO yahoo_rating (name) VALUES (?)", (new,))
            new_id = db.cur.execute("SELECT rating_id FROM yahoo_rating WHERE name = ?", (new,)).fetchone()[0]

        if change is None:
            change_id = None
        else:
            db.cur.execute("INSERT OR IGNORE INTO yahoo_rating (name) VALUES (?)", (change,))
            change_id = db.cur.execute("SELECT rating_id FROM yahoo_rating WHERE name = ?", (change,)).fetchone()[0]

        db.cur.execute(
            "REPLACE INTO yahoo_analyst_recommendation VALUES (?, ?, ?, ?, ?, ?)",
            (analyst_id, security_id, ts_rated, old_id, new_id, change_id)
        )

def update_yahoo_recommendation_trend(reader: YahooReader, db: Database) -> None:
    try:
        trend = reader.recommendation_trend()
    except:
        return

    security_id = db.cur.execute("SELECT security_id FROM security WHERE ticker = ?", (reader.ticker,)).fetchone()[0]

    year = pd.to_datetime("today").year
    month = pd.to_datetime("today").month

    for calendar in trend.keys():
        date_month = pd.to_datetime(f"{year}-{month}-01")
        if calendar == "today":
            pass
        elif calendar == "-1month":
            date_month = date_month - relativedelta(months=1)
        elif calendar == "-2months":
            date_month = date_month - relativedelta(months=2)
        elif calendar == "-3months":
            date_month = date_month - relativedelta(months=3)

        ts_month = int(date_month.timestamp())

        db.cur.execute(
            "REPLACE INTO yahoo_recommendation_trend VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (security_id,
            ts_month,
            trend[calendar]["count"],
            trend[calendar]["average"],
            trend[calendar]["strong_buy"],
            trend[calendar]["buy"],
            trend[calendar]["hold"],
            trend[calendar]["sell"],
            trend[calendar]["strong_sell"])
        )

def update_yahoo_prices(reader: YahooReader, db: Database) -> None:
    ts_today = int(pd.to_datetime(pd.to_datetime("today").date()).timestamp())
    security_id = db.cur.execute("SELECT security_id FROM security WHERE ticker = ?", (reader.ticker,)).fetchone()[0]

    try:
        data = reader.historical_data(frequency="1d", timestamps=True)
    except TickerError:
        db.cur.execute("UPDATE security SET prices_updated = ? WHERE security_id = ?", (ts_today, security_id))
        return

    df = data["data"]
    offset = data["information"]["utc_offset"]

    currency = data["information"]["currency"]
    currency_id = db.cur.execute("SELECT currency_id FROM currency WHERE abbr = ?", (currency,)).fetchone()[0]

    df["security id"] = security_id
    data = df.reindex(columns = ["security id", "ts", "open", "high", "low", "close", "adj_close", "volume", "dividends", "splits", "simple_returns", "log_returns"]).values

    db.cur.executemany("REPLACE INTO yahoo_security_price VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    db.cur.execute("UPDATE security SET prices_updated = ?, currency_id = ?, utc_offset = ? WHERE security_id = ?", (ts_today, currency_id, offset, security_id))

if __name__ == "__main__":
    with Database() as db:
        tickers = db.cur.execute(
            """
            SELECT
                ticker
            FROM
                security
            WHERE
                discontinued IS NULL
            ORDER BY
                ticker
            """
        ).fetchall()

        tickers = [item[0] for item in tickers]
        length = len(tickers)
        trail = len(str(length))

        start = time.time()
        for index, ticker in enumerate(tickers):
            print(f"{index+1: >{trail}} of {length}: {ticker}")

            # sleep every minute for a minute because of rate limits
            if time.time() - start >= 60:
                db.con.commit()
                time.sleep(60)
                start = time.time()

            try:
                reader = YahooReader(ticker)
            except TickerError:
                print(f"\t{ticker} failed")
                continue
            update_yahoo_data(reader, db)
