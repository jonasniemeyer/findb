from findata import FrenchReader, DatasetError
from findb import Database
import datetime as dt

def insert_french_data(db):
    ts = int((dt.date.today() - dt.date(1970,1,1)).total_seconds())

    datasets = FrenchReader.datasets()
    length = len(datasets)
    trail = len(str(length))

    for index, dataset in enumerate(datasets[105:]):
        print(f"{index+1:{trail}} of {length}: {dataset}")
        db.cur.execute("INSERT OR IGNORE INTO french_dataset (name, updated) VALUES (?, ?)", (dataset, ts))
        dataset_id = db.cur.execute("SELECT dataset_id FROM french_dataset WHERE name = ?", (dataset,)).fetchone()[0]
        try:
            dfs = FrenchReader(dataset, timestamps=True).read()
        except DatasetError:
            print("\tfailed")
            continue
        for table in dfs.keys():
            db.cur.execute("INSERT OR IGNORE INTO french_table (name) VALUES (?)", (table,))
            table_id = db.cur.execute("SELECT table_id FROM french_table WHERE name = ?", (table, )).fetchone()[0]
            df = dfs[table]
            if all([len(str(item)) == 4 for item in df.index]):
                df.index = [dt.datetime(year, 1, 1) for year in df.index]
            for col in df.columns:
                db.cur.execute("INSERT OR IGNORE INTO french_series (dataset_id, table_id, name) VALUES (?, ?, ?)", (dataset_id, table_id, col))
                series_id = db.cur.execute("SELECT series_id FROM french_series WHERE name = ? AND dataset_id = ? AND table_id = ?", (col, dataset_id, table_id)).fetchone()[0]
                data = list(zip(df.index, df[col]))
                data = [(series_id, *item) for item in data]
                db.cur.executemany("REPLACE INTO french_data VALUES (?, ?, ?)", data)
        db.con.commit()

    db.con.close()

if __name__ == "__main__":
    with Database() as db:
        insert_french_data(db)