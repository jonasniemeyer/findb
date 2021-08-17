from pathlib import Path
from finance_database import Database

db = Database()
con = db.connection
cur = db.cursor

# ===========================================================
# ===================== General =============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        flag BLOB
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        country_id INTEGER,
        UNIQUE(name, country_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS currencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        abbr TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS country_currency_match (
        country_id INTEGER,
        currency_id INTEGER,
        PRIMARY KEY(country_id, currency_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS exchanges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        yahoo_suffix TEXT,
        country_id TEXT,
        UNIQUE(name, country_id, yahoo_suffix)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS indices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        ticker TEXT,
        country_id INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS index_constituents (
        index_id INTEGER,
        security_id INTEGER,
        PRIMARY KEY(index_id, security_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS financial_statement_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """
)

cur.executescript(
    """
    INSERT INTO financial_statement_types (name) VALUES ("income statement");
    INSERT INTO financial_statement_types (name) VALUES ("balance sheet");
    INSERT INTO financial_statement_types (name) VALUES ("cashflow statement");
    INSERT INTO financial_statement_types (name) VALUES ("statement of changes in equity");
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_daily_filings_lists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER UNIQUE,
        url TEXT UNIQUE,
        parsed INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS form_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_filings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cik INTEGER,
        form_type_id INTEGER,
        ts_filed INTEGER,
        url TEXT,
        parsed INTEGER,
        UNIQUE(cik, form_type_id, ts_filed, url)
    )
    """
)

# ===========================================================
# ====================== Securities =========================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS securities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cik INTEGER,
        ticker TEXT,
        yahoo_name TEXT,
        description TEXT,
        type_id INTEGER,
        currency_id INTEGER,
        sec_name TEXT,
        isin TEXT,
        exchange INTEGER,
        added INTEGER,
        discontinued INTEGER,
        old_name TEXT,
        profile_updated INTEGER,
        prices_updated INTEGER,
        UNIQUE(cik, ticker)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS security_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS companies (
        security_id INTEGER PRIMARY KEY,
        sic_industry_id INTEGER,
        gics_industry_id INTEGER,
        website TEXT,
        country_id INTEGER,
        city_id INTEGER,
        address1 TEXT,
        address2 TEXT,
        zip TEXT,
        employees INTEGER,
        fiscal_year_end INTEGER,
        yahoo_fundamentals_updated INTEGER,
        macrotrends_fundamentals_updated INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS executives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        born INTEGER,
        UNIQUE(name, born)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS executive_positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS company_executive_match (
        security_id INTEGER,
        executive_id INTEGER,
        position_id INTEGER,
        salary REAL,
        added INTEGER,
        discontinued INTEGER,
        PRIMARY KEY(security_id, executive_id, position_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS security_prices (
        security_id INTEGER,
        ts INTEGER,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        adj_close REAL,
        volume INTEGER,
        dividends REAL,
        split_ratio REAL,
        simple_return REAL,
        log_return REAL,
        PRIMARY KEY(security_id, ts)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS analysts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS analyst_recommendations (
        analyst_id INTEGER,
        security_id INTEGER,
        ts INTEGER,
        old INTEGER,
        new INTEGER,
        change INTEGER,
        PRIMARY KEY(analyst_id, security_id, ts)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS recommendation_trend (
        security_id INTEGER,
        ts INTEGER,
        month INTEGER,
        number INTEGER,
        average INTEGER,
        strong_buy INTEGER,
        buy INTEGER,
        hold INTEGER,
        sell INTEGER,
        strong_sell INTEGER,
        UNIQUE(security_id, ts, month)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fundamental_variables_sec (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        statement_id INTEGER,
        UNIQUE(name, statement_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fundamental_data_sec (
        security_id INTEGER,
        variable_id INTEGER,
        quarter INTEGER,
        year INTEGER,
        ts INTEGER,
        value INTEGER,
        filing_id INTEGER,
        PRIMARY KEY(security_id, quarter, year, variable_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fundamental_variables_macrotrends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        statement_id INTEGER,
        UNIQUE(name, statement_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fundamental_data_macrotrends (
        security_id INTEGER,
        variable_id INTEGER,
        quarter INTEGER,
        year INTEGER,
        ts INTEGER,
        value INTEGER,
        PRIMARY KEY(security_id, variable_id, quarter, year)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fundamental_variables_yahoo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        statement_id INTEGER,
        UNIQUE(name, statement_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fundamental_data_yahoo (
        security_id INTEGER,
        variable_id INTEGER,
        quarter INTEGER,
        year INTEGER,
        ts INTEGER,
        value INTEGER,
        PRIMARY KEY(security_id, variable_id, quarter, year)
    )
    """
)

# ===========================================================
# ===================== Factors =============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS french_datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        updated INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS french_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS french_series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id INTEGER,
        category_id INTEGER,
        name TEXT,
        UNIQUE(dataset_id, category_id, name)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS french_data (
        series_id INTEGER,
        ts INTEGER,
        value REAL,
        PRIMARY KEY(series_id, ts)
    )
    """
)

# ===========================================================
# ================== 13F Filings ============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS investment_managers (
        cik INTEGER PRIMARY KEY,
        name TEXT
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS investment_manager_holdings (
        investment_manager_id INTEGER,
        quarter INTEGER,
        year INTEGER,
        ts INTEGER,
        cusip_id INTEGER,
        no_shares INTEGER,
        market_value REAL,
        option_id INTEGER,
        filing_id INTEGER,
        PRIMARY KEY(investment_manager_id, cusip_id, quarter, year, option_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """
)

# ===========================================================
# ================== 13D/G Filings ==========================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cusips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cusip TEXT
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS acquisitions (
        cik INTEGER,
        cusip_id INTEGER,
        ts INTEGER,
        shares INTEGER,
        percentage REAL,
        filing_id INTEGER,
        PRIMARY KEY(cik, cusip_id, ts)
    )
    """
)

# ===========================================================
# =================== Industry Groups =======================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sic_divisions (
        id INTEGER PRIMARY KEY,
        character TEXT UNIQUE,
        name TEXT UNIQUE,
        no_businesses INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sic_industries (
        id INTEGER PRIMARY KEY,
        name TEXT,
        no_businesses INTEGER,
        industry_group_id INTEGER,
        major_group_id INTEGER,
        division_id INTEGER,
        UNIQUE(name, industry_group_id, major_group_id, division_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS gics_sectors (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS gics_industries (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        sector_id INTEGER
    )
    """
)

# ===========================================================
# ================== Volatility =============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS vix_prices (
        maturity_date INTEGER,
        ts INTEGER,
        price REAL,
        volume INTEGER,
        PRIMARY KEY(maturity_date, ts)
    )
    """
)

# ===========================================================
# ================== Commodities ============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS commodities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        exchange_id INTEGER,
        sector_id INTEGER,
        prices_updated INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS commodity_sectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """
)

cur.executescript(
    """
    INSERT OR IGNORE INTO commodity_sectors (name) VALUES("Agriculture");
    INSERT OR IGNORE INTO commodity_sectors (name) VALUES("Energy");
    INSERT OR IGNORE INTO commodity_sectors (name) VALUES("Industrial Metals");
    INSERT OR IGNORE INTO commodity_sectors (name) VALUES("Livestock");
    INSERT OR IGNORE INTO commodity_sectors (name) VALUES("Precious Metals");
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS commodity_prices (
        commodity_id INTEGER,
        maturity_month INTEGER,
        maturity_year INTEGER,
        ts_maturity INTEGER,
        ts INTEGER,
        price REAL,
        volume INTEGER,
        PRIMARY KEY(commodity_id, maturity_month, maturity_year, ts)
    )
    """
)

# ===========================================================
# ================== Margin Debt ============================
# ===========================================================


cur.execute(
    """
    CREATE TABLE IF NOT EXISTS margin_debt (
        ts INTEGER PRIMARY KEY,
        debit INTEGER,
        credit INTEGER
    )
    """
)

# ===========================================================
# ================= Macroeconomic Data ======================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fred_categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        super_category_id INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fred_series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        abbr TEXT,
        name TEXT,
        description TEXT,
        category_id INTEGER,
        UNIQUE(abbr, name)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fred_data (
        series_id INTEGER,
        ts INTEGER,
        value REAL,
        PRIMARY KEY(series_id, ts)
    )
    """
)

con.commit()
con.close()