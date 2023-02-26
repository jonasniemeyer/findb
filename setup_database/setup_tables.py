from finance_database import Database

with Database() as db:
    # ===========================================================
    # ===================== General =============================
    # ===========================================================

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS country (
            country_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            flag_small BLOB,
            flag_medium BLOB,
            flag_large BLOB
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS currency (
            currency_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            abbr TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS country_currency_match (
            country_id INTEGER,
            currency_id INTEGER,
            PRIMARY KEY(country_id, currency_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS index (
            index_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            ticker TEXT NOT NULL,
            country_id INTEGER NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS index_constituent (
            index_id INTEGER,
            security_id INTEGER,
            PRIMARY KEY(index_id, security_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS financial_statement_type (
            statement_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.executescript(
        """
        INSERT OR IGNORE INTO financial_statement_type (name) VALUES ("income_statement");
        INSERT OR IGNORE INTO financial_statement_type (name) VALUES ("balance_sheet");
        INSERT OR IGNORE INTO financial_statement_type (name) VALUES ("cashflow_statement");
        INSERT OR IGNORE INTO financial_statement_type (name) VALUES ("statement_of_changes_in_equity");
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS security (
            security_id INTEGER PRIMARY KEY,
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS company (
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
            yahoo_data_updated INTEGER,
            macrotrends_data_updated INTEGER,
            tipranks_data_updated INTEGER,
            stratosphere_data_updated INTEGER,
            marketscreener_data_updated INTEGER
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS security_news (
            news_id INTEGER PRIMARY KEY,
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS security_news_match (
            security_id INTEGER,
            news_id INTEGER,
            PRIMARY KEY(security_id, news_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS news_source (
            source_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS news_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS general_news (
            news_id INTEGER PRIMARY KEY,
            source_id INTEGER NOT NULL,
            ts INTEGER NOT NULL,
            header TEXT NOT NULL,
            description TEXT,
            url TEXT NOT NULL,
            UNIQUE(ts, url)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS news_category_match (
            news_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY(news_id, news_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS news_category (
            category_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    # ===========================================================
    # ======================== CBOE =============================
    # ===========================================================

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cboe_vix_data (
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cme_commodity (
            commodity_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            exchange_id INTEGER NOT NULL,
            sector_id INTEGER NOT NULL,
            prices_updated INTEGER
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cme_commodity_sector (
            sector_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.executescript(
        """
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES("Agriculture");
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES("Energy");
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES("Industrial Metals");
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES("Livestock");
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES("Precious Metals");
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cme_commodity_data (
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


    db.cur.execute(
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS finviz_analyst_company (
            analyst_company_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS finviz_rating (
            rating_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS finviz_analyst_recommendation (
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS fred_category (
            category_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            super_category_id INTEGER
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS fred_series (
            series_id INTEGER PRIMARY KEY,
            abbr TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            UNIQUE(abbr, name)
        )
        """
    )

    db.cur.execute(
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS french_dataset (
            dataset_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            updated INTEGER NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS french_category (
            category_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS french_series (
            series_id INTEGER PRIMARY KEY,
            dataset_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            UNIQUE(dataset_id, category_id, name)
        )
        """
    )

    db.cur.execute(
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
    # ======= Industry Classification (GICS & SIC) ==============
    # ===========================================================

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS industry_classification_gics (
            industry_id INTEGER PRIMARY KEY,
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS industry_classification_sic (
            industry_id INTEGER PRIMARY KEY,
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS macrotrends_fundamental_variable (
            variable_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            statement_id INTEGER NOT NULL,
            UNIQUE(name, statement_id)
        )
        """
    )

    db.cur.execute(
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
    # =================== Marketscreener ========================
    # ===========================================================

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_fundamental_variable (
            variable_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            statement_id INTEGER NOT NULL,
            UNIQUE(name, statement_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_fundamental_data (
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_segment (
            segment_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_segment_data (
            security_id INTEGER NOT NULL,
            segment_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            value REAL,
            percentage REAL,
            PRIMARY KEY(security_id, segment_id, year)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_region (
            region_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_region_data (
            security_id INTEGER NOT NULL,
            region_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            value REAL,
            percentage REAL,
            PRIMARY KEY(security_id, region_id, year)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_industry (
            industry_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            super_id INTEGER
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_executive (
            executive_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            age INTEGER
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_company_executive_match (
            security_id INTEGER NOT NULL,
            executive_id INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            joined INTEGER,
            added INTEGER NOT NULL,
            discontinued INTEGER,
            PRIMARY KEY(security_id, executive_id, type_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_executive_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.executescript(
        """
        INSERT OR IGNORE INTO marketscreener_executive_type (name) VALUES ("manager");
        INSERT OR IGNORE INTO marketscreener_executive_type (name) VALUES ("board member");
        """
    )



    # ===========================================================
    # ========================= MSCI ============================
    # ===========================================================

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS msci_index (
            index_id INTEGER PRIMARY KEY,
            code INTEGER UNIQUE NOT NULL,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS msci_index_data (
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_daily_list (
            list_id INTEGER PRIMARY KEY,
            ts INTEGER UNIQUE NOT NULL,
            url TEXT UNIQUE NOT NULL,
            parsed INTEGER NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_form_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_filing (
            filing_id INTEGER PRIMARY KEY,
            cik INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            ts_filed INTEGER NOT NULL,
            filing_url TEXT NOT NULL,
            document_url TEXT NOT NULL,
            parsed INTEGER NOT NULL,
            list_id INTEGER NOT NULL,
            UNIQUE(cik, type_id, ts_filed, document_url)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_fundamental_variable (
            variable_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            statement_id INTEGER NOT NULL,
            UNIQUE(name, statement_id)
        )
        """
    )

    db.cur.execute(
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mutualfund_entity (
            entity_id INTEGER PRIMARY KEY,
            cik INTEGER UNIQUE,
            name TEXT UNIQUE,
            added INTEGER,
            discontinued INTEGER
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mutualfund_series (
            series_id INTEGER PRIMARY KEY,
            cik TEXT UNIQUE,
            name TEXT UNIQUE,
            entity_id INTEGER,
            added INTEGER,
            discontinued INTEGER
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mutualfund_class (
            security_id INTEGER PRIMARY KEY,
            series_id INTEGER
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_investment_manager (
            manager_id INTEGER PRIMARY KEY,
            cik INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_investment_manager_holding (
            manager_id INTEGER,
            quarter INTEGER,
            year INTEGER,
            ts INTEGER NOT NULL,
            cusip_id INTEGER,
            percentage REAL,
            no_shares INTEGER,
            market_value REAL,
            option_id INTEGER,
            filing_id INTEGER,
            PRIMARY KEY(manager_id, cusip_id, quarter, year, option_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_option (
            option_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_cusip (
            cusip_id INTEGER PRIMARY KEY,
            cusip TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_acquisition (
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


    db.cur.execute(
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

    db.cur.execute(
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tipranks_analyst (
            analyst_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            image BLOB,
            company_id INTEGER,
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tipranks_analyst_company (
            company_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tipranks_sector (
            sector_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tipranks_country (
            country_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tipranks_rating (
            rating_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tipranks_analyst_recommendation (
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

    db.cur.execute(
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT exists tipranks_institutional (
            institutional_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            manager TEXT,
            image BLOB,
            rank INTEGER,
            stars REAL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tipranks_institutional_holding (
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_city (
            city_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country_id INTEGER NOT NULL,
            UNIQUE(name, country_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_exchange (
            exchange_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            yahoo_suffix TEXT NOT NULL,
            country_id INTEGER NOT NULL,
            UNIQUE(name, country_id, yahoo_suffix)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_executive (
            executive_d INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            born INTEGER,
            UNIQUE(name, born)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_executive_position (
            position_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_company_executive_match (
            security_id INTEGER NOT NULL,
            executive_id INTEGER NOT NULL,
            position_id INTEGER NOT NULL,
            salary REAL,
            added INTEGER NOT NULL,
            discontinued INTEGER,
            PRIMARY KEY(security_id, executive_id, position_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_security_price (
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_security_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_analyst_company (
            company_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_rating (
            rating_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_analyst_recommendation (
            company_id INTEGER,
            security_id INTEGER,
            ts INTEGER,
            old INTEGER,
            new INTEGER NOT NULL,
            change INTEGER NOT NULL,
            PRIMARY KEY(company_id, security_id, ts)
        )
        """
    )

    db.cur.execute(
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_fundamental_variable (
            variable_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            statement_id INTEGER NOT NULL,
            UNIQUE(name, statement_id)
        )
        """
    )

    db.cur.execute(
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

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_gics_sector (
            sector_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_gics_industry (
            industry_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            sector_id INTEGER NOT NULL
        )
        """
    )