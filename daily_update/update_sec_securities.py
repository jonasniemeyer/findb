import requests
import datetime as dt
from finance_database import Database

def security_list() -> dict:
    dct = requests.get("https://www.sec.gov/files/company_tickers.json").json().values()
    securities = {(item["cik_str"], item["ticker"]): item["title"] for item in dct}
    return securities

def update_securities(securities, db_con) -> None:
    cur = db_con.cursor()

    date = dt.date.today() - dt.timedelta(days=1)
    timestamp = int((date - dt.date(1970,1,1)).total_seconds())

    for (cik, ticker, name) in cur.execute("SELECT cik, ticker, sec_name FROM securities").fetchall():
        if (cik, ticker) not in securities.keys():
            if cur.execute("SELECT discontinued FROM securities WHERE CIK = ? AND ticker = ?", (cik, ticker)).fetchone()[0] is None:
                cur.execute("UPDATE securities SET discontinued = ? WHERE cik = ? AND ticker = ?", (timestamp, cik, ticker))
                print("security discontinued", cik, ticker, name)
        elif securities[(cik, ticker)] != name:
            cur.execute(
                "UPDATE securities SET sec_name = ?, old_name = ? WHERE cik = ? AND ticker = ? AND discontinued IS Null", 
                (securities[(cik, ticker)], name, cik, ticker)
            )
            print("name updated", cik, ticker, "old name:", name, "new name:", securities[(cik, ticker)])

    con.commit()

    database_entries = cur.execute("SELECT cik, ticker FROM securities").fetchall()
    for (cik, ticker), name in securities.items():
        if (cik, ticker) not in database_entries:
            cur.execute("INSERT INTO securities (cik, ticker, sec_name, added) VALUES (?, ?, ?, ?)", (cik, ticker, name, timestamp))
            print("new security", cik, ticker, name)
        else:
            cur.execute("UPDATE securities SET discontinued = NULL WHERE cik = ? AND ticker = ?", (cik, ticker))

    con.commit()

if __name__ == "__main__":
    db = Database()
    con = db.connection
    securities = security_list()
    update_securities(securities, con)
    con.close()