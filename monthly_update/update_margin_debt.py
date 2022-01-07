from finance_data import margin_debt
from finance_database import Database

def insert_margin_debt(db_connection):
    cur = db_connection.cursor()
    df = margin_debt(timestamps=True)["combined full"]
    data = []
    for ts in df.index:
        data.append((ts, int(df.loc[ts, "debit"]), int(df.loc[ts, "credit"])))

    cur.executemany("INSERT OR IGNORE INTO margin_debt VALUES (?, ?, ?)", data)
    con.commit()

if __name__ == "__main__":
    db = Database()
    con = db.connection
    insert_margin_debt(con)
    con.close()
