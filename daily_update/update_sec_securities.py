import pandas as pd
from findata import sec_companies, sec_mutualfunds
from findb import Database

def update_companies(db: Database) -> None:
    new_companies = sec_companies()
    new_companies = {str(company["ticker"]): {"name": company["name"], "cik": company["cik"]} for company in new_companies}

    ts_today = int(pd.to_datetime("today").timestamp())

    # insert new entities
    for dct in new_companies.values():
        # if the entity is not in the database, insert it
        if db.cur.execute("SELECT cik FROM entity WHERE cik = ?", (dct["cik"],)).fetchone() is None:
            db.cur.execute("INSERT INTO entity (cik, sec_name, added) VALUES (?, ?, ?)", (dct["cik"], dct["name"], ts_today))
            print(f"New entity added: {dct['cik']}")
        # else if the new name is not None and different than in the database, update it
        elif dct["name"] is not None:
            old_name = db.cur.execute("SELECT sec_name FROM entity WHERE cik = ?", (dct["cik"],)).fetchone()[0]
            if dct["name"] != old_name:
                db.cur.execute("UPDATE entity SET sec_name = ?, old_name = ? WHERE cik = ?", (dct["name"], old_name, dct["cik"]))
                print(f"Entity Name Updated: {dct['cik']:>8}, New Name: {dct['name']}, Old Name: {old_name}")

    # insert new securities
    for ticker, dct in new_companies.items():
        # if the company is not in the database, insert it
        if db.cur.execute("SELECT ticker FROM security WHERE ticker = ?", (ticker,)).fetchone() is None:
            entity_id = db.cur.execute("SELECT entity_id FROM entity WHERE cik = ?", (dct["cik"],)).fetchone()[0]
            db.cur.execute("INSERT INTO security (entity_id, ticker, added) VALUES (?, ?, ?)", (entity_id, ticker, ts_today))
            print(f"New Company: {ticker:>8} {dct['cik']}")

def update_mutualfunds(db: Database) -> None:
    new_classes = sec_mutualfunds()
    ts_today = int(pd.to_datetime("today").timestamp())

    new_entity_ciks = set([class_["entity_cik"] for class_ in new_classes])

    # insert new entities
    for cik in new_entity_ciks:
        if db.cur.execute("SELECT cik FROM entity WHERE cik = ?", (cik,)).fetchone() is None:
            db.cur.execute("INSERT INTO entity (cik, added) VALUES (?, ?)", (cik, ts_today))
            print(f"New Mutual Fund Entity: {cik}")

    # insert new series
    new_series = set([(class_["series_cik"], class_["entity_cik"]) for class_ in new_classes])
    for series_cik, entity_cik in new_series:
        if db.cur.execute("SELECT cik FROM sec_mutualfund_series WHERE cik = ?", (series_cik,)).fetchone() is None:
            entity_id = db.cur.execute("SELECT entity_id FROM entity WHERE cik = ?", (entity_cik,)).fetchone()[0]
            db.cur.execute("INSERT INTO sec_mutualfund_series (cik, entity_id, added) VALUES (?, ?, ?)", (series_cik, entity_id, ts_today))
            print(f"New Mutual Fund Series: {series_cik}")

    # insert new classes
    for class_ in new_classes:
        ticker = class_["ticker"]
        if ticker is None:
            continue
        class_cik = class_["class_cik"]
        series_cik = class_["series_cik"]
        entity_cik = class_["entity_cik"]

        if db.cur.execute("SELECT ticker FROM security WHERE ticker = ?", (ticker,)).fetchone() is None:
            entity_id = db.cur.execute("SELECT entity_id FROM entity WHERE cik = ?",(entity_cik,)).fetchone()[0]
            db.cur.execute("INSERT INTO security (entity_id, ticker, added) VALUES (?, ?, ?)", (entity_id, ticker, ts_today))
            security_id = db.cur.execute("SELECT security_id FROM security WHERE ticker = ?",(ticker,)).fetchone()[0]
            series_id = db.cur.execute("SELECT series_id FROM sec_mutualfund_series WHERE cik = ?", (series_cik,)).fetchone()[0]
            db.cur.execute("INSERT INTO sec_mutualfund_class (security_id, series_id, cik) VALUES (?, ?, ?)", (security_id, series_id, class_cik))
            print(f"New Mutual Fund Class: {class_cik:>10} {ticker:>8}")

if __name__ == "__main__":
    with Database() as db:
        print("Updating SEC Companies")
        update_companies(db)

        print("Updating SEC Mutual Funds")
        update_mutualfunds(db)