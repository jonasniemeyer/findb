from finance_data import MacrotrendsReader
from finance_database import Database

if __name__ == '__main__':
    with Database() as db:
        reader = MacrotrendsReader(ticker='AAPL', statement='financial-statement', frequency='Y')
        data = reader.read()

        for statement in data.keys():
            statement_id = db.cur.execute("SELECT statement_id FROM financial_statement_types WHERE name = ?", (statement,)).fetchone()[0]
            for variable in data[statement]:
                db.cur.execute("INSERT OR IGNORE INTO macrotrends_fundamental_variables (name, statement_id) VALUES (?, ?)", (variable, statement_id))