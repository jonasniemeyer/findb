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
                security.ticker         AS ticker,
                security.yahoo_name     AS name
            FROM
                security
            WHERE
                yahoo_type_id = (
                    SELECT type_id FROM yahoo_security_type WHERE name = "EQUITY"
                )
            ORDER BY ticker ASC
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
        adjusted=False,
        start="1900-01-01",
        end=pd.to_datetime("today").isoformat()
    ) -> dict:
        adjusted = "adj_" if adjusted is True else ""
        data = self.cur.execute(
            f"""
            SELECT
                ts                  AS ts,
                {adjusted}close     AS close
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
                security_news_match.security_id = (SELECT security_id FROM security WHERE ticker = ?)
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
                    MIN(security.ticker)        AS ticker,
                    security.yahoo_name         AS name
                FROM
                    entity
                    LEFT JOIN security USING(entity_id)
                WHERE
                    gics_industry_id = (
                        SELECT gics_industry_id FROM entity WHERE entity_id = (
                            SELECT entity_id FROM security WHERE ticker = ?
                        )
                    )
                    AND yahoo_type_id = (SELECT type_id FROM yahoo_security_type WHERE name = "EQUITY")
                GROUP BY
                    name
                HAVING
                    ticker != ?
                ORDER BY
                    ticker
                """,
                (ticker, ticker)).fetchall()
        else:
            data = self.cur.execute(
                """
                SELECT
                    security.ticker         AS ticker,
                    security.yahoo_name     AS name
                FROM
                    entity
                    LEFT JOIN security USING(entity_id)
                WHERE
                    sic_industry_id = (
                        SELECT sic_industry_id FROM entity WHERE entity_id = (
                            SELECT entity_id FROM security WHERE ticker = ?
                        )
                    )
                    AND yahoo_type_id = (SELECT type_id FROM yahoo_security_type WHERE name = "EQUITY")
                GROUP BY
                    name
                HAVING
                    ticker != ?
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
                entity.lei                          AS lei,
                entity.cik                          AS cik,
                security.description                AS description,
                entity.website                      AS website,
                yahoo_gics_industry.name            AS gics,
                industry_classification_sic.name    AS sic,
                country.name                        AS country,
                entity.zip                          AS zip,
                yahoo_city.name                     AS city,
                entity.address1                     AS address1,
                entity.address2                     AS address2,
                entity.address3                     AS address3,
                entity.employees                    AS employees
            FROM
                security
                INNER JOIN  entity                          USING(entity_id)
                LEFT JOIN   yahoo_gics_industry             ON entity.gics_industry_id = yahoo_gics_industry.industry_id
                LEFT JOIN   industry_classification_sic     ON entity.sic_industry_id = industry_classification_sic.industry_id
                LEFT JOIN   country                         USING(country_id)
                LEFT JOIN   yahoo_city                      USING (city_id)
            WHERE
                security.ticker = ?
            """,
            (ticker,)).fetchone()

        dct = {}
        for index, col in enumerate(self.cur.description):
            dct[col[0]] = data[index]
        return dct
