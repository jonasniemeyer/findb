from finance_data import margin_debt
from finance_database import Database
import datetime as dt

def insert_margin_debt(db_connection):
    cur = db_connection.cursor()
    df = margin_debt()["combined full"]
    data = []
    for index in df.index:
        ts = int((index - dt.date(1970,1,1)).total_seconds())
        data.append((ts, int(df.loc[index, "debit"]), int(df.loc[index, "credit"])))

    cur.executemany("INSERT OR IGNORE INTO margin_debt VALUES (?, ?, ?)", data)
    con.commit()

if __name__ == "__main__":
    db = Database()
    con = db.connection
    insert_margin_debt(con)
    con.close()
