from pathlib import Path
from enum import Enum

DB_PATH = rf"{Path(__file__).parent}\database.db"

SEC_BASE_URL = "https://www.sec.gov/Archives"

HEADERS = {
        "Connection": "keep-alive",
        "Expires": "-1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        )
    }

class Conversion(Enum):
    # Income Statement
    REVENUE = "Total Revenue"
    COGS = "Cost Of Revenue"
    GROSS_PROFIT = "Gross Profit"
    RD = "Research & Development Expenses"
    SGA = "Selling, General & Administrative Expenses"
    OTHER_OPERATING_INCOME = "Other Operating Income/Expenses"
    TOTAL_OPERATING_EXPENSES = "Total Operating Expenses"
    OPERATING_INCOME = "Total Operating Income"
    NONOPERATING_INCOME = "Non-Operating Income/Loss"
    PRETAX_INCOME = "Income Before Income Taxes"
    INCOME_TAXES = "Income Taxes"
    INCOME_AFTER_TAXES = "Income After Taxes"
    OTHER_INCOME = "Other Income/Expenses"
    EBITDA = "EBITDA"
    EBIT = "EBIT"
    NET_INCOME = "Net Income"
    NET_INCOME_CONTINUED = "Net Income From Continued Operations"
    NET_INCOME_DISCONTINUED = "Net Income From Discontinued Operations"
    SHARES_BASIC = "Basic Shares Outstanding"
    SHARES_DILUTED = "Diluted Shares Outstanding"
    EPS_BASIC = "Basic EPS"
    EPS_DILUTED = "Diluted EPS"

    # Balance Sheet
    CASH = "Cash And Cash Equivalents"
    ST_SECURITIES = "Short-Term Marketable Securities"
    ACCOUNTS_RECEIVABLE = "Accounts Receivable"
    INVENTORY = "Inventory"
    PREPAID_EXPENSES = "Prepaid Expenses"
    OTHER_CURRENT_ASSETS = "Other Current Assets"
    TOTAL_CURRENT_ASSETS = "Total Current Assets"

    PROPERTY_PLANT_EQUIPMENT = "Property, Plant & Equipment"
    LT_SECURITIES = "Long-Term Marketable Securities"
    GOODWILL = "GoodWill"
    INTANGIBLE_ASSETS = "Intangible Assets"
    GOODWILL_INTANGIBLES = "Goodwill and Intangible Assets"
    OTHER_NONCURRENT_ASSETS = "Other Non-Current Assets"
    TOTAL_NONCURRENT_ASSETS = "Total Non-Current Assets"

    TOTAL_ASSETS = "Total Assets"

    ST_DEBT = "Short-Term Debt"
    CURRENT_LIABILITIES = "Current Liabilities"
    LT_DEBT = "Long-Term Debt"
    OTHER_NONCURRENT_LIABILITIES = "Other Non-Current Liabilities"
    TOTAL_NONCURRENT_LIABILITIES = "Total Non-Current Liabilities"
    TOTAL_LIABILITIES = "Total Liabilities"

    COMMON_STOCK = "Common Stock"
    RETAINED_EARNINGS = "Retained Earnings"
    COMPREHENSIVE_INCOME = "Comprehensive Income"
    OTHER_SHAREHOLDERS_EQUITY = "Other Shareholder Equity"
    TOTAL_SHAREHOLDERS_EQUITY = "Total Shareholder Equity"

    TOTAL_LIABILITIES_AND_SHAREHOLDERS_EQUITY = ""

    # Cashflow Statement
    NET_INCOME_CF = "Net Income"
    DA = "Depreciation and Amortization"
    CHANGE_OTHER_NONCASH = "Change In Other Non-Cash Items"
    CHANGE_TOTAL_NONCASH = "Change In Total Non-Cash Items"
    SBC = "Stock-Based Compensation"
    CHANGE_INVENTORY = "Change In Inventory"
    CHANGE_ACCOUNTS_RECEIVABLE = "Change In Accounts Receivable"
    CHANGE_ACCOUNTS_PAYABLE = "Change in Accounts Payable"
    CHANGE_OTHER_ASSETS_LIABILITIES = "Change In Other Assets and Liabilities"
    CHANGE_TOTAL_ASSETS_LIABILITIES = "Change In Total Assets and Liabilities"
    OPERATING_CASHFLOW = "Operating Cashflow"

    CAPEX = "Capital Expenditures"
    CHANGE_ST_SECURITIES = "Change In Short-Term Securities"
    CHANGE_LT_SECURITIES = "Change In Long-Term Securities"
    CHANGE_SECURITIES = "Change In Securities"
    ACQUISITIONS = "Acquisitions"
    CHANGE_INTANGIBLE_ASSETS = "Change In Intangible Assets"
    OTHER_INVESTING_ACTIVITIES = "Other Investing Activities"
    INVESTING_CASHFLOW = "Investing Cashflow"

    SHARES_ISSUED = "Shares Issued"
    LT_DEBT_ISSUED = "Long-Term Debt Issued"
    ST_DEBT_ISSUED = "Short-Term Debt Issued"
    TOTAL_DEBT_ISSUED = "Total Debt Issued"
    DIVIDENDS_PAID = "Dividends Paid"
    SHARES_REPURCHASED = "Shares Repurchased"
    COMMON_STOCK_ISSUED = "Common Stock Issued"
    TOTAL_STOCK_ISSUED = "Total Stock Issued"
    OTHER_FINANCING_ACTIVITIES = "Other Financing Activities"
    FINANCING_CASHFLOW = "Financing Cashflow"

    FREE_CASHFLOW = "Free Cashflow"
    CASH_START_PERIOD = "Cash and Cash Equivalents Start of Period"
    CHANGE_CASH = "Change In Cash and Cash Equivalents"
    CASH_END_PRIOD = "Cash and Cash Equivalents End of Period"

MACROTRENDS_CONVERSION = {
    # Income Statement
    "Revenue": Conversion.REVENUE,
    "Cost Of Goods Sold": Conversion.COGS,
    "Gross Profit": Conversion.GROSS_PROFIT,
    "Research And Development Expenses": Conversion.RD,
    "SG&A Expenses": Conversion.SGA,
    "Other Operating Income Or Expenses": Conversion.OTHER_OPERATING_INCOME,
    "Operating Expenses": Conversion.TOTAL_OPERATING_EXPENSES,
    "Operating Income": Conversion.OPERATING_INCOME,
    "Total Non-Operating Income/Expense": Conversion.NONOPERATING_INCOME,
    "Pre-Tax Income": Conversion.PRETAX_INCOME,
    "Income Taxes": Conversion.INCOME_TAXES,
    "Income After Taxes": Conversion.INCOME_AFTER_TAXES,
    "Other Income": Conversion.OTHER_INCOME,
    "Income From Continuous Operations": Conversion.NET_INCOME_CONTINUED,
    "Income From Discontinued Operations": Conversion.NET_INCOME_DISCONTINUED,
    "Net Income": Conversion.NET_INCOME,
    "EBITDA": Conversion.EBITDA,
    "EBIT": Conversion.EBIT,
    "Basic Shares Outstanding": Conversion.SHARES_BASIC,
    "Shares Outstanding": Conversion.SHARES_DILUTED,
    "Basic EPS": Conversion.EPS_BASIC,
    "EPS - Earnings Per Share": Conversion.EPS_DILUTED,

    # Balance Sheet
    "Cash On Hand": Conversion.CASH,
    "Receivables": Conversion.ACCOUNTS_RECEIVABLE,
    "Inventory": Conversion.INVENTORY,
    "Pre-Paid Expenses": Conversion.PREPAID_EXPENSES,
    "Other Current Assets": Conversion.OTHER_CURRENT_ASSETS,
    "Total Current Assets": Conversion.TOTAL_CURRENT_ASSETS,
    "Property, Plant, And Equipment": Conversion.PROPERTY_PLANT_EQUIPMENT,
    "Long-Term Investments": Conversion.LT_SECURITIES,
    "Goodwill And Intangible Assets": Conversion.GOODWILL_INTANGIBLES,
    "Other Long-Term Assets": Conversion.OTHER_NONCURRENT_ASSETS,
    "Total Long-Term Assets": Conversion.TOTAL_NONCURRENT_ASSETS,
    "Total Assets": Conversion.TOTAL_ASSETS,
    "Total Current Liabilities": Conversion.CURRENT_LIABILITIES,
    "Long Term Debt": Conversion.LT_DEBT,
    "Other Non-Current Liabilities": Conversion.OTHER_NONCURRENT_LIABILITIES,
    "Total Long Term Liabilities": Conversion.TOTAL_NONCURRENT_LIABILITIES,
    "Total Liabilities": Conversion.TOTAL_LIABILITIES,
    "Common Stock Net": Conversion.COMMON_STOCK,
    "Retained Earnings (Accumulated Deficit)": Conversion.RETAINED_EARNINGS,
    "Comprehensive Income": Conversion.COMPREHENSIVE_INCOME,
    "Other Share Holders Equity": Conversion.OTHER_SHAREHOLDERS_EQUITY,
    "Share Holder Equity": Conversion.TOTAL_SHAREHOLDERS_EQUITY,
    "Total Liabilities And Share Holders Equity": Conversion.TOTAL_LIABILITIES_AND_SHAREHOLDERS_EQUITY,

    # Cashflow Statement
    "Net Income/Loss": Conversion.NET_INCOME_CF,
    "Total Depreciation And Amortization - Cash Flow": Conversion.DA,
    "Other Non-Cash Items": Conversion.CHANGE_OTHER_NONCASH,
    "Total Non-Cash Items": Conversion.CHANGE_TOTAL_NONCASH,
    "Change In Accounts Receivable": Conversion.CHANGE_ACCOUNTS_RECEIVABLE,
    "Change In Inventories": Conversion.CHANGE_INVENTORY,
    "Change In Accounts Payable": Conversion.CHANGE_ACCOUNTS_PAYABLE,
    "Change In Assets/Liabilities": Conversion.CHANGE_OTHER_ASSETS_LIABILITIES,
    "Total Change In Assets/Liabilities": Conversion.CHANGE_TOTAL_ASSETS_LIABILITIES,
    "Cash Flow From Operating Activities": Conversion.OPERATING_CASHFLOW,
    "Net Change In Property, Plant, And Equipment": Conversion.CAPEX,
    "Net Change In Intangible Assets": Conversion.CHANGE_INTANGIBLE_ASSETS,
    "Net Acquisitions/Divestitures": Conversion.ACQUISITIONS,
    "Net Change In Short-term Investments": Conversion.CHANGE_ST_SECURITIES,
    "Net Change In Long-Term Investments": Conversion.CHANGE_LT_SECURITIES,
    "Net Change In Investments - Total": Conversion.CHANGE_SECURITIES,
    "Investing Activities - Other": Conversion.OTHER_INVESTING_ACTIVITIES,
    "Cash Flow From Investing Activities": Conversion.INVESTING_CASHFLOW,
    "Net Long-Term Debt": Conversion.LT_DEBT_ISSUED,
    "Net Current Debt": Conversion.ST_DEBT_ISSUED,
    "Debt Issuance/Retirement Net - Total": Conversion.TOTAL_DEBT_ISSUED,
    "Net Common Equity Issued/Repurchased": Conversion.COMMON_STOCK_ISSUED,
    "Net Total Equity Issued/Repurchased": Conversion.TOTAL_STOCK_ISSUED,
    "Total Common And Preferred Stock Dividends Paid": Conversion.DIVIDENDS_PAID,
    "Financial Activities - Other": Conversion.OTHER_FINANCING_ACTIVITIES,
    "Cash Flow From Financial Activities": Conversion.FINANCING_CASHFLOW,
    "Net Cash Flow": Conversion.CHANGE_CASH,
    "Stock-Based Compensation": Conversion.SBC,
    "Common Stock Dividends Paid": Conversion.DIVIDENDS_PAID
}