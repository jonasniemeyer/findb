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
        self.con.commit()
        self.con.close()

    def companies(self) -> list:
        data = self.cur.execute(
            """
            SELECT
                security.ticker      AS ticker,
                security.yahoo_name  AS name
            FROM
                security INNER JOIN company USING(security_id)
            """
        )
        data = [
            {
                "ticker": item[0],
                "name": item[1]
            }
            for item in data
        ]
        return data

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
                yahoo_security_price
            WHERE
                security_id = (SELECT security_id FROM security WHERE ticker = ?)
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
                INNER JOIN security_news_match  USING (news_id)
                INNER JOIN news_source          USING(source_id)
            WHERE
                security_news_match.security_id = (SELECT id FROM security WHERE ticker = ?)
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
                    security
                WHERE
                    id IN (
                        SELECT security_id FROM company WHERE gics_industry_id = (
                            SELECT gics_industry_id FROM company WHERE security_id = (
                                SELECT security_id FROM security WHERE ticker = ?
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
                    security
                WHERE
                    id IN (
                        SELECT security_id FROM company WHERE sic_industry_id = (
                            SELECT sic_industry_id FROM company WHERE security_id = (
                                SELECT security_id FROM security WHERE ticker = ?
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
                security.ticker                     AS ticker,
                security.yahoo_name                 AS name,
                security.isin                       AS isin,
                security.cik                        AS cik,
                security.description                AS description,
                company.website                     AS website,
                industry_classification_gics.name   AS gics,
                industry_classification_sic.name    AS sic,
                countries.name                      AS country,
                company.zip                         AS zip,
                yahoo_cities.name                   AS city,
                company.address1                    AS address1,
                company.address2                    AS address2,
                company.address3                    AS address3,
                company.employees                   AS employees
            FROM
                security
                INNER JOIN  company                         USING(security_id)
                LEFT JOIN   industry_classification_gics    ON company.gics_industry_id = industry_classification_gics.industry_id
                LEFT JOIN   industry_classification_sic     ON company.sic_industry_id = industry_classification_sic.industry_id
                LEFT JOIN   countries                       USING(country_id)
                LEFT JOIN   yahoo_cities                    USING (city_id)
            WHERE
                security.ticker = ?
            """,
            (ticker,)).fetchone()

        dct = {}
        for index, col in enumerate(self.cur.description):
            dct[col[0]] = data[index]
        return dct