from findb import Database
from findb.utils import Conversion, MACROTRENDS_CONVERSION
from findata import CMEReader

def setup_tables(db) -> None:
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
            PRIMARY KEY (country_id, currency_id),
            FOREIGN KEY (country_id) REFERENCES country (country_id),
            FOREIGN KEY (currency_id) REFERENCES currency (currency_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS security_index (
            index_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            ticker TEXT NOT NULL,
            country_id INTEGER NOT NULL,
            FOREIGN KEY (country_id) REFERENCES country (country_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS index_constituent (
            index_id INTEGER,
            security_id INTEGER,
            PRIMARY KEY(index_id, security_id),
            FOREIGN KEY (index_id) REFERENCES security_index (index_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS financial_statement (
            statement_id INTEGER PRIMARY KEY,
            internal_name TEXT UNIQUE NOT NULL,
            label TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.executescript(
        """
        INSERT OR IGNORE INTO financial_statement (internal_name, label) VALUES ("INCOME_STATEMENT", "Income Statement");
        INSERT OR IGNORE INTO financial_statement (internal_name, label) VALUES ("BALANCE_SHEET", "Balance Sheet");
        INSERT OR IGNORE INTO financial_statement (internal_name, label) VALUES ("CASHFLOW_STATEMENT", "Cashflow Statement");
        INSERT OR IGNORE INTO financial_statement (internal_name, label) VALUES ("STATEMENT_CHANGE_EQUITY", "Statement of Changes in Equity");
        INSERT OR IGNORE INTO financial_statement (internal_name, label) VALUES ("FINANCIAL_RATIOS", "Financial Ratios");
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS fundamental_variable (
            variable_id INTEGER PRIMARY KEY,
            internal_name TEXT UNIQUE NOT NULL,
            label TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS entity (
            entity_id INTEGER PRIMARY KEY,
            lei TEXT UNIQUE,
            cik INTEGER UNIQUE,
            name TEXT,
            old_name TEXT,
            logo BLOB,
            type_id INTEGER,
            gics_industry_id INTEGER,
            sic_industry_id INTEGER,
            website TEXT,
            country_id INTEGER,
            city_id INTEGER,
            address1 TEXT,
            address2 TEXT,
            address3 TEXT,
            zip TEXT,
            employees INTEGER,
            fiscal_year_end INTEGER,
            irs_number INTEGER,
            added INTEGER NOT NULL,
            FOREIGN KEY (type_id) REFERENCES sec_issuer_type (type_id),
            FOREIGN KEY (gics_industry_id) REFERENCES industry_classification_gics (industry_id),
            FOREIGN KEY (sic_industry_id) REFERENCES industry_classification_sic (industry_id),
            FOREIGN KEY (country_id) REFERENCES country (country_id),
            FOREIGN KEY (city_id) REFERENCES city (city_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_business_address (
            entity_id INTEGER PRIMARY KEY,
            street1 TEXT,
            street2 TEXT,
            city_id INTEGER,
            state_id INTEGER,
            zip INTEGER,
            phone TEXT,
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id),
            FOREIGN KEY (city_id) REFERENCES sec_city (city_id),
            FOREIGN KEY (state_id) REFERENCES sec_state (state_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mail_address (
            entity_id INTEGER PRIMARY KEY,
            street1 TEXT,
            street2 TEXT,
            city_id INTEGER,
            state_id INTEGER,
            zip INTEGER,
            phone TEXT,
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id),
            FOREIGN KEY (city_id) REFERENCES sec_city (city_id),
            FOREIGN KEY (state_id) REFERENCES sec_state (state_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS security (
            security_id INTEGER PRIMARY KEY,
            entity_id INTEGER NOT NULL,
            ticker TEXT NOT NULL,
            isin TEXT UNIQUE NOT NULL,
            cusip TEXT,
            sec_name TEXT,
            yahoo_name TEXT,
            onvista_name TEXT,
            sec_type_id INTEGER,
            yahoo_type_id INTEGER,
            description TEXT,
            currency_id INTEGER,
            utc_offset INTEGER,
            exchange_id INTEGER,
            added INTEGER NOT NULL,
            profile_updated INTEGER,
            prices_updated INTEGER,
            price_update_failed INTEGER DEFAULT 0,
            UNIQUE (ticker, entity_id),
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id),
            FOREIGN KEY (sec_type_id) REFERENCES sec_asset_type (type_id),
            FOREIGN KEY (yahoo_type_id) REFERENCES yahoo_asset_type (type_id),
            FOREIGN KEY (currency_id) REFERENCES currency (currency_id),
            FOREIGN KEY (exchange_id) REFERENCES exchange (exchange_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS company (
            security_id INTEGER PRIMARY KEY,
            yahoo_data_updated INTEGER,
            marketscreener_data_updated INTEGER,
            stratosphere_data_updated INTEGER,
            tipranks_data_updated INTEGER,
            finviz_data_updated INTEGER,
            macrotrends_data_updated INTEGER,
            FOREIGN KEY (security_id) REFERENCES security (security_id)
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
            UNIQUE (ts, url),
            FOREIGN KEY (source_id) REFERENCES news_source (source_id),
            FOREIGN KEY (type_id) REFERENCES news_type (type_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS security_news_match (
            security_id INTEGER,
            news_id INTEGER,
            PRIMARY KEY (security_id, news_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (news_id) REFERENCES news (news_id)
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
            UNIQUE (ts, url),
            FOREIGN KEY (source_id) REFERENCES news_source (source_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS news_category_match (
            news_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY (news_id, news_id),
            FOREIGN KEY (news_id) REFERENCES general_news (news_id),
            FOREIGN KEY (category_id) REFERENCES news_category (category_id)
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
            PRIMARY KEY (maturity_date, ts)
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
            prices_updated INTEGER,
            FOREIGN KEY (exchange_id) REFERENCES exchange (exchange_id),
            FOREIGN KEY (sector_id) REFERENCES cme_commodity_sector (sector_id)
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
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES ("Agriculture");
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES ("Energy");
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES ("Industrial Metals");
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES ("Livestock");
        INSERT OR IGNORE INTO cme_commodity_sector (name) VALUES ("Precious Metals");
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
            PRIMARY KEY (commodity_id, maturity_date, ts),
            FOREIGN KEY (commodity_id) REFERENCES cme_commodity (commodity_id)
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
            company_id INTEGER PRIMARY KEY,
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
            company_id INTEGER,
            security_id INTEGER,
            ts INTEGER,
            old_rating INTEGER,
            new_rating INTEGER NOT NULL,
            change INTEGER NOT NULL,
            old_price REAL,
            new_price REAL,
            PRIMARY KEY (company_id, security_id, ts),
            FOREIGN KEY (company_id) REFERENCES finviz_analyst_company (company_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
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
            super_category_id INTEGER,
            FOREIGN KEY (super_category_id) REFERENCES fred_category (category_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS fred_series (
            series_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            abbr TEXT NOT NULL,
            description TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            UNIQUE (abbr, name),
            FOREIGN KEY (category_id) REFERENCES fred_category (category_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS fred_data (
            series_id INTEGER,
            ts INTEGER,
            value REAL,
            PRIMARY KEY (series_id, ts),
            FOREIGN KEY (series_id) REFERENCES fred_series (series_id)
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
        CREATE TABLE IF NOT EXISTS french_table (
            table_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS french_series (
            series_id INTEGER PRIMARY KEY,
            dataset_id INTEGER NOT NULL,
            table_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            UNIQUE (dataset_id, table_id, name),
            FOREIGN KEY (dataset_id) REFERENCES french_dataset (dataset_id),
            FOREIGN KEY (table_id) REFERENCES french_table (table_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS french_data (
            series_id INTEGER,
            ts INTEGER,
            value REAL,
            PRIMARY KEY (series_id, ts),
            FOREIGN KEY (series_id) REFERENCES french_series (series_id)
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
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES industry_classification_gics (industry_id)
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
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES industry_classification_sic (industry_id)
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
            standard_id INTEGER UNIQUE NOT NULL,
            UNIQUE (name, statement_id),
            FOREIGN KEY (statement_id) REFERENCES financial_statement (statement_id),
            FOREIGN KEY (standard_id) REFERENCES fundamental_variable (variable_id)
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
            PRIMARY KEY (security_id, variable_id, quarter, year),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (variable_id) REFERENCES macrotrends_fundamental_variable (variable_id)
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
            standard_id INTEGER UNIQUE NOT NULL,
            UNIQUE (name, statement_id),
            FOREIGN KEY (statement_id) REFERENCES financial_statement (statement_id),
            FOREIGN KEY (standard_id) REFERENCES fundamental_variable (variable_id)
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
            PRIMARY KEY (security_id, variable_id, quarter, year),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (variable_id) REFERENCES marketscreener_fundamental_variable (variable_id)
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
            PRIMARY KEY (security_id, segment_id, year),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (segment_id) REFERENCES marketscreener_segment (segment_id)
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
            PRIMARY KEY (security_id, region_id, year),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (region_id) REFERENCES marketscreener_region (region_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marketscreener_industry (
            industry_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            super_id INTEGER,
            FOREIGN KEY (super_id) REFERENCES marketscreener_industry (industry_id)
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
            PRIMARY KEY (security_id, executive_id, type_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (executive_id) REFERENCES marketscreener_executive (executive_id),
            FOREIGN KEY (type_id) REFERENCES marketscreener_executive_type (type_id)
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
            PRIMARY KEY (index_id, ts),
            FOREIGN KEY (index_id) REFERENCES msci_index (index_id)
        )
        """
    )

    # ===========================================================
    # ====================== SEC ================================
    # ===========================================================

    # Filing- and entity-related tables

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
        CREATE TABLE IF NOT EXISTS sec_filing (
            filing_id INTEGER PRIMARY KEY,
            entity_id INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            ts_filed INTEGER NOT NULL,
            filing_url TEXT NOT NULL,
            document_url TEXT NOT NULL,
            parsed INTEGER NOT NULL,
            list_id INTEGER NOT NULL,
            UNIQUE (entity_id, type_id, ts_filed, document_url),
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id),
            FOREIGN KEY (type_id) REFERENCES sec_form_type (type_id),
            FOREIGN KEY (list_id) REFERENCES sec_daily_list (list_id)
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
        CREATE TABLE IF NOT EXISTS sec_state (
            state_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            abbr TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_city (
            city_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            state_id INTEGER NOT NULL,
            FOREIGN KEY (state_id) REFERENCES sec_state (state_id)
        )
        """
    )

    # SEC fundamental data tables

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_fundamental_variable (
            variable_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            statement_id INTEGER NOT NULL,
            UNIQUE (name, statement_id),
            FOREIGN KEY (statement_id) REFERENCES financial_statement (statement_id)
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
            PRIMARY KEY (security_id, variable_id, quarter, year),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (variable_id) REFERENCES sec_fundamental_variable (variable_id),
            FOREIGN KEY (filing_id) REFERENCES sec_filing (filing_id)
        )
        """
    )

    # Form NPORT-P related tables

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_series (
            series_id INTEGER PRIMARY KEY,
            cik TEXT UNIQUE,
            lei TEXT UNIQUE,
            name TEXT,
            entity_id INTEGER NOT NULL,
            added INTEGER NOT NULL,
            discontinued INTEGER,
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_class (
            class_id INTEGER,
            series_id INTEGER NOT NULL,
            cik TEXT PRIMARY KEY,
            FOREIGN KEY (class_id) REFERENCES security (security_id),
            FOREIGN KEY (series_id) REFERENCES sec_mf_series (series_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_class_return (
            class_id INTEGER,
            ts INTEGER,
            return REAL,
            PRIMARY KEY (class_id, ts),
            FOREIGN KEY (class_id) REFERENCES sec_mf_class (class_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_flow (
            series_id INTEGER,
            ts INTEGER,
            sales REAL,
            reinvestments REAL,
            redemptions REAL,
            PRIMARY KEY (series_id, ts),
            FOREIGN KEY (series_id) REFERENCES sec_mf_series (series_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_derivative_gain (
            series_id INTEGER,
            contract_type_id INTEGER,
            derivative_type_id INTEGER,
            ts INTEGER,
            realized_gain REAL,
            unrealized_appreciation REAL,
            PRIMARY KEY (series_id, contract_type_id, derivative_type_id, ts),
            FOREIGN KEY (series_id) REFERENCES sec_mf_series (series_id),
            FOREIGN KEY (contract_type_id) REFERENCES sec_contract_type (type_id),
            FOREIGN KEY (derivative_type_id) REFERENCES sec_derivative_type (type_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_nonderivative_gain (
            series_id INTEGER,
            ts INTEGER,
            realized_gain REAL,
            unrealized_appreciation REAL,
            PRIMARY KEY (series_id, ts),
            FOREIGN KEY (series_id) REFERENCES sec_mf_series (series_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_lending (
            series_id INTEGER,
            entity_id INTEGER,
            ts INTEGER,
            value REAL,
            PRIMARY KEY (series_id, entity_id, ts),
            FOREIGN KEY (series_id) REFERENCES sec_mf_series (series_id),
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_explanatory_note (
            series_id INTEGER,
            ts INTEGER,
            section TEXT,
            note TEXT,
            PRIMARY KEY (series_id, ts),
            FOREIGN KEY (series_id) REFERENCES sec_mf_series (series_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_holding (
            holding_id INTEGER PRIMARY KEY,
            series_id INTEGER NOT NULL,
            ts INTEGER NOT NULL,
            quarter INTEGER,
            year INTEGER,
            position_order INTEGER,
            entity_id INTEGER,
            issuer_name TEXT,
            title TEXT,
            ticker TEXT,
            isin TEXT,
            cusip TEXT,
            security_id INTEGER,
            percentage REAL,
            market_value REAL,
            quantity INTEGER,
            quantity_type_id INTEGER,
            currency_id INTEGER,
            exchange_rate INTEGER,
            payoff_direction TEXT,
            asset_type_id INTEGER,
            restricted_security INTEGER,
            fair_value_level INTEGER,
            is_debt INTEGER,
            is_repo INTEGER,
            is_derivative INTEGER,
            derivative_type_id INTEGER,
            cash_collateral REAL,
            non_cash_collateral REAL,
            loaned REAL,
            UNIQUE (series_id, ts, position_order),
            FOREIGN KEY (series_id) REFERENCES sec_mf_series (series_id),
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (quantity_type_id) REFERENCES sec_quantity_type (type_id),
            FOREIGN KEY (currency_id) REFERENCES currency (currency_id),
            FOREIGN KEY (asset_type_id) REFERENCES sec_asset_type (type_id),
            FOREIGN KEY (derivative_type_id) REFERENCES sec_derivative_type (type_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_debt_information (
            holding_id INTEGER PRIMARY KEY,
            maturity_date INTEGER,
            coupon_rate REAL,
            coupon_type TEXT,
            in_default INTEGER,
            coupon_payments_deferred INTEGER,
            paid_in_kind INTEGER,
            FOREIGN KEY (holding_id) REFERENCES sec_mf_holding (holding_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_convertible_information (
            holding_id INTEGER PRIMARY KEY,
            mandatory_convertible INTEGER,
            contingent_convertible INTEGER,
            issuer_name TEXT,
            title TEXT,
            currency_id INTEGER,
            ticker TEXT,
            isin TEXT,
            cusip TEXT,
            conversion_ratio REAL,
            conversion_currency_id INTEGER,
            delta REAL,
            FOREIGN KEY (holding_id) REFERENCES sec_mf_holding (holding_id),
            FOREIGN KEY (currency_id) REFERENCES currency (currency_id),
            FOREIGN KEY (conversion_currency_id) REFERENCES currency (currency_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_repo_information (
            holding_id INTEGER PRIMARY KEY,
            type TEXT,
            central_counterparty INTEGER,
            entity_id INTEGER,
            counterparty_name TEXT,
            tri_party INTEGER,
            repurchase_rate REAL,
            maturity_date INTEGER,
            FOREIGN KEY (holding_id) REFERENCES sec_mf_holding (holding_id),
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_repo_collateral (
            holding_id INTEGER,
            principal_value REAL,
            principal_currency_id INTEGER,
            collateral_value REAL,
            collateral_currency_id INTEGER,
            type_id INTEGER,
            PRIMARY KEY (holding_id, type_id),
            FOREIGN KEY (holding_id) REFERENCES sec_mf_holding (holding_id),
            FOREIGN KEY (principal_currency_id) REFERENCES currency (currency_id),
            FOREIGN KEY (collateral_currency_id) REFERENCES currency (currency_id),
            FOREIGN KEY (type_id) REFERENCES sec_asset_type (type_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_derivative_counterparty (
            holding_id INTEGER,
            entity_id INTEGER,
            name TEXT,
            PRIMARY KEY (holding_id, name),
            FOREIGN KEY (holding_id) REFERENCES sec_mf_holding (holding_id),
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_currency_forward_information (
            holding_id INTEGER PRIMARY KEY,
            purchased_value REAL,
            purchased_currency_id INTEGER,
            sold_value REAL,
            sold_currency_id INTEGER,
            settlement_date INTEGER,
            unrealized_appreciation REAL,
            FOREIGN KEY (holding_id) REFERENCES sec_mf_holding (holding_id),
            FOREIGN KEY (purchased_currency_id) REFERENCES currency (currency_id),
            FOREIGN KEY (sold_currency_id) REFERENCES currency (currency_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_future_information (
            holding_id INTEGER PRIMARY KEY,
            trade_direction TEXT,
            expiration_date INTEGER,
            notional_amount REAL,
            currency_id INTEGER,
            unrealized_appreciation REAL,
            FOREIGN KEY (holding_id) REFERENCES sec_mf_holding (holding_id),
            FOREIGN KEY (currency_id) REFERENCES currency (currency_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_option_information (
            holding_id INTEGER PRIMARY KEY,
            type TEXT,
            trade_direction TEXT,
            quantity REAL,
            quantity_type_id INTEGER,
            exercise_price REAL,
            exercise_currency_id INTEGER,
            expiration_date INTEGER,
            delta REAL,
            unrealized_appreciation REAL,
            FOREIGN KEY (holding_id) REFERENCES sec_mf_holding (holding_id),
            FOREIGN KEY (quantity_type_id) REFERENCES sec_quantity_type (type_id),
            FOREIGN KEY (exercise_currency_id) REFERENCES currency (currency_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_mf_other_derivative_information (
            holding_id INTEGER PRIMARY KEY,
            termination_date INTEGER,
            notional_amount REAL,
            delta REAL,
            unrealized_appreciation REAL,
            FOREIGN KEY (holding_id) REFERENCES sec_mf_holding (holding_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_asset_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            abbr TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_derivative_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            abbr TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_issuer_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            abbr TEXT UNIQUE,
            UNIQUE (name, abbr)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_quantity_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            abbr TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_contract_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_derivative_contract_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
    )

    # Form 13F related tables

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_hf_holding (
            entity_id INTEGER,
            security_id INTEGER,
            ts INTEGER NOT NULL,
            quarter INTEGER,
            year INTEGER,
            cusip TEXT,
            percentage REAL,
            no_shares INTEGER,
            market_value REAL,
            option_id INTEGER,
            filing_id INTEGER,
            PRIMARY KEY (entity_id, security_id, quarter, year, option_id),
            FOREIGN KEY (entity_id) REFERENCES entity (entity_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (option_id) REFERENCES sec_option (option_id),
            FOREIGN KEY (filing_id) REFERENCES sec_filing (filing_id)
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

    # Form 3/4/5 related tables

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_shareholder_trade (
            filer_entity_id INTEGER NOT NULL,
            subject_entity_id INTEGER NOT NULL,
            security_id INTEGER NOT NULL,
            ts INTEGER NOT NULL,
            shares INTEGER NOT NULL,
            percentage REAL NOT NULL,
            filing_id INTEGER PRIMARY KEY,
            FOREIGN KEY (filer_entity_id) REFERENCES entity (entity_id),
            FOREIGN KEY (subject_entity_id) REFERENCES entity (entity_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (filing_id) REFERENCES sec_filing (filing_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sec_transaction_type (
            type_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            abbr TEXT UNIQUE
        )
        """
    )

    # ===========================================================
    # ===================== Stratosphere ========================
    # ===========================================================

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_fundamental_variable (
            variable_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            statement_id INTEGER NOT NULL,
            UNIQUE (name, statement_id),
            FOREIGN KEY (statement_id) REFERENCES financial_statement (statement_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_fundamental_data (
            security_id INTEGER NOT NULL,
            variable_id INTEGER NOT NULL,
            ts INTEGER NOT NULL,
            quarterly INTEGER NOT NULL,
            value REAL,
            PRIMARY KEY (security_id, variable_id, ts, quarterly),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (variable_id) REFERENCES stratosphere_fundamental_variable (variable_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_segment_variable (
            variable_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_segment_data (
            security_id INTEGER NOT NULL,
            variable_id INTEGER NOT NULL,
            ts INTEGER NOT NULL,
            quarterly INTEGER NOT NULL,
            value REAL,
            PRIMARY KEY (security_id, variable_id, ts, quarterly),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (variable_id) REFERENCES stratosphere_segment_variable (variable_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_kpi_variable (
            variable_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_kpi_data (
            security_id INTEGER NOT NULL,
            variable_id INTEGER NOT NULL,
            ts INTEGER NOT NULL,
            quarterly INTEGER NOT NULL,
            value REAL,
            PRIMARY KEY (security_id, variable_id, ts, quarterly),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (variable_id) REFERENCES stratosphere_kpi_variable (variable_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_analyst (
            analyst_id INTEGER PRIMARY KEY,
            name TEXT,
            company_id INTEGER NOT NULL,
            UNIQUE (name, company_id),
            FOREIGN KEY (company_id) REFERENCES stratosphere_analyst_company (company_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_analyst_company (
            company_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_analyst_price_target (
            security_id INTEGER NOT NULL,
            analyst_id INTEGER NOT NULL,
            price_target REAL,
            price_when_rated REAL,
            ts INTEGER,
            title TEXT,
            url TEXT,
            source_id INTEGER NOT NULL,
            PRIMARY KEY (security_id, analyst_id, ts),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (analyst_id) REFERENCES stratosphere_analyst (analyst_id),
            FOREIGN KEY (source_id) REFERENCES news_source (source_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stratosphere_analyst_estimate (
            security_id INTEGER NOT NULL,
            variable_id INTEGER NOT NULL,
            ts INTEGER NOT NULL,
            quarterly INTEGER NOT NULL,
            high REAL,
            average REAL,
            low REAL,
            number_analysts INTEGER,
            PRIMARY KEY (security_id, variable_id, ts, quarterly),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (variable_id) REFERENCES stratosphere_fundamental_variable (variable_id)
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
            PRIMARY KEY (security_id, week),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
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
            PRIMARY KEY (security_id, week),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
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
            sell_percentage REAL,
            FOREIGN KEY (company_id) REFERENCES tipranks_analyst_company (company_id),
            FOREIGN KEY (sector_id) REFERENCES tipranks_sector (sector_id),
            FOREIGN KEY (country_id) REFERENCES tipranks_country (country_id)
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
            PRIMARY KEY (analyst_id, security_id, ts),
            FOREIGN KEY (analyst_id) REFERENCES tipranks_analyst (analyst_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (rating_id) REFERENCES tipranks_rating (rating_id),
            FOREIGN KEY (change_id) REFERENCES tipranks_rating (change_id)
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
            PRIMARY KEY (analyst_id, security_id),
            FOREIGN KEY (analyst_id) REFERENCES tipranks_analyst (analyst_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
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
            PRIMARY KEY (institutional_id, security_id, ts),
            FOREIGN KEY (institutional_id) REFERENCES tipranks_institutional (institutional_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
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
            UNIQUE (name, country_id),
            FOREIGN KEY (country_id) REFERENCES country (country_id)
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
            UNIQUE (name, country_id, yahoo_suffix),
            FOREIGN KEY (country_id) REFERENCES country (country_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_executive (
            executive_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            born INTEGER,
            UNIQUE (name, born)
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
            PRIMARY KEY (security_id, executive_id, position_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (executive_id) REFERENCES yahoo_executive (executive_id),
            FOREIGN KEY (position_id) REFERENCES yahoo_executive_position (position_id)
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
            PRIMARY KEY (security_id, ts),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_currency_price (
            numerator_id INTEGER,
            denominator_id INTEGER,
            ts INTEGER,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            adj_close REAL,
            simple_return REAL,
            log_return REAL,
            PRIMARY KEY (numerator_id, denominator_id, ts),
            FOREIGN KEY (numerator_id) REFERENCES currency (currency_id),
            FOREIGN KEY (denominator_id) REFERENCES currency (currency_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_asset_type (
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
            PRIMARY KEY (company_id, security_id, ts),
            FOREIGN KEY (company_id) REFERENCES yahoo_analyst_company (company_id),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
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
            PRIMARY KEY (security_id, month),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_fundamental_variable (
            variable_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            statement_id INTEGER NOT NULL,
            UNIQUE (name, statement_id),
            FOREIGN KEY (statement_id) REFERENCES financial_statement (statement_id)
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
            PRIMARY KEY (security_id, variable_id, quarter, year),
            FOREIGN KEY (security_id) REFERENCES security (security_id),
            FOREIGN KEY (variable_id) REFERENCES yahoo_fundamental_variable (variable_id)
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
            sector_id INTEGER NOT NULL,
            FOREIGN KEY (sector_id) REFERENCES yahoo_gics_sector (sector_id)
        )
        """
    )

    db.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS yahoo_earnings_history (
            security_id INTEGER,
            ts INTEGER NOT NULL,
            estimate REAL,
            actual REAL,
            abs_diff REAL,
            rel_diff REAL,
            PRIMARY KEY (security_id, ts),
            FOREIGN KEY (security_id) REFERENCES security (security_id)
        )
        """
    )


def insert_cme_commodities(db) -> None:
    for name, properties in CMEReader.commodities.items():
        sector_id = db.cur.execute(f"SELECT sector_id FROM cme_commodity_sector WHERE name = ?", (properties["sector_name"],)).fetchone()[0]
        exchange_id = db.cur.execute(f"SELECT exchange_id FROM yahoo_exchange WHERE yahoo_suffix = '.CME'").fetchone()[0]
        db.cur.execute(
            f"INSERT OR IGNORE INTO cme_commodity (name, exchange_id, sector_id) VALUES (?, ?, ?)",
            (name, exchange_id, sector_id)
        )


def insert_standardized_variables(db) -> None:
    for var in Conversion:
        db.cur.execute("INSERT OR IGNORE INTO fundamental_variable (internal_name, label) VALUES(?, ?)", (var.name, var.value))


def insert_macrotrends_variables(db) -> None:
    for statement in MACROTRENDS_CONVERSION.keys():
        statement_id = db.cur.execute("SELECT statement_id FROM financial_statement WHERE internal_name = ?", (statement,)).fetchone()[0]
        for variable, enum in MACROTRENDS_CONVERSION[statement].items():
            enum_id = db.cur.execute("SELECT variable_id FROM fundamental_variable WHERE internal_name = ?", (enum.name,)).fetchone()[0]
            db.cur.execute("INSERT OR IGNORE INTO macrotrends_fundamental_variable (name, statement_id, standard_id) VALUES (?, ?, ?)", (variable, statement_id, enum_id))

if __name__ == "__main__":
    from findb.setup_db.countries_currencies_exchanges import insert_countries_currencies_exchanges
    from findb.setup_db.industry_classifications import insert_gics_classifcation, insert_sic_classification
    with Database() as db:
        print("Setup Tables")
        setup_tables(db)

        print("Inserting Countries")
        insert_countries_currencies_exchanges(db)

        print("Inserting CME Commodities")
        insert_cme_commodities(db)

        print("Inserting Standardized Fundamental Variables")
        insert_standardized_variables(db)

        print("Inserting Macrotrends Fundamental Variables")
        insert_macrotrends_variables(db)

        print("Inserting GICS Classification")
        insert_gics_classifcation(db)

        print("Inserting SIC Classification")
        insert_sic_classification(db)