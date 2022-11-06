from finance_data import sec_companies, sec_mutualfunds
from finance_database import Database
import pandas as pd

def update_companies(db_connection):
    con = db_connection
    cur = con.cursor()

    new_companies = sec_companies()
    new_companies = {(str(company["cik"]), company["ticker"]): company["name"] for company in new_companies}
    ts_today = int(pd.to_datetime("today").timestamp())

    database_companies = cur.execute("SELECT cik, ticker, sec_name FROM securities WHERE is_sec_company = 1").fetchall()    
    for (cik, ticker, name) in database_companies:
        # if the company in the database IS NOT in the new companies dict, it should be set to discontinued if not already done
        if (
            (cik, ticker) not in new_companies.keys()
            and cur.execute("SELECT discontinued FROM securities WHERE cik = ? AND ticker = ?", (cik, ticker)).fetchone()[0] is None
        ):
            cur.execute("UPDATE securities SET discontinued = ? WHERE cik = ? AND ticker = ?", (ts_today, cik, ticker))
            print(f"Discontinued Company: {cik:>10} {ticker:>6} {name}")
        
        # if the company in the database IS in the new companies dict but has a different name, the name should be updated
        elif new_companies[(cik, ticker)] != name:
            cur.execute(
                "UPDATE securities SET sec_name = ?, old_name = ? WHERE cik = ? AND ticker = ?", 
                (new_companies[(cik, ticker)], name, cik, ticker)
            )
            print(f"Company Name Updated: {cik:>10} {ticker:>6} {name}")
            print(f"\tNew Name: {new_companies[(cik, ticker)]}")
            print(f"\tOld Name: {name}")
        
        con.commit()
    
    # fetch again without names
    database_companies = cur.execute("SELECT cik, ticker FROM securities WHERE is_sec_company = 1").fetchall()
    for (cik, ticker), name in new_companies.items():
        # if the new company is not in the database, insert it
        if (cik, ticker) not in database_companies:
            cur.execute("INSERT INTO securities (cik, ticker, sec_name, added, is_sec_company) VALUES (?, ?, ?, ?, ?)", (cik, ticker, name, ts_today, True))
            print(f"New Company: {cik:>10} {ticker:>6} {name}")
        # if the new company is already in the database, set discontinued to NULL in case if was discontinued in the past
        else:
            cur.execute("UPDATE securities SET discontinued = NULL WHERE cik = ? AND ticker = ?", (cik, ticker))

def update_mutualfunds(db_connection):
    con = db_connection
    cur = con.cursor()

    new_classes = sec_mutualfunds()
    ts_today = int(pd.to_datetime("today").timestamp())

    new_entity_ciks = set([class_["entity_cik"] for class_ in new_classes])
    database_entities = cur.execute("SELECT cik FROM sec_mutualfund_entities").fetchall()
    database_entities = [item[0] for item in database_entities]

    new_series_ciks = set([class_["series_cik"] for class_ in new_classes])
    database_series = cur.execute("SELECT cik FROM sec_mutualfund_series").fetchall()
    database_series = [item[0] for item in database_series]

    new_class_ciks = set([class_["class_cik"] for class_ in new_classes])
    database_classes = cur.execute("SELECT cik, ticker FROM securities WHERE is_sec_mutualfund = 1").fetchall()

    # set entities to discontinued that are IN the database but are NOT IN the new classes dict if not already done
    for cik in database_entities:
        if (
            cik not in new_entity_ciks
            and cur.execute("SELECT discontinued FROM sec_mutualfund_entities WHERE cik = ?", (cik,)).fetchone()[0] is None
        ):
            cur.execute("UPDATE sec_mutualfund_entities SET discontinued = ? WHERE cik = ?", (ts_today, cik))
            print(f"Discontinued Mutual Fund Entity: {cik:>10}")
    con.commit()

    # set series to discontinued that are IN the database but are NOT IN the new classes dict if not already done
    for cik in database_series:
        if (
            cik not in new_series_ciks
            and cur.execute("SELECT discontinued FROM sec_mutualfund_series WHERE cik = ?", (cik,)).fetchone()[0] is None
        ):
            cur.execute("UPDATE sec_mutualfund_series SET discontinued = ? WHERE cik = ?", (ts_today, cik))
            print(f"Discontinued Mutual Fund Series: {cik:>10}")
    con.commit()

    # set classes to discontinued that are IN the database but are NOT IN the new classes dict if not already done
    for cik, ticker in database_classes:
        if (
            cik not in new_class_ciks
            and cur.execute("SELECT discontinued FROM securities WHERE cik = ? AND ticker = ?", (cik, ticker)).fetchone()[0] is None
        ):
            cur.execute("UPDATE securities SET discontinued = ? WHERE cik = ? AND ticker = ?", (ts_today, cik, ticker))
            print(f"Discontinued Mutual Fund Class: {cik:>10} {ticker:>6}")
    con.commit()

    # insert new entities
    for cik in new_entity_ciks:
        if cik not in database_entities:
            cur.execute("INSERT INTO sec_mutualfund_entities (cik, added) VALUES (?, ?)", (cik, ts_today))
            print(f"New Mutual Fund Entity: {cik}")
        else:
            cur.execute("UPDATE sec_mutualfund_entities SET discontinued = NULL WHERE cik = ?", (cik,))
    con.commit()

    # insert new series
    new_series = set([(class_["series_cik"], class_["entity_cik"]) for class_ in new_classes])
    for series_cik, entity_cik in new_series:
        if series_cik not in database_series:
            entity_id = cur.execute("SELECT id FROM sec_mutualfund_entities WHERE cik = ?", (entity_cik,)).fetchone()[0]
            cur.execute("INSERT INTO sec_mutualfund_series (cik, entity_id, added) VALUES (?, ?, ?)", (series_cik, entity_id, ts_today))
            print(f"New Mutual Fund Series: {series_cik}")
        else:
            cur.execute("UPDATE sec_mutualfund_series SET discontinued = NULL WHERE cik = ?", (series_cik,))
    con.commit()

    # insert new classes
    for class_ in new_classes:
        ticker = class_["ticker"]
        class_cik = class_["class_cik"]
        series_cik = class_["series_cik"]
        entity_cik = class_["entity_cik"]

        if (class_cik, ticker) not in database_classes:
            cur.execute("INSERT INTO securities (cik, ticker, added, is_sec_mutualfund) VALUES (?, ?, ?, ?)", (class_cik, ticker, ts_today, True))
            class_id = cur.execute("SELECT id FROM securities WHERE cik = ? AND ticker = ?", (class_cik, ticker)).fetchone()[0]
            series_id = cur.execute("SELECT id FROM sec_mutualfund_series WHERE cik = ?", (series_cik,)).fetchone()[0]
            cur.execute("INSERT INTO sec_mutualfund_classes (security_id, series_id) VALUES (?, ?)", (class_id, series_id))
            print(f"New Mutual Fund Class: {class_cik:>10} {ticker:>6}")
        else:
            cur.execute("UPDATE securities SET discontinued = NULL WHERE cik = ? AND ticker = ?", (class_cik, ticker))
    con.commit()

if __name__ == "__main__":
    db = Database()
    con = db.connection
    print("Updating SEC Companies")
    update_companies(con)
    print("Updating SEC Mutual Funds")
    update_mutualfunds(con)
    con.close()