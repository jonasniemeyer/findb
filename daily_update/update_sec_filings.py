import requests
import datetime as dt
from finance_database import Database, utils

sec_base_url = utils.sec_base_url

def get_filing_lists(first_year=1900, first_quarter=0):
    years_url = f"{sec_base_url}/edgar/daily-index/index.json"
    years = requests.get(years_url, headers=utils.headers).json()
    for year in years["directory"]["item"]:
        try:
            if int(year["name"]) < first_year:
                continue
        except:
            continue
        quarters_url = f"{sec_base_url}/edgar/daily-index/{year['name']}/index.json"
        print(year["name"])
        quarters = requests.get(quarters_url, headers=utils.headers).json()
        for quarter in quarters["directory"]["item"]:
            if int(year["name"]) < first_year and int(quarter['name'][-1]) < first_quarter:
                continue
            print(quarter['name'])
            days_url = f"{sec_base_url}/edgar/daily-index/{year['name']}/{quarter['name']}/index.json"
            days = requests.get(days_url, headers=utils.headers).json()
            for day in days["directory"]["item"]:
                if day["name"].startswith("master"):
                    date = day["name"].split(".")[1]
                    if len(date) == 8:
                        date = "{}-{}-{}".format(date[:4], date[4:6], date[6:])
                    elif int(year["name"]) == 1994:
                        date = "19{}-{}-{}".format(date[4:], date[:2], date[2:4])
                    elif int(date[:2]) > 50:
                        date = "19{}-{}-{}".format(date[:2], date[2:4], date[4:])
                    else:
                        raise ValueError(year["name"])
                    day_url = f"{sec_base_url}/edgar/daily-index/{year['name']}/{quarter['name']}/{day['href']}".rstrip(".gz")
                    if day_url in filing_lists:
                        continue
                    ts_today = int((dt.date.fromisoformat(date) - dt.date(1970, 1, 1)).total_seconds())
                    if cur.execute("SELECT url FROM sec_daily_filings_lists WHERE ts = ?", (ts_today, )).fetchone() is None:
                        cur.execute("INSERT INTO sec_daily_filings_lists (ts, url) VALUES (?, ?)", (ts_today, day_url))
            con.commit()

def get_filings():
    filing_lists = cur.execute("SELECT url FROM sec_daily_filings_lists WHERE parsed IS ?", (None,)).fetchall()
    filing_lists = [item[0] for item in filing_lists]
    for index, day_url in enumerate(filing_lists):
        print(f"{index} of {len(filing_lists)}: {day_url}")
        day = requests.get(day_url, headers=utils.headers).text.split("\n")
        for row in day:
            row = row.split("|")
            if len(row) != 5 or any([item == "" for item in row]):
                continue
            cik, name, form, date, href = row
            try:
                cik = int(cik)
            except:
                continue
            date = "{}-{}-{}".format(date[:4], date[4:6], date[6:])
            ts_filed = int((dt.date.fromisoformat(date) - dt.date(1970, 1, 1)).total_seconds())
            href_split = href.strip().split("/")
            href = f"{sec_base_url}/edgar/data/{href_split[-2]}/{href_split[-1]}"
            if cur.execute("SELECT id FROM form_types WHERE name = ?", (form,)).fetchone() is None:
                cur.execute("INSERT INTO form_types (name) VALUES (?)", (form,))
            form_id = cur.execute("SELECT id FROM form_types WHERE name = ?", (form,)).fetchone()[0]
            if cur.execute("SELECT url FROM sec_filings WHERE cik = ? AND form_type_id = ? AND ts_filed = ? AND url = ?", (cik, form_id, ts_filed, href)).fetchone() is None:
                cur.execute(
                    """
                    INSERT INTO sec_filings (cik, form_type_id, ts_filed, url)
                    VALUES (?, ?, ?, ?)
                    """,
                    (cik, form_id, ts_filed, href)
                )
        cur.execute("UPDATE sec_daily_filings_lists SET parsed = ? WHERE url = ?", (True, day_url))
        con.commit()

if __name__ == "__main__":

    db = Database()
    con = db.connection
    cur = db.cursor

    filing_lists = cur.execute("SELECT ts, url FROM sec_daily_filings_lists ORDER BY ts DESC").fetchall()
    if len(filing_lists) == 0:
        get_filing_lists()
    else:
        last_date_parsed = dt.date.fromtimestamp(filing_lists[0][0])
        year = last_date_parsed.year
        quarter = (last_date_parsed.month - 1) // 3 + 1
        get_filing_lists(first_year=year, first_quarter=quarter)
    
    get_filings()
    con.close()
