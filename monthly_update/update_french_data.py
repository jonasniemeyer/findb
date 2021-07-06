from finance_data import FrenchReader
from finance_database import Database
import datetime as dt

ts = int((dt.date.today() - dt.date(1970,1,1)).total_seconds())

db = Database()
con = db.connection
cur = db.cursor

datasets = FrenchReader.datasets()
for index, dataset in enumerate(datasets):
    print(f"{index} of {len(datasets)}")
    if cur.execute("SELECT id FROM french_datasets WHERE name = ?", (dataset,)).fetchone() is None:
        cur.execute("INSERT INTO french_datasets (name, updated) VALUES (?, ?)", (dataset, ts))
    dataset_id = cur.execute("SELECT id FROM french_datasets WHERE name = ?", (dataset,)).fetchone()[0]
    dfs = FrenchReader(dataset).read()
    for category in dfs.keys():
        if cur.execute("SELECT id FROM french_categories WHERE name = ?", (category, )).fetchone() is None:
            cur.execute("INSERT INTO french_categories (name) VALUES (?)", (category,))
        category_id = cur.execute("SELECT id FROM french_categories WHERE name = ?", (category, )).fetchone()[0]
        df = dfs[category]
        if all([len(str(item)) == 4 for item in df.index]):
            df.index = [dt.date(year, 1, 1) for year in df.index]
        else:
            df.index = [int((item.date() - dt.date(1970,1,1)).total_seconds()) for item in df.index]
        for col in df.columns:
            if cur.execute("SELECT id FROM french_series WHERE name = ? AND dataset_id = ? AND category_id = ?", (col, dataset_id, category_id)).fetchone() is None:
                cur.execute("INSERT INTO french_series (dataset_id, category_id, name) VALUES (?, ?, ?)", (dataset_id, category_id, col))
            series_id = cur.execute("SELECT id FROM french_series WHERE name = ? AND dataset_id = ? AND category_id = ?", (col, dataset_id, category_id)).fetchone()[0]
            data = list(zip(df.index, df[col]))
            data = [(series_id, *item) for item in data]
            cur.executemany("REPLACE INTO french_data VALUES (?, ?, ?)", data)
    con.commit()

con.close()