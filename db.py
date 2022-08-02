from finance_database.utils import DB_PATH
from sqlite3 import connect

class Database:
    path = DB_PATH
    
    def __init__(self):
        self.connection = connect(self.path)
        self.cursor = self.connection.cursor()