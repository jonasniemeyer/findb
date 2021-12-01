from finance_database import Database
from finance_data import Filing13D
import datetime as dt

ts_today = int((dt.date.today() - dt.date(1970,1,1)).total_seconds())

db = Database()
con = db.connection
cur = db.cursor

forms = (
    "SC 13D",
    "SC 13D/A",
    "SC 13G",
    "SC 13G/A"
)

form_ids = cur.execute(
    f"SELECT id FROM form_types WHERE name IN {forms}",
).fetchall()
form_ids = tuple([item[0] for item in form_ids])

data = cur.execute(f"SELECT id, url FROM sec_filings WHERE form_type_id IN {form_ids} AND parsed IS NULL ORDER BY ts_filed ASC").fetchall()
no_files = len(data)
print(no_files)

for index, (filing_id, url) in enumerate(data):
    print(f"{index} of {no_files}", url)
    try:
        file = Filing13D.from_url(url)
        cusip = file.subject["cusip"]
        shares = file.shares_acquired
        percentage = file.percent_acquired
    except:
        cur.execute("UPDATE sec_filings SET parsed = ? WHERE id = ?", (True, filing_id))
        print("\t\t\tfailed")
        continue
    cik_subject = file.subject["cik"]
    ts_filed = int((dt.date.fromisoformat(file.filing_date) - dt.date(1970,1,1)).total_seconds())

    sic_code_subject = file.subject["sic_code"]
    cur.execute("UPDATE companies SET sic_industry_id = ? WHERE security_id = (SELECT id FROM securities WHERE cik = ?)", (sic_code_subject, cik_subject))

    cur.execute("INSERT OR IGNORE INTO cusips (cusip) VALUES (?)", (cusip,))
    cusip_id = cur.execute("SELECT id FROM cusips WHERE cusip = ?", (cusip,)).fetchone()[0]

    for filer in file.filer:
        cik_filer = filer["cik"]
        try:
            sic_code_filer = file.filer["sic_code"]
            cur.execute("UPDATE companies SET sic_industry_id = ? WHERE security_id = (SELECT id FROM securities WHERE cik = ?)", (sic_code_filer, cik_filer))
        except:
            pass
        cur.execute(
            "INSERT OR IGNORE INTO acquisitions VALUES (?, ?, ?, ?, ?, ?, ?)",
            (cik_filer, cik_subject, cusip_id, ts_filed, shares, percentage, filing_id)
        )

    cur.execute("UPDATE sec_filings SET parsed = ? WHERE id = ?", (True, filing_id))
    
    if index % 100 == 0:
        con.commit()

con.commit()
con.close()


