from finance_database.utils import DB_PATH
from sqlite3 import connect
from typing import Union
import pandas as pd

class Database:    
    def __init__(self):
        self.connection = connect(DB_PATH)
        self.con = self.connection
        self.cursor = self.connection.cursor()
        self.cur = self.cursor
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.co
        self.connection.close()
    
    def security_prices(
        self,
        ticker,
        start="1900-01-01",
        end=pd.to_datetime("today").isoformat()
    ) -> dict:
        data = self.cur.execute(
            """
            SELECT
                ts          AS ts,
                adj_close   AS close
            FROM
                yahoo_security_prices
            WHERE
                security_id = (SELECT id FROM securities WHERE ticker = ?)
                AND ts BETWEEN STRFTIME("%s", ?) AND STRFTIME("%s", ?)
            """,
            (ticker, start, end)).fetchall()
        data = {item[0]: item[1] for item in data}
        return data

    def security_news(
        self,
        ticker,
        start="1900-01-01",
        end=pd.to_datetime("today").isoformat()
    ) -> list:
        data = self.cur.execute(
            """
            SELECT
                news_source.name            AS source,
                security_news.header        AS header,
                security_news.description   AS description,
                security_news.url           AS url
            FROM
                security_news
                INNER JOIN  security_news_match
                INNER JOIN  news_source
            ON
                security_news.id = security_news_match.news_id
                AND security_news.source_id = news_source.id
            WHERE
                security_news_match.security_id = (SELECT id FROM securities WHERE ticker = ?)
                AND security_news.ts BETWEEN STRFTIME("%s", ?) AND STRFTIME("%s", ?)
            """,
            (ticker, start, end)).fetchall()

        cols = [item[0] for item in self.cur.description]
        data = [
            {
                cols[0]: item[0],
                cols[1]: item[1],
                cols[2]: item[2],
                cols[3]: item[3]
            }
            for item in data
        ]
        return data
    
    def competitors(
        self,
        ticker,
        classification="gics"
    ) -> list:
        if classification.lower() == "gics":
            data = self.cur.execute(
                """
                SELECT
                    ticker      AS ticker,
                    yahoo_name  AS name,
                FROM
                    securities
                WHERE
                    id IN (
                        SELECT security_id FROM companies WHERE gics_industry_id = (
                            SELECT gics_industry_id FROM companies WHERE security_id = (
                                SELECT id FROM securities WHERE ticker = ?
                            )
                        )
                    )
                    AND ticker NOT LIKE ?
                ORDER BY
                    ticker
                """,
                (ticker, ticker+"%")).fetchall()
        else:
            data = self.cur.execute(
                """
                SELECT
                    ticker      AS ticker,
                    yahoo_name  AS name,
                FROM
                    securities
                WHERE
                    id IN (
                        SELECT security_id FROM companies WHERE sic_industry_id = (
                            SELECT sic_industry_id FROM companies WHERE security_id = (
                                SELECT id FROM securities WHERE ticker = ?
                            )
                        )
                    )
                AND
                    ticker NOT LIKE ?
                ORDER BY
                    ticker
                """,
                (ticker, ticker+"%")).fetchall()
        data = [
            {
                "ticker": item[0],
                "name": item[1]
            }
            for item in data
        ]
        return data
    
    def company_profile(self, ticker) -> dict:
        data = self.cur.execute(
            """
            SELECT
                securities.ticker                   AS ticker,
                securities.yahoo_name               AS name,
                securities.isin                     AS isin,
                securities.cik                      AS cik,
                securities.description              AS description,
                companies.website                   AS website,
                industry_classification_gics.name   AS gics,
                industry_classification_sic.name    AS sic,
                countries.name                      AS country,
                companies.zip                       AS zip,
                yahoo_cities.name                   AS city,
                companies.address1                  AS address1,
                companies.address2                  AS address2,
                companies.employees                 AS employees
            FROM
                securities
                INNER JOIN  companies
                LEFT JOIN   industry_classification_gics
                LEFT JOIN   industry_classification_sic
                LEFT JOIN   countries
                LEFT JOIN   yahoo_cities
            ON
                companies.security_id = securities.id
                AND companies.gics_industry_id = industry_classification_gics.code
                AND companies.sic_industry_id = industry_classification_sic.code
                AND companies.country_id = countries.id
                AND companies.city_id = yahoo_cities.id
            WHERE
                securities.ticker = ?
            """,
            (ticker,)).fetchone()

        dct = {}
        for index, col in enumerate(self.cur.description):
            dct[col[0]] = data[index]
        return dct