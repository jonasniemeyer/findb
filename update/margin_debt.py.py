from findata import finra_margin_debt
from findb import Database

def insert_margin_debt(db):
    cur = db.connection.cursor()
    df = finra_margin_debt(timestamps=True)

    df.reset_index(inplace=True)
    cur.executemany("INSERT OR IGNORE INTO finra_margin_debt VALUES (?, ?, ?, ?)", df.to_numpy())
    db.connection.commit()

if __name__ == "__main__":
    with Database() as db:
        insert_margin_debt(db)
