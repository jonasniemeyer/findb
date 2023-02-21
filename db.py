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
    ) -> Union[dict, list]:
        query = """
        SELECT ts, adj_close FROM yahoo_security_prices 
        WHERE security_id = (SELECT id FROM securities WHERE ticker = ?)
        AND ts BETWEEN STRFTIME("%s", ?) AND STRFTIME("%s", ?)
        """

        if isinstance(ticker, str):
            return self.cur.execute(query, (ticker, start, end)).fetchall()
        else:
            data = {}
            for symbol in ticker:
                data[symbol] = self.cur.execute(query, (symbol, start, end)).fetchall()
            return data