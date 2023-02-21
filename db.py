from finance_database.utils import DB_PATH
from sqlite3 import connect

class Database:    
    def __init__(self):
        self.connection = connect(DB_PATH)
        self.cursor = self.connection.cursor()
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.connection.close()