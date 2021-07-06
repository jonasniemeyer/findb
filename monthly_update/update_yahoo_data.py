from finance_data import YahooReader
from finance_database import Database
import datetime as dt
from dateutil.relativedelta import relativedelta

ts_today = int((dt.date.today() - dt.date(1970,1,1)).total_seconds())

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

tickers = cur.execute("SELECT ticker FROM securities WHERE discontinued IS NULL").fetchall()
tickers = [item[0] for item in tickers]

types = []
length = len(tickers)
for index, ticker in enumerate(tickers):
    if index % 100 == 0:
        con.commit()
    print(ticker, index, "of", length)
    try:
        reader = YahooReader(ticker)
        profile = reader.profile()
    except:
        print("\t", ticker, "failed")
        continue
    
    security_id = cur.execute("SELECT id FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    cik = cur.execute("SELECT cik FROM securities WHERE ticker = ?", (ticker,)).fetchone()[0]
    
    security_name = reader.name
    security_type = reader.security_type
    if cur.execute("SELECT id FROM security_types WHERE name = ?", (security_type,)).fetchone() is None:
        cur.execute("INSERT INTO security_types (name) VALUES (?)", (security_type, ))
    type_id = cur.execute("SELECT id FROM security_types WHERE name = ?", (security_type,)).fetchone()[0]

    description = profile["description"]

    cur.execute("UPDATE securities SET yahoo_name = ?, type_id = ?, description = ? WHERE ticker = ?", (security_name, type_id, description, ticker))

    if security_type == "EQUITY" and cur.execute(f"SELECT * FROM sec_filings WHERE cik = ? AND form_type_id IN {form_ids}", (cik, )).fetchone() is None:
        
        cur.execute("INSERT OR IGNORE INTO companies (security_id) VALUES (?)", (security_id,))
        
        data = {}
        for var in (
            "website",
            "country",
            "city",
            "address1",
            "address2",
            "zip",
            "fullTimeEmployees",
            "industry",
            "sector"
        ):
            try:
                data[var] = profile[var]
            except:
                data[var] = None

        #industry
        if data["industry"] is not None:
            if cur.execute("SELECT id FROM gics_sectors WHERE name = ?", (data["sector"],)).fetchone() is None:
                cur.execute("INSERT INTO gics_sectors (name) VALUES (?)", (data["sector"],))
            sector_id = cur.execute("SELECT id FROM gics_sectors WHERE name = ?", (data["sector"],)).fetchone()[0]
            if cur.execute("SELECT id FROM gics_industries WHERE name = ?", (data["industry"],)).fetchone() is None:
                cur.execute("INSERT INTO gics_industries (name, sector_id) VALUES (?, ?)", (data["industry"], sector_id))
            industry_id = cur.execute("SELECT id FROM gics_industries WHERE name = ?", (data["industry"],)).fetchone()[0]
        else:
            industry_id = None
        
        if data["country"] == "Bahamas":
            data["country"] = "The Bahamas"
        
        if data["country"] != "Netherlands Antilles":
            country_id = cur.execute("SELECT name FROM countries WHERE name = ?", (data["country"], )).fetchone()[0]

        cur.execute(
            """
            UPDATE companies SET gics_industry_id = ?, website = ?, country_id = ?, city = ?,
            address1 = ?, address2 = ?, zip = ?, employees = ?
            WHERE security_id = ?
            """,
            (industry_id, data["website"], country_id, data["city"], data["address1"], data["address2"], data["zip"], data["fullTimeEmployees"], security_id)
        )

        # executives
        executives = {}
        for item in profile["executives"]:
            name = item["name"]
            position = item["position"]
            salary = item["salary"]
            age = item["age"]
            born = item["born"]

            cur.execute("UPDATE executives SET age = ? WHERE name = ? AND born = ?", (age, name, born))
            if cur.execute("SELECT id FROM executives WHERE name = ?", (name,)).fetchone() is None:
                cur.execute("INSERT INTO executives (name, age, born) VALUES (?, ?, ?)", (name, age, born))
            executive_id = cur.execute("SELECT id FROM executives WHERE name = ?", (name,)).fetchone()[0]

            if cur.execute("SELECT id FROM executive_positions WHERE name = ?", (position,)).fetchone() is None:
                cur.execute("INSERT OR IGNORE INTO executive_positions (name) VALUES (?)", (position,))
            position_id = cur.execute("SELECT id FROM executive_positions WHERE name = ?", (position,)).fetchone()[0]

            executives[(security_id, executive_id, position_id)] = salary

        for (security_id, executive_id, position_id, salary) in \
            cur.execute(
                "SELECT security_id, executive_id, position_id, salary FROM company_executive_match WHERE security_id = ? AND executive_id = ? AND position_id = ?",
                (security_id, executive_id, position_id)
            ).fetchall():
            if (security_id, executive_id, position_id) not in executives.keys():
                if cur.execute(
                    "SELECT discontinued FROM company_executive_match WHERE security_id = ? AND security_id = ? AND position_id = ?",
                    (security_id, executive_id, position_id)
                ).fetchone()[0] is None:
                    cur.execute(
                        "UPDATE company_executive_match SET discontinued = ? WHERE security_id = ? AND executive_id = ? AND position_id = ?", 
                        (ts_today, security_id, executive_id, position_id)
                    )
                elif executives[(security_id, executive_id, position_id)] != salary:
                    cur.execute(
                        "UPDATE company_executive_match SET salary = ? WHERE security_id = ? AND executive_id = ? AND position_id = ?",
                        (executives[(security_id, executive_id, position_id)], security_id, executive_id, position_id)
                    )
            
        con.commit()

        entries = cur.execute("SELECT security_id, executive_id, position_id FROM company_executive_match").fetchall()

        for (security_id, executive_id, position_id), salary in executives.items():
            if (security_id, executive_id, position_id) not in entries:
                cur.execute(
                    "INSERT INTO company_executive_match (security_id, executive_id, position_id, salary, added) VALUES (?, ?, ?, ?, ?)",
                    (security_id, executive_id, position_id, salary, ts_today)
                )
            else:
                cur.execute(
                    "UPDATE company_executive_match SET discontinued = NULL WHERE security_id = ? AND executive_id = ? AND position_id = ?",
                    (security_id, executive_id, position_id)
                )
        
        con.commit()

        # fundamental data

        try:
            statements = reader.financial_statement()
        except:
            pass
        else:
            for statement in statements.keys():
                statement_name = statement.replace("_", " ")
                for date_iso in statements[statement].keys():
                    date = dt.date.fromisoformat(date_iso)
                    year = date.year
                    ts_statement = int((date - dt.date(1970, 1, 1)).total_seconds())
                    for variable in statements[statement][date_iso]:
                        statement_id = cur.execute("SELECT id FROM financial_statement_types WHERE name = ?", (statement_name, )).fetchone()[0]
                        if cur.execute("SELECT id FROM fundamental_variables_yahoo WHERE name = ? AND statement_id = ?", (variable, statement_id)).fetchone() is None:
                            cur.execute("INSERT INTO fundamental_variables_yahoo (name, statement_id) VALUES (?, ?)", (variable, statement_id))
                        variable_id = cur.execute("SELECT id FROM fundamental_variables_yahoo WHERE name = ? AND statement_id = ?", (variable, statement_id)).fetchone()[0]
                        cur.execute(
                            "INSERT OR IGNORE INTO fundamental_data_yahoo VALUES (?, ?, ?, ?, ?, ?)",
                            (security_id, variable_id, 0, year, ts_statement, statements[statement][date_iso][variable])
                        )
            fiscal_end_quarter = (date.month - 1 // 3) + 1
            cur.execute("UPDATE companies SET fiscal_year_end = ? WHERE security_id = ?",(date.month ,security_id))
            try:
                statements = reader.financial_statement(quarterly=True)
            except:
                pass
            else:
                for statement in statements.keys():
                    statement_name = statement.replace("_", " ")
                    for date_iso in statements[statement].keys():
                        date = dt.date.fromisoformat(date_iso)
                        year = date.year
                        quarter = (date.month - 1 // 3) + 1
                        quarter = (quarter + 4 - fiscal_end_quarter - 1) // 4 + 1
                        ts_statement = int((date - dt.date(1970, 1, 1)).total_seconds())
                        for variable in statements[statement][date_iso]:
                            statement_id = cur.execute("SELECT id FROM financial_statement_types WHERE name = ?", (statement_name, )).fetchone()[0]
                            if cur.execute("SELECT id FROM fundamental_variables_yahoo WHERE name = ? AND statement_id = ?", (variable, statement_id)).fetchone() is None:
                                cur.execute("INSERT INTO fundamental_variables_yahoo (name, statement_id) VALUES (?, ?)", (variable, statement_id))
                            variable_id = cur.execute("SELECT id FROM fundamental_variables_yahoo WHERE name = ? AND statement_id = ?", (variable, statement_id)).fetchone()[0]
                            cur.execute(
                                "INSERT OR IGNORE INTO fundamental_data_yahoo VALUES (?, ?, ?, ?, ?, ?)",
                                (security_id, variable_id, quarter, year, ts_statement, statements[statement][date_iso][variable])
                            )

        # analyst recommendations
        try:
            recommendations = reader.analyst_recommendations()
        except:
            pass
        else:
            for dct in recommendations:
                ts_rated = int((dt.date.fromisoformat(dct["date"]) - dt.date(1970, 1, 1)).total_seconds())
                name = dct["firm"]
                old = dct["old"]
                new = dct["new"]
                change = dct["change"]
                
                if  cur.execute("SELECT id FROM analysts WHERE name = ?", (name, )).fetchone() is None:
                    cur.execute("INSERT INTO analysts (name) VALUES (?)", (name, ))
                analyst_id = cur.execute("SELECT id FROM analysts WHERE name = ?", (name, )).fetchone()[0]

                if cur.execute("SELECT id FROM ratings WHERE name = ?", (old, )).fetchone() is None:
                    cur.execute("INSERT INTO ratings (name) VALUES (?)", (old, ))
                old_id = cur.execute("SELECT id FROM ratings WHERE name = ?", (old, )).fetchone()[0]

                if cur.execute("SELECT id FROM ratings WHERE name = ?", (new, )).fetchone() is None:
                    cur.execute("INSERT INTO ratings (name) VALUES (?)", (new, ))
                new_id = cur.execute("SELECT id FROM ratings WHERE name = ?", (new, )).fetchone()[0]

                if cur.execute("SELECT id FROM ratings WHERE name = ?", (change, )).fetchone() is None:
                    cur.execute("INSERT INTO ratings (name) VALUES (?)", (change, ))
                change_id = cur.execute("SELECT id FROM ratings WHERE name = ?", (new, )).fetchone()[0]

                cur.execute(
                    "INSERT OR IGNORE INTO analyst_recommendations VALUES (?, ?, ?, ?, ?, ?)",
                    (analyst_id, security_id, ts_rated, old_id, new_id, change_id)
                )

        # recommendation trend
        try:
            trend = reader.recommendation_trend()
        except:
            pass
        else:
            year = dt.date.today().year
            month = dt.date.today().month
            for calendar in trend.keys():
                date_month = dt.date(year, month, 1)
                if calendar == "today":
                    pass
                elif calendar == "-1month":
                    date_month = date_month - relativedelta(months=1)
                elif calendar == "-2months":
                    date_month = date_month - relativedelta(months=2)
                elif calendar == "-3months":
                    date_month = date_month - relativedelta(months=3)
                
                ts_month = int((date_month - dt.date(1970, 1, 1)).total_seconds())

                cur.execute(
                    "INSERT OR IGNORE INTO recommendation_trend VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (security_id,
                    ts_today,
                    ts_month,
                    trend[calendar]["recommendations"],
                    trend[calendar]["average"],
                    trend[calendar]["strong_buy"],
                    trend[calendar]["buy"],
                    trend[calendar]["hold"],
                    trend[calendar]["sell"],
                    trend[calendar]["strong_sell"])
                )
    
    cur.execute("UPDATE securities SET profile_updated = ?", (ts_today,))

con.commit()
con.close()


