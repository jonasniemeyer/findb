import requests
import pandas as pd
from finance_database import Database
from finance_database.utils import SEC_BASE_URL, HEADERS

def get_sec_filing_lists(start_year=1900, start_quarter=0):
    url = f"{SEC_BASE_URL}/edgar/daily-index/index.json"
    years = requests.get(url=url, headers=HEADERS).json()
    for year in years["directory"]["item"]:
        if year["type"] == "dir" and len(year["name"]) == 4:
            if int(year["name"]) < start_year:
                continue
            print(f"Year {year['name']}")

            year_url = f"{SEC_BASE_URL}/edgar/daily-index/{year['name']}/index.json"
            quarters = requests.get(url=year_url, headers=HEADERS).json()
            for quarter in quarters["directory"]["item"]:
                if int(quarter["name"][-1]) < start_quarter and int(year["name"]) == start_year:
                    continue
                print(f"{quarter['name']}")

                quarter_url = f"{SEC_BASE_URL}/edgar/daily-index/{year['name']}/{quarter['name']}/index.json"
                days = requests.get(url=quarter_url, headers=HEADERS).json()
                for day in days["directory"]["item"]:
                    file_name = day["name"]
                    if not file_name.startswith("master"):
                        continue
                    if len(file_name.split(".")) == 2:
                        continue
                    date = file_name.split(".")[1]
                    if len(date) == 8:
                        date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
                    elif int(year["name"]) == 1994:
                        date = f"19{date[4:]}-{date[:2]}-{date[2:4]}"
                    elif int(date[:2]) > 50:
                        date = f"19{date[:2]}-{date[2:4]}-{date[4:]}"
                    day_url = f"{SEC_BASE_URL}/edgar/daily-index/{year['name']}/{quarter['name']}/{day['href']}".rstrip(".gz")
                    ts = int(pd.to_datetime(date).timestamp())
                    cur.execute("INSERT OR IGNORE INTO sec_daily_list (ts, url, parsed) VALUES (?, ?, ?)", (ts, day_url, False))
                con.commit()

def scrape_sec_filing_lists():
    filing_lists = cur.execute("SELECT list_id, url FROM sec_daily_list WHERE parsed = ?", (False,)).fetchall()
    total_filings = len(filing_lists)
    trail = len(str(total_filings))

    for index, (list_id, url) in enumerate(filing_lists):
        print(f"{index+1:>{trail}} of {total_filings}: {url}")
        file = requests.get(url=url, headers=HEADERS).text.split("\n")
        for row in file:
            row = row.split("|")
            if len(row) != 5 or any([item == "" for item in row]):
                continue
            cik, _, form, date, href = row
            if cik.strip() == "CIK":
                continue
            cik = int(cik)
            date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
            ts_filed = int(pd.to_datetime(date).timestamp())
            href_split = href.strip().split("/")
            document_url = f"{SEC_BASE_URL}/edgar/data/{href_split[-2]}/{href_split[-1]}"
            accession = href_split[-1].split(".")[0].replace("-", "")
            filing_url = f"{SEC_BASE_URL}/edgar/data/{href_split[-2]}/{accession}/{href_split[-1].replace('.txt', '-index.html')}"
            cur.execute("INSERT OR IGNORE INTO sec_form_type (name) VALUES (?)", (form,))
            form_id = cur.execute("SELECT type_id FROM sec_form_type WHERE name = ?", (form,)).fetchone()[0]
            cur.execute(
                """
                INSERT OR IGNORE INTO sec_filing (cik, type_id, ts_filed, filing_url, document_url, parsed, list_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (cik, form_id, ts_filed, filing_url, document_url, False, list_id)
            )
        cur.execute("UPDATE sec_daily_list SET parsed = ? WHERE url = ?", (True, url))
        con.commit()

if __name__ == "__main__":
    db = Database()
    con = db.connection
    cur = db.cursor

    filing_lists = cur.execute("SELECT ts, url FROM sec_daily_list ORDER BY ts DESC LIMIT 1").fetchall()

    # if there are no filing lists in the database, scrape all lists. Else, scrape only those that are dated later
    print("Scraping SEC Daily Filing Lists")
    if len(filing_lists) == 0:
        get_sec_filing_lists()
    else:
        last_date_parsed = pd.to_datetime(filing_lists[0][0], unit="s")
        year = last_date_parsed.year
        quarter = (last_date_parsed.month - 1) // 3 + 1
        get_sec_filing_lists(start_year=year, start_quarter=quarter)
    
    print("Scraping SEC Filings")
    scrape_sec_filing_lists()
    con.close()
