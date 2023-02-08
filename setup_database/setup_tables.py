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
    CREATE TABLE IF NOT EXISTS securities (
        id INTEGER PRIMARY KEY,
        cik TEXT NOT NULL,
        ticker TEXT NOT NULL,
        isin TEXT,
        yahoo_name TEXT,
        sec_name TEXT,
        description TEXT,
        logo BLOB,
        type_id INTEGER,
        currency_id INTEGER,
        utc_offset INTEGER,
        exchange_id INTEGER,
        added INTEGER NOT NULL,
        discontinued INTEGER,
        old_name TEXT,
        profile_updated INTEGER,
        prices_updated INTEGER,
        is_sec_company INTEGER,
        is_sec_mutualfund INTEGER,
        UNIQUE(cik, ticker)
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
        macrotrends_fundamentals_updated INTEGER,
        tipranks_data_updated INTEGER
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
        description TEXT,
        url TEXT NOT NULL,
        UNIQUE(ts, url)
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
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS general_news (
        id INTEGER PRIMARY KEY,
        source_id INTEGER NOT NULL,
        ts INTEGER NOT NULL,
        header TEXT NOT NULL,
        description TEXT,
        url TEXT NOT NULL,
        UNIQUE(ts, url)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS news_category_match (
        news_id INTEGER,
        category_id INTEGER,
        PRIMARY KEY(news_id, news_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS news_categories (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

# ===========================================================
# ======================== CBOE =============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cboe_vix_prices (
        maturity_date INTEGER,
        ts INTEGER,
        price REAL NOT NULL,
        volume INTEGER NOT NULL,
        PRIMARY KEY(maturity_date, ts)
    )
    """
)

# ===========================================================
# ========= Chicago Mercantile Exchange (CME) ===============
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cme_commodities (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        exchange_id INTEGER NOT NULL,
        sector_id INTEGER NOT NULL,
        prices_updated INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cme_commodity_sectors (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.executescript(
    """
    INSERT OR IGNORE INTO cme_commodity_sectors (name) VALUES("Agriculture");
    INSERT OR IGNORE INTO cme_commodity_sectors (name) VALUES("Energy");
    INSERT OR IGNORE INTO cme_commodity_sectors (name) VALUES("Industrial Metals");
    INSERT OR IGNORE INTO cme_commodity_sectors (name) VALUES("Livestock");
    INSERT OR IGNORE INTO cme_commodity_sectors (name) VALUES("Precious Metals");
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cme_commodity_prices (
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
# ======================== Finra ============================
# ===========================================================


cur.execute(
    """
    CREATE TABLE IF NOT EXISTS finra_margin_debt (
        ts INTEGER PRIMARY KEY,
        debit INTEGER NOT NULL,
        credit INTEGER NOT NULL
    )
    """
)

# ===========================================================
# ======================== Finviz ===========================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS finviz_analyst_companies (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS finviz_ratings (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS finviz_analyst_recommendations (
        analyst_company_id INTEGER,
        security_id INTEGER,
        ts INTEGER,
        old_rating INTEGER,
        new_rating INTEGER NOT NULL,
        change INTEGER NOT NULL,
        old_price REAL,
        new_price REAL,
        PRIMARY KEY(analyst_company_id, security_id, ts)
    )
    """
)

# ===========================================================
# ========================= FRED ============================
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

# ===========================================================
# ======================== French ===========================
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
# =================== GICS & SIC ============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS industry_classification_gics (
        code INTEGER UNIQUE,
        name TEXT NOT NULL,
        is_sector INTEGER,
        is_industry_group INTEGER,
        is_industry INTEGER,
        is_sub_industry INTEGER,
        parent_id INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS industry_classification_sic (
        code INTEGER UNIQUE,
        name TEXT NOT NULL,
        no_businesses INTEGER NOT NULL,
        is_division INTEGER,
        is_major_group INTEGER,
        is_industry_group INTEGER,
        is_industry INTEGER,
        description TEXT,
        parent_id INTEGER
    )
    """
)

# ===========================================================
# ===================== Macrotrends =========================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS macrotrends_fundamental_variables (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        statement_id INTEGER NOT NULL,
        UNIQUE(name, statement_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS macrotrends_fundamental_data (
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
# ========================= MSCI ============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS msci_indices (
        id INTEGER PRIMARY KEY,
        code INTEGER UNIQUE NOT NULL,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS msci_index_prices (
        index_id INTEGER,
        ts INTEGER,
        price REAL,
        simple_return REAL,
        log_return REAL,
        PRIMARY KEY(index_id, ts)
    )
    """
)

# ===========================================================
# ====================== SEC ================================
# ===========================================================

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
    CREATE TABLE IF NOT EXISTS sec_form_types (
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

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_fundamental_variables (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        statement_id INTEGER NOT NULL,
        UNIQUE(name, statement_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_fundamental_data (
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
    CREATE TABLE IF NOT EXISTS sec_mutualfund_entities (
        id INTEGER PRIMARY KEY,
        cik INTEGER UNIQUE,
        name TEXT UNIQUE,
        added INTEGER,
        discontinued INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_mutualfund_series (
        id INTEGER PRIMARY KEY,
        cik TEXT UNIQUE,
        name TEXT UNIQUE,
        entity_id INTEGER,
        added INTEGER,
        discontinued INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_mutualfund_classes (
        security_id INTEGER PRIMARY KEY,
        series_id INTEGER
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_investment_managers (
        id INTEGER PRIMARY KEY,
        cik INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_investment_manager_holdings (
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
    CREATE TABLE IF NOT EXISTS sec_options (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_cusips (
        id INTEGER PRIMARY KEY,
        cusip TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sec_acquisitions (
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
# ===================== Tipranks ============================
# ===========================================================


cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_recommendation_trend (
        security_id INTEGER,
        week INTEGER,
        number INTEGER,
        average REAL,
        buy INTEGER,
        hold INTEGER,
        sell INTEGER,
        average_price_target REAL,
        PRIMARY KEY(security_id, week)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_news_sentiment (
        security_id INTEGER,
        week INTEGER,
        number INTEGER,
        average REAL,
        buy INTEGER,
        hold INTEGER,
        sell INTEGER,
        PRIMARY KEY(security_id, week)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_analysts (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        image BLOB,
        analyst_company_id INTEGER,
        sector_id INTEGER,
        country_id INTEGER,
        rank INTEGER,
        stars REAL,
        successful_recommendations INTEGER,
        total_recommendations INTEGER,
        success_rate REAL,
        average_rating_return REAL,
        buy_percentage REAL,
        hold_percentage REAL,
        sell_percentage REAL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_analyst_companies (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_sectors (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_countries (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_ratings (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_analyst_recommendations (
        analyst_id INTEGER,
        security_id INTEGER,
        ts INTEGER,
        rating_id INTEGER,
        change_id INTEGER,
        price_target REAL,
        title TEXT,
        url TEXT,
        PRIMARY KEY(analyst_id, security_id, ts)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_analyst_stock_summary (
        analyst_id INTEGER,
        security_id INTEGER,
        successful_recommendations INTEGER,
        total_recommendations INTEGER,
        success_rate REAL,
        average_rating_return REAL,
        PRIMARY KEY(analyst_id, security_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT exists tipranks_institutionals (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        manager TEXT,
        image BLOB,
        rank INTEGER,
        stars REAL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tipranks_institutional_holdings (
        institutional_id INTEGER,
        security_id INTEGER,
        ts INTEGER,
        value INTEGER,
        change REAL,
        percentage_of_portfolio REAL,
        PRIMARY KEY(institutional_id, security_id, ts)
    )
    """
)

# ===========================================================
# ======================== Yahoo ============================
# ===========================================================

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_cities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country_id INTEGER NOT NULL,
        UNIQUE(name, country_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_exchanges (
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
    CREATE TABLE IF NOT EXISTS yahoo_executives (
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
    CREATE TABLE IF NOT EXISTS yahoo_executive_positions (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_company_executive_match (
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
    CREATE TABLE IF NOT EXISTS yahoo_security_prices (
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
    CREATE TABLE IF NOT EXISTS yahoo_security_types (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_analyst_companies (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_ratings (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_analyst_recommendations (
        analyst_company_id INTEGER,
        security_id INTEGER,
        ts INTEGER,
        old INTEGER,
        new INTEGER NOT NULL,
        change INTEGER NOT NULL,
        PRIMARY KEY(analyst_company_id, security_id, ts)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_recommendation_trend (
        security_id INTEGER,
        month INTEGER,
        number INTEGER,
        average REAL,
        strong_buy INTEGER,
        buy INTEGER,
        hold INTEGER,
        sell INTEGER,
        strong_sell INTEGER,
        PRIMARY KEY(security_id, month)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_fundamental_variables (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        statement_id INTEGER NOT NULL,
        UNIQUE(name, statement_id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_fundamental_data (
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
    CREATE TABLE IF NOT EXISTS yahoo_gics_sectors (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS yahoo_gics_industries (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        sector_id INTEGER NOT NULL
    )
    """
)

con.commit()
con.close()