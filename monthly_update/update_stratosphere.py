from findata import StratosphereReader
from findb import Database
from findb.utils import STRATOSPHERE_CONVERSION

def update_stratosphere_fundamental_data(data: dict, security_id: int, db: Database) -> None:
    if data is None:
        return
    for statement in data:
        if data[statement] is None:
            continue
        for freq, quarterly in {"annual": 0, "quarterly": 1}.items():
            for var in data[statement][freq]:
                var_id = db.cur.execute("SELECT variable_id FROM fundamental_variable WHERE internal_name = ?", (STRATOSPHERE_CONVERSION[statement.upper()][var].name,)).fetchone()[0]
                for ts, value in data[statement][freq][var].items():
                    value = float(value) if value is not None else None
                    db.cur.execute(
                        """
                        INSERT OR IGNORE INTO stratosphere_fundamental_data
                        (security_id, variable_id, ts, quarterly, value)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (security_id, var_id, ts, quarterly, value)
                    )

def update_stratosphere_segment_data(data: dict, security_id: int, db: Database) -> None:
    if data is None:
        return
    for freq, quarterly in {"annual": 0, "quarterly": 1}.items():
        for var in data[freq]:
            db.cur.execute("INSERT OR IGNORE INTO stratosphere_segment_variable (name) VALUES (?)", (var,))
            var_id = db.cur.execute("SELECT variable_id FROM stratosphere_segment_variable WHERE name = ?", (var,)).fetchone()[0]
            for ts, value in data[freq][var].items():
                db.cur.execute(
                    """
                    INSERT OR IGNORE INTO stratosphere_segment_data
                    (security_id, variable_id, ts, quarterly, value)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (security_id, var_id, ts, quarterly, value)
                )

def update_stratosphere_kpi_data(data: dict, security_id: int, db: Database) -> None:
    if data is None:
        return
    for freq, quarterly in {"annual": 0, "quarterly": 1}.items():
        for var in data[freq]:
            db.cur.execute("INSERT OR IGNORE INTO stratosphere_kpi_variable (name) VALUES (?)", (var,))
            var_id = db.cur.execute("SELECT variable_id FROM stratosphere_kpi_variable WHERE name = ?", (var,)).fetchone()[0]
            for ts, value in data[freq][var].items():
                db.cur.execute(
                    """
                    INSERT OR IGNORE INTO stratosphere_kpi_data
                    (security_id, variable_id, ts, quarterly, value)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (security_id, var_id, ts, quarterly, value)
                )

def update_stratosphere_analyst_estimates(data: dict, security_id: int, db: Database) -> None:
    if data is None:
        return
    return

def update_stratosphere_price_targets(data: dict, security_id: int, db: Database) -> None:
    if data is None:
        return
    for item in data:
        db.cur.execute("INSERT OR IGNORE INTO stratosphere_analyst_company (name) VALUES (?)", (item["analyst_company"],))
        company_id = db.cur.execute("SELECT company_id FROM stratosphere_analyst_company WHERE name = ?", (item["analyst_company"],)).fetchone()[0]

        db.cur.execute("INSERT OR IGNORE INTO stratosphere_analyst (name, company_id) VALUES (?, ?)", (item["analyst_name"], company_id))
        if item["analyst_name"] is None:
            analyst_id = db.cur.execute("SELECT analyst_id FROM stratosphere_analyst WHERE name IS NULL AND company_id = ?", (company_id,)).fetchone()[0]
        else:
            analyst_id = db.cur.execute("SELECT analyst_id FROM stratosphere_analyst WHERE name = ? AND company_id = ?", (item["analyst_name"], company_id)).fetchone()[0]

        db.cur.execute("INSERT OR IGNORE INTO news_source (name) VALUES (?)", (item["news_source"],))
        source_id = db.cur.execute("SELECT source_id FROM news_source WHERE name = ?", (item["news_source"],)).fetchone()[0]

        db.cur.execute(
            """
            INSERT OR IGNORE INTO stratosphere_analyst_price_target
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (security_id, analyst_id, item["price_target"], item["price_when_rated"], item["datetime"], item["news_title"], item["news_url"], source_id)
        )

if __name__ == "__main__":
    import pandas as pd
    ts_today = pd.to_datetime(pd.to_datetime("today").date()).timestamp()

    with Database() as db:
        tickers = [item["ticker"] for item in db.companies()]
        length = len(tickers)
        trail = len(str(length))

        for index, ticker in enumerate(tickers):
            security_id = db.cur.execute("SELECT security_id FROM security WHERE ticker = ?", (ticker,)).fetchone()[0]
            #if db.cur.execute("SELECT stratosphere_data_updated FROM company WHERE security_id = ?", (security_id,)).fetchone()[0] is not None:
            #    continue
            print(f"{index+1: >{trail}} of {length}: {ticker}")
            db.cur.execute("INSERT OR IGNORE INTO security (ticker, added) VALUES (?, ?)", (ticker, ts_today))
            reader = StratosphereReader(ticker)
            update_stratosphere_fundamental_data(reader.financial_statement(timestamps=True), security_id, db)
            update_stratosphere_segment_data(reader.segment_information(timestamps=True), security_id, db)
            update_stratosphere_kpi_data(reader.kpi_information(timestamps=True), security_id, db)
            update_stratosphere_analyst_estimates(reader.analyst_estimates(timestamps=True), security_id, db)
            update_stratosphere_price_targets(reader.price_targets(timestamps=True), security_id, db)
            if index % 100 == 0:
                db.con.commit()
            db.cur.execute("UPDATE company SET stratosphere_data_updated = ? WHERE security_id = ?", (ts_today, security_id))