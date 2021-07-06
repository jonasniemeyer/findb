from finance_data import MacrotrendsReader
from finance_database import Database

if __name__ == '__main__':
    db = Database()
    con = db.connection
    cur = db.cursor

    reader = MacrotrendsReader(ticker='AAPL', statement='financial-statement', frequency='Y')
    reader.open_website()
    data = reader.parse()

    for statement in data.keys():
        statement_ = statement.replace("_", " ")
        statement_id = cur.execute("SELECT id FROM financial_statement_types WHERE name = ?", (statement_,)).fetchone()[0]
        for variable in data[statement]:
            cur.execute("INSERT OR IGNORE INTO fundamental_variables_macrotrends (name, statement_id) VALUES (?, ?)", (variable, statement_id))

    con.commit()
    con.close()