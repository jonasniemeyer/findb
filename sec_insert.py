import pandas as pd
import time
from finance_database import Database
from finance_data import (
    YahooReader,
    TickerError,
    FilingNPORT
)

class NPORTInsert:
    def __init__(self, filing: FilingNPORT, db: Database) -> None:
        self.filing = filing
        self.db = db
        self.ts_today = int(pd.to_datetime(pd.to_datetime("today").date()).timestamp())
        self.ts_period = int(pd.to_datetime(self.filing.date_of_period).timestamp())

        # insert series information and get series id
        series = self.filing.general_information["series"]
        self.db.cur.execute("INSERT OR IGNORE INTO sec_mf_series (cik, added) VALUES (?, ?)", (series["cik"], self.ts_today))
        self.db.cur.execute(
            "UPDATE sec_mf_series SET lei = ?, name = ? WHERE cik = ?",
            (series["lei"], series["name"], series["cik"])
        )
        self.series_id = self.db.cur.execute("SELECT series_id FROM sec_mf_series WHERE cik = ?", (series["cik"],)).fetchone()[0]

    def insert_filing_data(self) -> None:
        self.insert_filer_information()
        self.insert_class_information()
        self.insert_fund_information()
        self.insert_portfolio_data()
        self.insert_explanatory_notes()

    def insert_fund_information(self) -> None:
        self.insert_return_information()
        self.insert_flow_information()
        self.insert_lending_information()

    def insert_filer_information(self) -> None:
        cik = self.filing.filer["cik"]
        business = self.filing.filer["business_address"]
        mail = self.filing.filer["mail_address"]
        lei = self.filing.general_information["filer_lei"]
        
        if self.filing.filer["former_names"] is None:
            former_name = None
        else:
            former_name = self.filing.filer["former_names"][0]["name"]

        if self.filing.filer["fiscal_year_end"] is None:
            fiscal_year_end = None
        else:
            fiscal_year_end = int(str(self.filing.filer["fiscal_year_end"]["month"]) + str(self.filing.filer["fiscal_year_end"]["day"]))

        self.db.cur.execute("INSERT OR IGNORE INTO entity (cik) VALUES (?)", (cik,))
        if self.filing.filer["sic"]["code"] is None:
            sic_industry_id = None
        else:
            sic_industry_id = self.db.cur.execute("SELECT industry_id FROM industry_classification_sic WHERE code = ?", (self.filing.filer["sic"]["code"],)).fetchone()[0]
        self.db.cur.execute(
            """
            UPDATE entity SET lei = ?, name = ?, old_name = ?, sic_industry_id = ?, fiscal_year_end = ?, irs_number = ?
            WHERE cik = ?
            """,
            (lei, self.filing.filer["name"], former_name, sic_industry_id, fiscal_year_end, self.filing.filer["irs_number"], self.filing.filer["cik"])
        )

        entity_id = self.db.cur.execute("SELECT entity_id FROM entity WHERE cik = ?", (cik,)).fetchone()[0]

        self.db.cur.execute("INSERT OR IGNORE INTO sec_state (abbr) VALUES (?)", (business["state"],))
        state_id = self.db.cur.execute("SELECT state_id FROM sec_state WHERE abbr = ?", (business["state"],)).fetchone()[0]

        self.db.cur.execute("INSERT OR IGNORE INTO sec_city (name, state_id) VALUES (?, ?)", (business["city"], state_id))
        city_id = self.db.cur.execute("SELECT city_id FROM sec_city WHERE name = ?", (business["city"],)).fetchone()[0]

        self.db.cur.execute("INSERT OR IGNORE INTO sec_business_address (entity_id) VALUES (?)", (entity_id,))
        self.db.cur.execute(
            """
            UPDATE sec_business_address SET street1 = ?, street2 = ?, city_id = ?, state_id = ?, zip = ?, phone = ?
            WHERE entity_id = ?
            """,
            (business["street1"], business["street2"], city_id, state_id, business["zip"], business["phone"], entity_id)
        )

        self.db.cur.execute("INSERT OR IGNORE INTO sec_state (abbr) VALUES (?)", (mail["state"],))
        state_id = self.db.cur.execute("SELECT state_id FROM sec_state WHERE abbr = ?", (mail["state"],)).fetchone()[0]

        self.db.cur.execute("INSERT OR IGNORE INTO sec_city (name, state_id) VALUES (?, ?)", (mail["city"], state_id))
        city_id = self.db.cur.execute("SELECT city_id FROM sec_city WHERE name = ?", (mail["city"],)).fetchone()[0]

        self.db.cur.execute("INSERT OR IGNORE INTO sec_mail_address (entity_id) VALUES (?)", (entity_id,))
        self.db.cur.execute(
            """
            UPDATE sec_mail_address SET street1 = ?, street2 = ?, city_id = ?, state_id = ?, zip = ?
            WHERE entity_id = ?
            """,
            (mail["street1"], mail["street2"], city_id, state_id, mail["zip"], entity_id)
        )
    
    def insert_portfolio_data(self) -> None:
        quarter = 1
        year = 1900
        security_id = None

        portfolio = self.filing.portfolio(sorted_by="percentage")
        length = len(portfolio)
        trail = len(str(length))

        for index, item in enumerate(portfolio):
            issuer = item["issuer"]
            if issuer["lei"] is None:
                entity_id = None
            else:
                self.db.cur.execute("INSERT OR IGNORE INTO entity (lei, name, added) VALUES (?, ?, ?)", (issuer["lei"], issuer["name"], self.ts_today))
                entity_id = self.db.cur.execute("SELECT entity_id FROM entity WHERE lei = ?", (issuer["lei"],)).fetchone()[0]

            identifier = item["identifier"]
            lending = item["securities_lending"]
            amount = item["amount"]
            currency_id = self.db.cur.execute("SELECT currency_id FROM currency WHERE abbr = ?", (amount["currency"]["abbr"],)).fetchone()[0]

            self.db.cur.execute("INSERT OR IGNORE INTO sec_asset_type (abbr, name) VALUES (?, ?)", (item["asset_type"]["abbr"], item["asset_type"]["name"]))
            asset_type_id = self.db.cur.execute("SELECT type_id FROM sec_asset_type WHERE abbr = ?", (item["asset_type"]["abbr"],)).fetchone()[0]

            self.db.cur.execute("INSERT OR IGNORE INTO sec_quantity_type (abbr, name) VALUES (?, ?)", (amount["quantity_type"]["abbr"], amount["quantity_type"]["name"]))
            quantity_type_id = self.db.cur.execute("SELECT type_id FROM sec_quantity_type WHERE abbr = ?", (amount["quantity_type"]["abbr"],)).fetchone()[0]

            is_debt = True if item["debt_information"] is not None else False
            is_repo = True if item["repurchase_information"] is not None else False
            is_derivative = True if item["derivative_information"] is not None else False

            self.db.cur.execute(
                """
                INSERT OR IGNORE INTO sec_mf_holding (
                    series_id,
                    ts,
                    quarter,
                    year,
                    holding_id,
                    entity_id,
                    title,
                    ticker,
                    isin,
                    cusip,
                    security_id,
                    percentage,
                    market_value,
                    quantity,
                    quantity_type_id,
                    currency_id,
                    exchange_rate,
                    payoff_direction,
                    asset_type_id,
                    restricted_security,
                    fair_value_level,
                    is_debt,
                    is_repo,
                    is_derivative,
                    cash_collateral,
                    non_cash_collateral,
                    loaned
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.series_id,
                    self.ts_period,
                    quarter,
                    year,
                    index,
                    entity_id,
                    item["title"],
                    identifier.get("ticker", None),
                    identifier.get("isin", None),
                    identifier.get("cusip", None),
                    security_id,
                    amount["percentage"],
                    amount["market_value"],
                    amount["quantity"],
                    quantity_type_id,
                    currency_id,
                    amount["currency"]["exchange_rate"],
                    item["payoff_direction"],
                    asset_type_id,
                    item["restricted_security"],
                    item["us_gaap_fair_value_hierarchy"],
                    is_debt,
                    is_repo,
                    is_derivative,
                    lending["cash_collateral"],
                    lending["non_cash_collateral"],
                    lending["loaned"]
                )
            )
    
    def insert_explanatory_notes(self) -> None:
        for section, note in self.filing.explanatory_notes.items():
            self.db.cur.execute(
                """
                INSERT OR IGNORE INTO sec_mf_explanatory_note
                (series_id, ts, section, note)
                VALUES (?, ?, ?, ?)
                """,
                (self.series_id, self.ts_period, section, note)
            )
    
    def insert_class_information(self) -> None:
        classes = self.filing.general_information["classes"]
        for class_ in classes:
            self.db.cur.execute("INSERT OR IGNORE INTO security (ticker, added) VALUES (?, ?)", (class_["ticker"], self.ts_today))
            self.db.cur.execute(
                "UPDATE security SET sec_name = ? WHERE ticker = ?",
                (class_["name"], class_["ticker"])
            )
            security_id = self.db.cur.execute("SELECT security_id FROM security WHERE ticker = ?", (class_["ticker"],)).fetchone()[0]
            self.db.cur.execute("INSERT OR IGNORE INTO sec_mf_class (security_id, series_id, cik) VALUES (?, ?, ?)", (security_id, self.series_id, class_["cik"],))

    def insert_flow_information(self) -> None:
        for date, data in self.filing.flow_information.items():
            ts = int(pd.to_datetime(date).timestamp())
            self.db.cur.execute(
                """
                INSERT OR IGNORE INTO sec_mf_flow
                (series_id, ts, sales, reinvestments, redemptions)
                VALUES (?, ?, ?, ?, ?)
                """,
                (self.series_id, ts, data["sales"], data["reinvestments"], data["redemptions"])
            )

    def insert_lending_information(self) -> None:
        if self.filing.securities_lending["borrowers"] is not None:
            for dct in self.filing.securities_lending["borrowers"]:
                self.db.cur.execute("INSERT OR IGNORE INTO sec_borrower (lei, name) VALUES (?, ?)", (dct["lei"], dct["name"]))
                borrower_id = self.db.cur.execute("SELECT borrower_id FROM sec_borrower WHERE lei = ?", (dct["lei"],)).fetchone()[0]
                
                self.db.cur.execute("INSERT OR IGNORE INTO sec_mf_lending VALUES (?, ?, ?, ?)", (self.series_id, borrower_id, self.ts_period, dct["value"]))

        if self.filing.securities_lending["non_cash_collateral"] is not None:
            raise ValueError("non cash collteral not None")

    def insert_return_information(self) -> None:
        # insert class returns
        for class_cik, data in self.filing.return_information["class_returns"].items():
            security_id = self.db.cur.execute("SELECT security_id FROM sec_mf_class WHERE cik = ?", (class_cik,)).fetchone()[0]
            for date, class_return in data.items():
                ts = int(pd.to_datetime(date).timestamp())
                self.db.cur.execute(
                    "INSERT OR IGNORE INTO sec_mf_class_return (class_id, ts, return) VALUES (?, ?, ?)",
                    (security_id, ts, class_return)
                )
        
        # insert derivative gains
        for derivative, data in self.filing.return_information["derivative_gains"].items():
            self.db.cur.execute("INSERT OR IGNORE INTO sec_derivative_type (name) VALUES (?)", (derivative,))
            derivative_type_id = self.db.cur.execute("SELECT type_id FROM sec_derivative_type WHERE name = ?", (derivative,)).fetchone()[0]
            for date in data.keys():
                if date != "derivative_types":
                    ts = int(pd.to_datetime(date).timestamp())
                    if data[date] is None:
                        realized_gain, unrealized_appreciation = None, None
                    else:
                        realized_gain = data[date]["realized_gain"]
                        unrealized_appreciation = data[date]["unrealized_appreciation"]
                    self.db.cur.execute(
                        """
                        INSERT OR IGNORE INTO sec_mf_derivative_gain
                        (series_id, derivative_type_id, contract_type_id, ts, realized_gain, unrealized_appreciation)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """
                        ,
                        (self.series_id, derivative_type_id, None, ts, realized_gain, unrealized_appreciation)
                    )
            for contract, contract_data in data["derivative_types"].items():
                self.db.cur.execute("INSERT OR IGNORE INTO sec_contract_type (name) VALUES (?)", (contract,))
                contract_type_id = self.db.cur.execute("SELECT type_id FROM sec_contract_type WHERE name = ?", (contract,)).fetchone()[0]
                for contract_date in contract_data:
                    deriv_ts = int(pd.to_datetime(contract_date).timestamp())
                    if contract_data[contract_date] is None:
                        deriv_realized_gain, deriv_unrealized_appreciation = None, None
                    else:
                        deriv_realized_gain = contract_data[contract_date]["realized_gain"]
                        deriv_unrealized_appreciation = contract_data[contract_date]["unrealized_appreciation"]
                    self.db.cur.execute(
                        """
                        INSERT OR IGNORE INTO sec_mf_derivative_gain
                        (series_id, derivative_type_id, contract_type_id, ts, realized_gain, unrealized_appreciation)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """
                        ,
                        (self.series_id, derivative_type_id, contract_type_id, deriv_ts, deriv_realized_gain, deriv_unrealized_appreciation)
                    )

        # insert non-derivative gains
        for date, data in self.filing.return_information["non_derivative_gains"].items():
            ts = int(pd.to_datetime(date).timestamp())
            self.db.cur.execute(
                """
                INSERT OR IGNORE INTO sec_mf_nonderivative_gain
                (series_id, ts, realized_gain, unrealized_appreciation)
                VALUES (?, ?, ?, ?)
                """
                ,
                (self.series_id, ts, data["realized_gain"], data["unrealized_appreciation"])
            )