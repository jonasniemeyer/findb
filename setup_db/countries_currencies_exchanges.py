import requests
from bs4 import BeautifulSoup
from finance_database import Database
import re
from finance_database.utils import HEADERS

def insert_countries_currencies_exchanges(db) -> None:
    country_url = "https://en.wikipedia.org/wiki/List_of_circulating_currencies"
    html = requests.get(url=country_url, headers=HEADERS).text
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    length = len(table.find_all("tr")[1:])
    for index, row in enumerate(table.find_all("tr")[1:]):
        cells = row.find_all("td")
        if len(cells) == 6:
            country_name = cells[0].find("a").get("title")
            country_name = "Ireland" if country_name == "Republic of Ireland" else country_name.split("(")[0]
            flag_url = "https:" + cells[0].find("img").get("src")
            flag_url_50 = re.sub("[0-9]+px", "50px", flag_url)
            flag_url_100 = re.sub("[0-9]+px", "100px", flag_url)
            flag_url_200 = re.sub("[0-9]+px", "200px", flag_url)
            flag_bytes_50 = requests.get(url=flag_url_50, headers=HEADERS).content
            flag_bytes_100 = requests.get(url=flag_url_100, headers=HEADERS).content
            flag_bytes_200 = requests.get(url=flag_url_200, headers=HEADERS).content
            i = 1
        else:
            i = 0
        currency_name = cells[i].text.split("[")[0].strip()
        currency_name = cells[i].find("a")
        if currency_name is None:
            continue
        currency_name = currency_name.get("title")
        currency_abbr = cells[i+2].text.split("[")[0].strip()
        currency_abbr = None if currency_abbr == "(none)" else currency_abbr

        db.cur.execute(
            """
            INSERT OR IGNORE INTO currency (name, abbr)
            VALUES (?, ?)
            """,
            (currency_name, currency_abbr)
        )

        currency_id = db.cur.execute("SELECT currency_id FROM currency WHERE name = ?", (currency_name,)).fetchone()[0]

        db.cur.execute(
            """
            INSERT OR IGNORE INTO country (name, flag_small, flag_medium, flag_large)
            VALUES (?, ?, ?, ?)
            """,
            (country_name, flag_bytes_50, flag_bytes_100, flag_bytes_200)
        )
        print(f"{index+1:>3} of {length}: {country_name}")
        country_id = db.cur.execute("SELECT country_id FROM country WHERE name = ?", (country_name,)).fetchone()[0]

        db.cur.execute(
            """
            INSERT OR IGNORE INTO country_currency_match (country_id, currency_id)
            VALUES (?, ?)
            """,
            (country_id, currency_id)
        )

    db.cur.execute(
        """
        INSERT OR IGNORE INTO country (name)
        VALUES (?)
        """,
        ("Europe",)
    )

    europe_id = db.cur.execute("SELECT country_id FROM country WHERE name = ?", ("Europe",)).fetchone()[0]
    eur_id = db.cur.execute("SELECT currency_id FROM currency WHERE name = ?", ("Euro",)).fetchone()[0]
    db.cur.execute("INSERT OR IGNORE INTO country_currency_match VALUES (?, ?)", (europe_id, eur_id))

    db.cur.execute(
        """
        INSERT OR IGNORE INTO country (name)
        VALUES (?)
        """,
        (None,)
    )

    db.cur.execute(
        """
        INSERT OR IGNORE INTO country (name)
        VALUES (?)
        """,
        ("Global",)
    )

    exchange_url = "https://help.yahoo.com/kb/exchanges-data-providers-yahoo-finance-sln2310.html"
    html = requests.get(url=exchange_url, headers=HEADERS).text
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        country_name = cells[0].text.strip()
        if country_name == "United States of America":
            country_name = "United States"
        exchange_name = cells[1].text.replace("*", "").strip()
        suffix = cells[2].text.strip()
        suffix = "" if suffix == "N/A" else suffix

        country_id = db.cur.execute("SELECT country_id FROM country WHERE name = ?", (country_name,)).fetchone()[0]
        db.cur.execute(
            """
            INSERT OR IGNORE INTO yahoo_exchange (name, country_id, yahoo_suffix)
            VALUES (?, ?, ?)
            """,
            (exchange_name, country_id, suffix)
        )