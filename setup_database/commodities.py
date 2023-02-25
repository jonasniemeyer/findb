from finance_data import CMEReader
from finance_database import Database

with Database() as db:
    for name, properties in CMEReader.commodities.items():
        sector_id = db.cur.execute(f"SELECT sector_id FROM cme_commodity_sectors WHERE name = ?", (properties["sector_name"],)).fetchone()[0]
        exchange_id = db.cur.execute(f"SELECT exchange_id FROM yahoo_exchanges WHERE yahoo_suffix = '.CME'").fetchone()[0]
        db.cur.execute(
            f"INSERT OR IGNORE INTO cme_commodities (name, exchange_id, sector_id) VALUES (?, ?, ?)",
            (name, exchange_id, sector_id)
        )