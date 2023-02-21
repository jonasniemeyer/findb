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
            source.name,
            news.header,
            news.description,
            news.url
            FROM security_news news 
            INNER JOIN security_news_match match
            INNER JOIN news_source source
            ON news.id = match.news_id AND news.source_id = source.id
            WHERE match.security_id = (SELECT id FROM securities WHERE ticker = ?)
            AND news.ts BETWEEN STRFTIME("%s", ?) AND STRFTIME("%s", ?)
            """,
            (ticker, start, end)).fetchall()
        return data