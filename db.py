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
        self.connection.close()
    
    def security_prices(
        self,
        ticker,
        start="1900-01-01",
        end=pd.to_datetime("today").isoformat()
    ) -> list:
        data = self.cur.execute(
            """
            SELECT ts, adj_close FROM yahoo_security_prices
            WHERE security_id = (SELECT id FROM securities WHERE ticker = ?)
            AND ts BETWEEN STRFTIME("%s", ?) AND STRFTIME("%s", ?)
            """,
            (ticker, start, end)).fetchall()
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
            news_source.name,
            security_news.header,
            security_news.description,
            security_news.url
            FROM security_news INNER JOIN security_news_match INNER JOIN news_source
            ON security_news.id = security_news_match.news_id AND security_news.source_id = news_source.id
            WHERE security_news_match.security_id = (SELECT id FROM securities WHERE ticker = ?)
            AND security_news.ts BETWEEN STRFTIME("%s", ?) AND STRFTIME("%s", ?)
            """,
            (ticker, start, end)).fetchall()
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
                ticker,
                yahoo_name
                FROM securities
                WHERE id IN (
                    SELECT security_id FROM companies WHERE gics_industry_id = (
                        SELECT gics_industry_id FROM companies WHERE security_id = (
                            SELECT id FROM securities WHERE ticker = ?
                        )
                    )
                )
                AND ticker NOT LIKE ?
                ORDER BY ticker
                """,
                (ticker, ticker+"%")).fetchall()
        else:
            data = self.cur.execute(
                """
                SELECT
                ticker,
                yahoo_name
                FROM securities
                WHERE id IN (
                    SELECT security_id FROM companies WHERE sic_industry_id = (
                        SELECT sic_industry_id FROM companies WHERE security_id = (
                            SELECT id FROM securities WHERE ticker = ?
                        )
                    )
                )
                AND ticker NOT LIKE ?
                ORDER BY ticker
                """,
                (ticker, ticker+"%")).fetchall()
        return data
    
    def company_profile(self, ticker) -> dict:
        data = self.cur.execute(
            """
            SELECT
            securities.ticker AS ticker,
            securities.yahoo_name AS name,
            securities.isin AS isin,
            securities.cik AS cik,
            securities.description AS description,
            companies.website AS website,
            (SELECT name FROM industry_classification_gics WHERE id = companies.gics_industry_id) AS gics,
            (SELECT name FROM industry_classification_sic WHERE id = companies.sic_industry_id) AS sic,
            (SELECT name FROM countries WHERE id = companies.country_id) AS country,
            companies.zip AS zip,
            (SELECT name FROM yahoo_cities WHERE id = companies.city_id) AS city,
            companies.address1 AS address1,
            companies.address2 AS address2,
            companies.employees AS employees
            FROM
            securities INNER JOIN companies
            ON securities.id = companies.security_id
            WHERE securities.ticker = ?
            """,
            (ticker,)).fetchall()
        return data