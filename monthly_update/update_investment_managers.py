from glob import glob
from pathlib import Path
from finance_database import Database

managers = []

directory = Path(__file__).parent.parent
paths = glob(f"{directory}/sec_daily_filings/*/*")
for path in paths:
    with open(path) as file:
        data = file.readlines()
        for row in data:
            row = row.split('|')
            if len(row) == 5:
                cik, name, type_, date, url = row
                if type_ in ("13F-HR", "13F-HR/A"):
                    managers.append((int(cik), name))

managers = set(managers)

db = Database()
con = db.connection
cur = db.cursor

cur.executemany("INSERT OR IGNORE INTO investment_managers VALUES(?, ?)", managers)

con.commit()
con.close()
