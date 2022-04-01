from pathlib import Path
from finance_database import Database
import sqlite3

db = Database()
con = db.connection
cur = db.cursor

# ===========================================================
# ===================== General =============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        flag_small BLOB,
        flag_medium BLOB,
        flag_large BLOB
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country_id INTEGER NOT NULL,
        UNIQUE(name, country_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS currencies (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
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
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        yahoo_suffix TEXT NOT NULL,
        country_id INTEGER NOT NULL,
        UNIQUE(name, country_id, yahoo_suffix)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS indices (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        ticker TEXT NOT NULL,
        country_id INTEGER NOT NULL
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
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.executescript(
    """
    INSERT OR IGNORE INTO financial_statement_types (name) VALUES ("income statement");
    INSERT OR IGNORE INTO financial_statement_types (name) VALUES ("balance sheet");
    INSERT OR IGNORE INTO financial_statement_types (name) VALUES ("cashflow statement");
    INSERT OR IGNORE INTO financial_statement_types (name) VALUES ("statement of changes in equity");
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_daily_filings_lists (
        id INTEGER PRIMARY KEY,
        ts INTEGER UNIQUE NOT NULL,
        url TEXT UNIQUE NOT NULL,
        parsed INTEGER NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS form_types (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_filings (
        id INTEGER PRIMARY KEY,
        cik INTEGER NOT NULL,
        form_type_id INTEGER NOT NULL,
        ts_filed INTEGER NOT NULL,
        url TEXT NOT NULL,
        parsed INTEGER NOT NULL,
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
        id INTEGER PRIMARY KEY,
        cik INTEGER NOT NULL,
        ticker TEXT NOT NULL,
        isin TEXT,
        yahoo_name TEXT,
        description TEXT,
        logo BLOB,
        type_id INTEGER,
        currency_id INTEGER,
        utc_offset INTEGER,
        sec_name TEXT,
        exchange_id INTEGER,
        added INTEGER NOT NULL,
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
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
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
    CREATE TABLE IF NOT EXISTS security_news (
        id INTEGER PRIMARY KEY,
        source_id INTEGER NOT NULL,
        type_id INTEGER NOT NULL,
        ts INTEGER NOT NULL,
        header TEXT NOT NULL,
        url TEXT NOT NULL,
        UNIQUE(source_id, type_id, url)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS security_news_match (
        security_id INTEGER,
        news_id INTEGER,
        PRIMARY KEY(security_id, news_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS news_source (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS news_type (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS executives (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        born INTEGER,
        UNIQUE(name, born)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS executive_positions (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
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
        added INTEGER NOT NULL,
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
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS analyst_recommendations (
        analyst_id INTEGER,
        security_id INTEGER,
        ts INTEGER,
        old INTEGER NOT NULL,
        new INTEGER NOT NULL,
        change INTEGER NOT NULL,
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
        average REAL,
        strong_buy INTEGER,
        buy INTEGER,
        hold INTEGER,
        sell INTEGER,
        strong_sell INTEGER,
        PRIMARY KEY(security_id, ts, month)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fundamental_variables_sec (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        statement_id INTEGER NOT NULL,
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
        ts INTEGER NOT NULL,
        value INTEGER,
        filing_id INTEGER NOT NULL,
        PRIMARY KEY(security_id, variable_id, quarter, year)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fundamental_variables_macrotrends (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        statement_id INTEGER NOT NULL,
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
        ts INTEGER NOT NULL,
        value INTEGER,
        PRIMARY KEY(security_id, variable_id, quarter, year)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fundamental_variables_yahoo (
        id INTEGER PRIMARY KEY,
        name TEXT, NOT NULL
        statement_id INTEGER NOT NULL,
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
        ts INTEGER NOT NULL,
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
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        updated INTEGER NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS french_categories (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS french_series (
        id INTEGER PRIMARY KEY,
        dataset_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        name TEXT NOT NULL,
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
        id INTEGER PRIMARY KEY,
        cik INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS investment_manager_holdings (
        investment_manager_id INTEGER,
        quarter INTEGER,
        year INTEGER,
        ts INTEGER NOT NULL,
        cusip_id INTEGER,
        percentage REAL,
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
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

# ===========================================================
# ================== 13D/G Filings ==========================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cusips (
        id INTEGER PRIMARY KEY,
        cusip TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS acquisitions (
        cik_filer INTEGER NOT NULL,
        cik_subject INTEGER NOT NULL,
        cusip_id INTEGER NOT NULL,
        ts INTEGER NOT NULL,
        shares INTEGER NOT NULL,
        percentage REAL NOT NULL,
        filing_id INTEGER,
        PRIMARY KEY(filing_id)
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
        character TEXT UNIQUE NOT NULL,
        name TEXT UNIQUE NOT NULL,
        no_businesses INTEGER NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sic_industries (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        no_businesses INTEGER NOT NULL
        industry_group_id INTEGER,
        major_group_id INTEGER,
        division_id INTEGER NOT NULL,
        UNIQUE(name, industry_group_id, major_group_id, division_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS gics_sectors (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS gics_industries (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        sector_id INTEGER NOT NULL
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
        price REAL NOT NULL,
        volume INTEGER NOT NULL,
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
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        exchange_id INTEGER NOT NULL,
        sector_id INTEGER NOT NULL,
        prices_updated INTEGER NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS commodity_sectors (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
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
        maturity_date INTEGER,
        ts INTEGER,
        price REAL,
        volume INTEGER,
        open_interest INTEGER,
        PRIMARY KEY(commodity_id, maturity_date, ts)
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
        debit INTEGER NOT NULL,
        credit INTEGER NOT NULL
    )
    """
)

# ===========================================================
# ================= Macroeconomic Data ======================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fred_categories(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        super_category_id INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS fred_series (
        id INTEGER PRIMARY KEY,
        abbr TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        category_id INTEGER NOT NULL,
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