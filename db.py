from finance_database.utils import db_path
from sqlite3 import connect

class Database:
    db_path = db_path
    
    def __init__(self):
        self.connection = connect(self.db_path)
        self.cursor = self.connection.cursor()