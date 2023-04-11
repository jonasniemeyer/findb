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
    REVENUE_ESTIMATE_HIGH = "Revenue Estimate High"
    REVENUE_ESTIMATE_LOW = "Revenue Estimate Low"
    REVENUE_ESTIMATE_AVG = "Revenue Estimate Average"
    REVENUE_ANALYSTS = "Total Revenue Analyst Count"
    COGS = "Cost of Revenue"
    GROSS_PROFIT = "Gross Profit"
    RD = "Research & Development Expenses"
    GA = "General & Administrative Expenses"
    SM = "Selling & Marketing Expenses"
    SGA = "Selling, General & Administrative Expenses"
    SGA_ESTIMATE_HIGH = "SG&A Estimate High"
    SGA_ESTIMATE_LOW = "SG&A Estimate Low"
    SGA_ESTIMATE_AVG = "SG&A Estimate Average"
    OTHER_OPERATING_INCOME = "Other Operating Income/Expenses"
    TOTAL_OPERATING_EXPENSES = "Total Operating Expenses"
    TOTAL_EXPENSES = "Total Expenses"
    OPERATING_INCOME = "Total Operating Income"
    OPERATING_INCOME_ANALYSTS = "Total Operating Income Analyst Count"
    INTEREST_INCOME = "Interest Income"
    INTEREST_EXPENSE = "Interest Expense"
    NONOPERATING_INCOME = "Non-Operating Income/Loss"
    PRETAX_INCOME = "Income Before Income Taxes"
    PRETAX_INCOME_ANALYSTS = "Income Before Income Taxes Analyst Count"
    INCOME_TAXES = "Income Taxes"
    INCOME_AFTER_TAXES = "Income After Taxes"
    OTHER_INCOME = "Other Income/Expenses"
    EBITDA = "EBITDA"
    EBITDA_ESTIMATE_HIGH = "EBITDA Estimate High"
    EBITDA_ESTIMATE_LOW = "EBITDA Estimate Low"
    EBITDA_ESTIMATE_AVG = "EBITDA Estimate Average"
    EBITDA_ANALYSTS = "EBITDA Analyst Count"
    EBIT = "EBIT"
    EBIT_ESTIMATE_HIGH = "EBIT Estimate High"
    EBIT_ESTIMATE_LOW = "EBIT Estimate Low"
    EBIT_ESTIMATE_AVG = "EBIT Estimate Average"
    NET_INCOME = "Net Income"
    NET_INCOME_ESTIMATE_HIGH = "Net Income Estimate High"
    NET_INCOME_ESTIMATE_LOW = "Net Income Estimate Low"
    NET_INCOME_ESTIMATE_AVG = "Net Income Estimate Average"
    NET_INCOME_ANALYSTS = "Net Income Analyst Count"
    NET_INCOME_CONTINUED = "Net Income From Continued Operations"
    NET_INCOME_DISCONTINUED = "Net Income From Discontinued Operations"
    SHARES_BASIC = "Basic Shares Outstanding"
    SHARES_DILUTED = "Diluted Shares Outstanding"
    EPS_BASIC = "Basic EPS"
    EPS_DILUTED = "Diluted EPS"
    EPS_DILUTED_ESTIMATE_HIGH = "EPS Diluted Estimate High"
    EPS_DILUTED_ESTIMATE_LOW = "EPS Diluted Estimate Low"
    EPS_DILUTED_ESTIMATE_AVG = "EPS Diluted Estimate Average"
    EPS_DILUTED_ANALYSTS = "Diluted EPS Analyst Count"
    DIVIDENDS_PER_SHARE = "Dividends Per Share"
    DIVIDENDS_PER_SHARE_ANALYSTS = "Dividends Per Share Analyst Count"

    # Balance Sheet
    CASH = "Cash and Cash Equivalents"
    ST_SECURITIES = "Short-Term Marketable Securities"
    CASH_ST_SECURITIES = "Cash and Short-Term Marketable Securities"
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
    TAX_ASSETS = "Tax Assets"
    OTHER_NONCURRENT_ASSETS = "Other Non-Current Assets"
    TOTAL_NONCURRENT_ASSETS = "Total Non-Current Assets"

    TOTAL_INVESTMENTS ="Total Investments"
    OTHER_ASSETS = "Other Assets"
    TOTAL_ASSETS = "Total Assets"
    TOTAL_ASSETS_ANALYSTS = "Total Assets Analyst Count"

    ST_DEBT = "Short-Term Debt"
    TAX_LIABILITIES = "Tax Liabilities"
    CURRENT_LIABILITIES = "Current Liabilities"
    ACCOUNTS_PAYABLE = "Accounts Payable"
    ST_DEFERRED_REVENUE = "Short-Term Deferred Revenue"
    OTHER_CURRENT_LIABILITIES = "Other Current Liabilities"
    TOTAL_CURRENT_LIABILITIES = "Total Current Liabilities"
    LT_DEBT = "Long-Term Debt"
    LT_DEFERRED_REVENUE = "Long-Term Deferred Revenue"
    LT_DEFERRED_TAX_LIABILITIES = "Long-Term Deferred Tax Liabilities"
    OTHER_NONCURRENT_LIABILITIES = "Other Non-Current Liabilities"
    TOTAL_NONCURRENT_LIABILITIES = "Total Non-Current Liabilities"
    OTHER_LIABILITIES = "Other Liabilities"
    CAPITAL_LEASE_OBLIGATIONS = "Capital Lease Obligations"
    TOTAL_DEBT = "Total Debt"
    NET_DEBT = "Net Debt"
    TOTAL_LIABILITIES = "Total Liabilities"

    COMMON_STOCK = "Common Stock"
    PREFERRED_STOCK = "Preferred Stock"
    RETAINED_EARNINGS = "Retained Earnings"
    COMPREHENSIVE_INCOME = "Comprehensive Income"
    OTHER_SHAREHOLDERS_EQUITY = "Other Shareholders' Equity"
    TOTAL_SHAREHOLDERS_EQUITY = "Total Shareholders' Equity"
    TOTAL_SHAREHOLDERS_EQUITY_ANALYSTS = "Total Shareholders' Equity Analyst Count"
    TOTAL_EQUITY = "Total Equity"
    MINORITY_INTEREST = "Minority Interest"

    TOTAL_LIABILITIES_AND_SHAREHOLDERS_EQUITY = "Total Liabilities And Shareholders' Equity"
    TOTAL_LIABILITIES_AND_EQUITY = "Total Liabilities And Equity"

    # Cashflow Statement
    NET_INCOME_CF = "Net Income"
    DA = "Depreciation and Amortization"
    DEFERRED_INCOME_TAXES = "Deferred Income Taxes"
    CHANGE_OTHER_NONCASH = "Change of Other Non-Cash Items"
    CHANGE_TOTAL_NONCASH = "Change of Total Non-Cash Items"
    SBC = "Stock-Based Compensation"
    CHANGE_WORKING_CAPITAL = "Change of Working Capital"
    CHANGE_INVENTORY = "Change of Inventory"
    CHANGE_ACCOUNTS_RECEIVABLE = "Change of Accounts Receivable"
    CHANGE_ACCOUNTS_PAYABLE = "Change of Accounts Payable"
    CHANGE_OTHER_WORKING_CAPITAL = "Change of Other Working Capital"
    CHANGE_OTHER_ASSETS_LIABILITIES = "Change of Other Assets and Liabilities"
    CHANGE_TOTAL_ASSETS_LIABILITIES = "Change of Total Assets and Liabilities"
    OPERATING_CASHFLOW = "Operating Cashflow"
    CASHFLOW_PER_SHARE = "Cashflow Per Share"
    CASHFLOW_PER_SHARE_ANALYSTS = "Cashflow Per Share Analyst Count"

    CAPEX = "Capital Expenditures"
    CAPEX_ANALYSTS = "Capital Expenditures Analyst Count"
    PURCHASE_SECURITIES = "Purchase of Securities"
    SALE_MATURITY_SECURITIES = "Sales and Maturity of Securities"
    CHANGE_ST_SECURITIES = "Change of Short-Term Securities"
    CHANGE_LT_SECURITIES = "Change of Long-Term Securities"
    CHANGE_SECURITIES = "Change of Securities"
    ACQUISITIONS = "Acquisitions"
    CHANGE_INTANGIBLE_ASSETS = "Change of Intangible Assets"
    OTHER_INVESTING_ACTIVITIES = "Other Investing Activities"
    INVESTING_CASHFLOW = "Investing Cashflow"

    SHARES_ISSUED = "Shares Issued"
    LT_DEBT_ISSUED = "Long-Term Debt Issued"
    ST_DEBT_ISSUED = "Short-Term Debt Issued"
    TOTAL_DEBT_ISSUED = "Total Debt Issued"
    TOTAL_DEBT_REPAID = "Total Debt Repaid"
    DIVIDENDS_PAID = "Dividends Paid"
    SHARES_REPURCHASED = "Shares Repurchased"
    COMMON_STOCK_ISSUED = "Common Stock Issued"
    TOTAL_STOCK_ISSUED = "Total Stock Issued"
    OTHER_FINANCING_ACTIVITIES = "Other Financing Activities"
    FINANCING_CASHFLOW = "Financing Cashflow"

    FREE_CASHFLOW = "Free Cashflow"
    FREE_CASHFLOW_ANALYSTS = "Free Cashflow Analyst Count"
    CASH_START_PERIOD = "Cash and Cash Equivalents Start of Period"
    CURRENCY_CASH_IMPACT = "Currency Impact on Cash and Cash Equivalents"
    CHANGE_CASH = "Change of Cash and Cash Equivalents"
    CASH_END_PRIOD = "Cash and Cash Equivalents End of Period"

    # Financial Ratios
    GROSS_MARGIN = "Gross Margin"
    EBITDA_MARGIN = "EBITDA Margin"
    OPERATING_MARGIN = "Operating Margin"
    OPERATING_MARGIN_ANALYSTS = "Operating Margin Analyst Count"
    PRETAX_MARGIN = "Pre-Tax Margin"
    NET_MARGIN = "Net Margin"
    NET_MARGIN_ANALYSTS = "Net Margin Analyst Count"
    FCF_MARGIN = "FCF Margin"
    FCF_MARGIN_ANALYSTS = "FCF Margin Analyst Count"
    FCF_CONVERSION = "FCF Conversion"
    FCF_CONVERSION_ANALYSTS = "FCF Conversion Analyst Count"

    REVENUE_PER_SHARE = "Revenue Per Share"
    NET_INCOME_PER_SHARE = "Net Income Per Share"
    OPERATING_CASHFLOW_PER_SHARE = "Operating Cashflow Per Share"
    FCF_PER_SHARE = "FCF Per Share"
    CASH_PER_SHARE = "Cash Per Share"
    TANGIBLE_BOOK_VALUE_PER_SHARE = "Tangible Book Value Per Share"
    BOOK_VALUE_PER_SHARE = "Book Value Per Share"
    BOOK_VALUE_PER_SHARE_ANALYSTS = "Book Value Per Share Analyst Count"
    EQUITY_PER_SHARE = "Equity Per Share"
    DEBT_PER_SHARE = "Debt Per Share"
    MARKET_CAP = "Market Capitalization"
    ENTERPRISE_VALUE = "Enterprise Value"

    PB = "Price/Book Ratio"
    PS = "Price/Sales Ratio"
    PE = "Price/Earnings Ratio"
    PRICE_OPERATING_CASHFLOW = "Price/Operating-Cashflow Ratio"
    PRICE_FCF = "Price/FCF Ratio"
    EV_SALES = "Enterprise-Value/Sales Ratio"
    EV_EBITDA = "Enterprise-Value/EBITDA Ratio"
    EV_OPERATING_CASHFLOW = "Enterprise-Value/Operating-Cashflow Ratio"
    EV_FCF = "Enterprise-Value/FCF Ratio"
    PRICE_TANGIBLE_EQUITY = "Price/Tangible-Equity Ratio"
    EARNINGS_YIELD = "Earnings Yield"
    FCF_YIELD = "FCF Yield"
    DIVIDEND_YIELD = "Dividend Yield"

    DEBT_EQUITY = "Debt/Equity"
    DEBT_ASSETS = "Debt/Assets"
    DEBT_EBITDA = "Debt/EBITDA"
    CURRENT_RATIO = "Current Ratio"
    INTEREST_COVERAGE = "Interest Coverage"
    INCOME_QUALITY = "Income Quality"
    PAYOUT_RATIO = "Payout Ratio"
    SGA_REVENUE = "SG&A/Revenue"
    RD_REVENUE = "R&D/Revenue"
    INTANGIBLES_TOTAL_ASSETS = "Intangibles/Total-Assets"
    CAPEX_OPERATING_CASHFLOW = "Capex/Operating-Cashflow"
    CAPEX_REVENUE = "Capex/Revenue"
    CAPEX_DA = "Capex/Depreciation&Amortization"
    SBC_REVENUE = "Stock-Based-Compensation/Revenue"
    GRAHAM_NUMBER = "Graham Number"
    ROIC = "Return on Invested Capital"
    RETURN_TANGIBLE_ASSETS = "Return on Tangible Assets"
    GRAHAM_NET_NET = "Graham Net Net"
    WORKING_CAPITAL = "Working Capital"
    TANGIBLE_ASSETS = "Tangible Assets"
    NET_CURRENT_ASSETS = "Net Current Assets"
    INVESTED_CAPITAL = "Invested Capital"
    AVERAGE_RECEIVABLES = "Average Receivables"
    AVERAGE_PAYABLES = "Average Payables"
    AVERAGE_INVENTORY = "Average Inventory"
    DAYS_SALES_OUTSTANDING = "Days of Sales Outstanding"
    DAYS_PAYABLES_OUTSTANDING = "Days of Payables Outstanding"
    DAYS_INVENTORY = "Days of Inventory"
    RECEIVABLE_TURNOVER = "Receivable Turnover"
    PAYABLES_TURNOVER = "Payables Turnover"
    INVENTORY_TURNOVER = "Inventory Turnover"
    ROE = "Return on Equity"
    CAPEX_PER_SHARE = "Capex Per Share"


MACROTRENDS_CONVERSION = {
    # Income Statement
    "INCOME_STATEMENT": {
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
        "EPS - Earnings Per Share": Conversion.EPS_DILUTED
    },
    "BALANCE_SHEET": {
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
        "Total Liabilities And Share Holders Equity": Conversion.TOTAL_LIABILITIES_AND_SHAREHOLDERS_EQUITY 
    },
    "CASHFLOW_STATEMENT": {
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
}

MARKETSCREENER_CONVERSION = {
    "INCOME_STATEMENT": {
        "Net Sales": Conversion.REVENUE,
        "Net Sales Analysts": Conversion.REVENUE_ANALYSTS,
        "EBITDA": Conversion.EBITDA,
        "EBITDA Analysts": Conversion.EBITDA_ANALYSTS,
        "Operating Profit": Conversion.OPERATING_INCOME,
        "Operating Profit Analysts": Conversion.OPERATING_INCOME_ANALYSTS,
        "Pre-Tax Profit": Conversion.PRETAX_INCOME,
        "Pre-Tax Profit Analysts": Conversion.PRETAX_INCOME_ANALYSTS,
        "Net Income": Conversion.NET_INCOME,
        "Net Income Analysts": Conversion.NET_INCOME_ANALYSTS,
        "EPS": Conversion.EPS_DILUTED,
        "EPS Analysts": Conversion.EPS_DILUTED_ANALYSTS,
        "Dividend Per Share": Conversion.DIVIDENDS_PER_SHARE,
        "Dividend Per Share Analysts": Conversion.DIVIDENDS_PER_SHARE_ANALYSTS
    },
    "BALANCE_SHEET": {
        "Assets": Conversion.TOTAL_ASSETS,
        "Assets Analysts": Conversion.TOTAL_ASSETS_ANALYSTS,
        "Shareholders' Equity": Conversion.TOTAL_SHAREHOLDERS_EQUITY,
        "Shareholders' Equity Analysts": Conversion.TOTAL_SHAREHOLDERS_EQUITY_ANALYSTS,
        "Book Value Per Share": Conversion.BOOK_VALUE_PER_SHARE,
        "Book Value Per Share Analysts": Conversion.BOOK_VALUE_PER_SHARE_ANALYSTS
    },
    "CASHFLOW_STATEMENT": {
        "Free Cash Flow": Conversion.FREE_CASHFLOW,
        "Free Cash Flow Analysts": Conversion.FREE_CASHFLOW_ANALYSTS,
        "Cash Flow Per Share": Conversion.CASHFLOW_PER_SHARE,
        "Cash Flow Per Share Analysts": Conversion.CASHFLOW_PER_SHARE_ANALYSTS,
        "Capex": Conversion.CAPEX,
        "Capex Analysts": Conversion.CAPEX_ANALYSTS
    },
    "FINANCIAL_RATIOS": {
        "Operating Margin": Conversion.OPERATING_MARGIN,
        "Operating Margin Analysts": Conversion.OPERATING_MARGIN_ANALYSTS,
        "Net Margin": Conversion.NET_MARGIN,
        "Net Margin Analysts": Conversion.NET_MARGIN_ANALYSTS,
        "FCF Margin": Conversion.FCF_MARGIN,
        "FCF Margin Analysts": Conversion.FCF_MARGIN_ANALYSTS,
        "FCF Conversion": Conversion.FCF_CONVERSION,
        "FCF Conversion Analysts": Conversion.FCF_CONVERSION_ANALYSTS
    }
}

STRATOSPHERE_CONVERSION = {
    "INCOME_STATEMENT": {
        "revenue": Conversion.REVENUE,
        "costOfRevenue": Conversion.COGS,
        "grossProfit": Conversion.GROSS_PROFIT,
        "grossProfitRatio": Conversion.GROSS_MARGIN,
        "researchAndDevelopmentExpenses": Conversion.RD,
        "generalAndAdministrativeExpenses": Conversion.GA,
        "sellingAndMarketingExpenses": Conversion.SM,
        "sellingGeneralAndAdministrativeExpenses": Conversion.SGA,
        "otherExpenses": Conversion.OTHER_OPERATING_INCOME,
        "operatingExpenses": Conversion.TOTAL_OPERATING_EXPENSES,
        "costAndExpenses": Conversion.TOTAL_EXPENSES,
        "interestIncome": Conversion.INTEREST_INCOME,
        "interestExpense": Conversion.INTEREST_EXPENSE,
        "depreciationAndAmortization": Conversion.DA,
        "ebitda": Conversion.EBITDA,
        "ebitdaratio": Conversion.EBITDA_MARGIN,
        "operatingIncome": Conversion.OPERATING_INCOME,
        "operatingIncomeRatio": Conversion.OPERATING_MARGIN,
        "totalOtherIncomeExpensesNet": Conversion.OTHER_INCOME,
        "incomeBeforeTax": Conversion.PRETAX_INCOME,
        "incomeBeforeTaxRatio": Conversion.PRETAX_MARGIN,
        "incomeTaxExpense": Conversion.INCOME_TAXES,
        "netIncome": Conversion.NET_INCOME,
        "netIncomeRatio": Conversion.NET_MARGIN,
        "eps": Conversion.EPS_BASIC,
        "epsdiluted": Conversion.EPS_DILUTED,
        "weightedAverageShsOut": Conversion.SHARES_BASIC,
        "weightedAverageShsOutDil": Conversion.SHARES_DILUTED
    },
    "BALANCE_SHEET": {
        "cashAndCashEquivalents": Conversion.CASH,
        "shortTermInvestments": Conversion.ST_SECURITIES,
        "cashAndShortTermInvestments": Conversion.CASH_ST_SECURITIES,
        "netReceivables": Conversion.ACCOUNTS_RECEIVABLE,
        "inventory": Conversion.INVENTORY,
        "otherCurrentAssets": Conversion.OTHER_CURRENT_ASSETS,
        "totalCurrentAssets": Conversion.TOTAL_CURRENT_ASSETS,
        "propertyPlantEquipmentNet": Conversion.PROPERTY_PLANT_EQUIPMENT,
        "goodwill": Conversion.GOODWILL,
        "intangibleAssets": Conversion.INTANGIBLE_ASSETS,
        "goodwillAndIntangibleAssets": Conversion.GOODWILL_INTANGIBLES,
        "longTermInvestments": Conversion.LT_SECURITIES,
        "taxAssets": Conversion.TAX_ASSETS,
        "otherNonCurrentAssets": Conversion.OTHER_NONCURRENT_ASSETS,
        "totalNonCurrentAssets": Conversion.TOTAL_NONCURRENT_ASSETS,
        "otherAssets": Conversion.OTHER_ASSETS,
        "totalAssets": Conversion.TOTAL_ASSETS,
        "accountPayables": Conversion.ACCOUNTS_PAYABLE,
        "shortTermDebt": Conversion.ST_DEBT,
        "taxPayables": Conversion.TAX_LIABILITIES,
        "deferredRevenue": Conversion.ST_DEFERRED_REVENUE,
        "otherCurrentLiabilities": Conversion.OTHER_CURRENT_LIABILITIES,
        "totalCurrentLiabilities": Conversion.TOTAL_CURRENT_LIABILITIES,
        "longTermDebt": Conversion.LT_DEBT,
        "deferredRevenueNonCurrent": Conversion.LT_DEFERRED_REVENUE,
        "deferredTaxLiabilitiesNonCurrent": Conversion.LT_DEFERRED_TAX_LIABILITIES,
        "otherNonCurrentLiabilities": Conversion.OTHER_NONCURRENT_LIABILITIES,
        "totalNonCurrentLiabilities": Conversion.TOTAL_NONCURRENT_LIABILITIES,
        "otherLiabilities": Conversion.OTHER_LIABILITIES,
        "capitalLeaseObligations": Conversion.CAPITAL_LEASE_OBLIGATIONS,
        "totalLiabilities": Conversion.TOTAL_LIABILITIES,
        "preferredStock": Conversion.PREFERRED_STOCK,
        "commonStock": Conversion.COMMON_STOCK,
        "retainedEarnings": Conversion.RETAINED_EARNINGS,
        "accumulatedOtherComprehensiveIncomeLoss": Conversion.COMPREHENSIVE_INCOME,
        "othertotalStockholdersEquity": Conversion.OTHER_SHAREHOLDERS_EQUITY,
        "totalStockholdersEquity": Conversion.TOTAL_SHAREHOLDERS_EQUITY,
        "totalEquity": Conversion.TOTAL_EQUITY,
        "totalLiabilitiesAndStockholdersEquity": Conversion.TOTAL_LIABILITIES_AND_SHAREHOLDERS_EQUITY,
        "minorityInterest": Conversion.MINORITY_INTEREST,
        "totalLiabilitiesAndTotalEquity": Conversion.TOTAL_LIABILITIES_AND_EQUITY,
        "totalInvestments": Conversion.TOTAL_INVESTMENTS,
        "totalDebt": Conversion.TOTAL_DEBT,
        "netDebt": Conversion.NET_DEBT
    },
    "CASHFLOW_STATEMENT": {
        "netIncome": Conversion.NET_INCOME_CF,
        "depreciationAndAmortization": Conversion.DA,
        "deferredIncomeTax": Conversion.DEFERRED_INCOME_TAXES,
        "stockBasedCompensation": Conversion.SBC,
        "changeInWorkingCapital": Conversion.CHANGE_WORKING_CAPITAL,
        "accountsReceivables": Conversion.CHANGE_ACCOUNTS_RECEIVABLE,
        "inventory": Conversion.CHANGE_INVENTORY,
        "accountsPayables": Conversion.CHANGE_ACCOUNTS_PAYABLE,
        "otherWorkingCapital": Conversion.CHANGE_OTHER_WORKING_CAPITAL,
        "otherNonCashItems": Conversion.CHANGE_OTHER_NONCASH,
        "netCashProvidedByOperatingActivities": Conversion.OPERATING_CASHFLOW,
        "investmentsInPropertyPlantAndEquipment": Conversion.CAPEX,
        "acquisitionsNet": Conversion.ACQUISITIONS,
        "purchasesOfInvestments": Conversion.PURCHASE_SECURITIES,
        "salesMaturitiesOfInvestments": Conversion.SALE_MATURITY_SECURITIES,
        "otherInvestingActivites": Conversion.OTHER_INVESTING_ACTIVITIES,
        "netCashUsedForInvestingActivites": Conversion.INVESTING_CASHFLOW,
        "debtRepayment": Conversion.TOTAL_DEBT_REPAID,
        "commonStockIssued": Conversion.TOTAL_STOCK_ISSUED,
        "commonStockRepurchased": Conversion.SHARES_REPURCHASED,
        "dividendsPaid": Conversion.DIVIDENDS_PAID,
        "otherFinancingActivites": Conversion.OTHER_FINANCING_ACTIVITIES,
        "netCashUsedProvidedByFinancingActivities": Conversion.FINANCING_CASHFLOW,
        "effectOfForexChangesOnCash": Conversion.CURRENCY_CASH_IMPACT,
        "netChangeInCash": Conversion.CHANGE_CASH,
        "cashAtEndOfPeriod": Conversion.CASH_END_PRIOD,
        "cashAtBeginningOfPeriod": Conversion.CASH_START_PERIOD,
        "operatingCashFlow": Conversion.OPERATING_CASHFLOW,
        "capitalExpenditure": Conversion.CAPEX,
        "freeCashFlow": Conversion.FREE_CASHFLOW
    },
    "FINANCIAL_RATIOS": {
        "revenuePerShare": Conversion.REVENUE_PER_SHARE,
        "netIncomePerShare": Conversion.NET_INCOME_PER_SHARE,
        "operatingCashFlowPerShare": Conversion.OPERATING_CASHFLOW_PER_SHARE,
        "freeCashFlowPerShare": Conversion.FCF_PER_SHARE,
        "cashPerShare": Conversion.CASH_PER_SHARE,
        "bookValuePerShare": Conversion.BOOK_VALUE_PER_SHARE,
        "tangibleBookValuePerShare": Conversion.TANGIBLE_BOOK_VALUE_PER_SHARE,
        "shareholdersEquityPerShare": Conversion.EQUITY_PER_SHARE,
        "interestDebtPerShare": Conversion.DEBT_PER_SHARE,
        "marketCap": Conversion.MARKET_CAP,
        "enterpriseValue": Conversion.ENTERPRISE_VALUE,
        "peRatio": Conversion.PE,
        "priceToSalesRatio": Conversion.PS,
        "pocfratio": Conversion.PRICE_OPERATING_CASHFLOW,
        "pfcfRatio": Conversion.PRICE_FCF,
        "pbRatio": Conversion.PB,
        "ptbRatio": Conversion.PRICE_TANGIBLE_EQUITY,
        "evToSales": Conversion.EV_SALES,
        "enterpriseValueOverEBITDA": Conversion.EV_EBITDA,
        "evToOperatingCashFlow": Conversion.EV_OPERATING_CASHFLOW,
        "evToFreeCashFlow": Conversion.EV_FCF,
        "earningsYield": Conversion.EARNINGS_YIELD,
        "freeCashFlowYield": Conversion.FCF_YIELD,
        "debtToEquity": Conversion.DEBT_EQUITY,
        "debtToAssets": Conversion.DEBT_ASSETS,
        "netDebtToEBITDA": Conversion.DEBT_EBITDA,
        "currentRatio": Conversion.CURRENT_RATIO,
        "interestCoverage": Conversion.INTEREST_COVERAGE,
        "incomeQuality": Conversion.INCOME_QUALITY,
        "dividendYield": Conversion.DIVIDEND_YIELD,
        "payoutRatio": Conversion.PAYOUT_RATIO,
        "salesGeneralAndAdministrativeToRevenue": Conversion.SGA_REVENUE,
        "researchAndDdevelopementToRevenue": Conversion.RD_REVENUE,
        "intangiblesToTotalAssets": Conversion.INTANGIBLES_TOTAL_ASSETS,
        "capexToOperatingCashFlow": Conversion.CAPEX_OPERATING_CASHFLOW,
        "capexToRevenue": Conversion.CAPEX_REVENUE,
        "capexToDepreciation": Conversion.CAPEX_DA,
        "stockBasedCompensationToRevenue": Conversion.SBC_REVENUE,
        "grahamNumber": Conversion.GRAHAM_NUMBER,
        "roic": Conversion.ROIC,
        "returnOnTangibleAssets": Conversion.RETURN_TANGIBLE_ASSETS,
        "grahamNetNet": Conversion.GRAHAM_NET_NET,
        "workingCapital": Conversion.WORKING_CAPITAL,
        "tangibleAssetValue": Conversion.TANGIBLE_ASSETS,
        "netCurrentAssetValue": Conversion.NET_CURRENT_ASSETS,
        "investedCapital": Conversion.INVESTED_CAPITAL,
        "averageReceivables": Conversion.AVERAGE_RECEIVABLES,
        "averagePayables": Conversion.AVERAGE_PAYABLES,
        "averageInventory": Conversion.AVERAGE_INVENTORY,
        "daysSalesOutstanding": Conversion.DAYS_SALES_OUTSTANDING,
        "daysPayablesOutstanding": Conversion.DAYS_PAYABLES_OUTSTANDING,
        "daysOfInventoryOnHand": Conversion.DAYS_INVENTORY,
        "receivablesTurnover": Conversion.RECEIVABLE_TURNOVER,
        "payablesTurnover": Conversion.PAYABLES_TURNOVER,
        "inventoryTurnover": Conversion.INVENTORY_TURNOVER,
        "roe": Conversion.ROE,
        "capexPerShare": Conversion.CAPEX_PER_SHARE,
    },
    "ESTIMATES": {
        "estimatedRevenueLow": Conversion.REVENUE_ESTIMATE_LOW,
        "estimatedRevenueHigh": Conversion.REVENUE_ESTIMATE_HIGH,
        "estimatedRevenueAvg": Conversion.REVENUE_ESTIMATE_AVG,
        "estimatedEbitdaLow": Conversion.EBITDA_ESTIMATE_LOW,
        "estimatedEbitdaHigh": Conversion.EBITDA_ESTIMATE_HIGH,
        "estimatedEbitdaAvg": Conversion.EBITDA_ESTIMATE_AVG,
        "estimatedEbitLow": Conversion.EBIT_ESTIMATE_LOW,
        "estimatedEbitHigh": Conversion.EBIT_ESTIMATE_HIGH,
        "estimatedEbitAvg": Conversion.EBIT_ESTIMATE_AVG,
        "estimatedNetIncomeLow": Conversion.NET_INCOME_ESTIMATE_LOW,
        "estimatedNetIncomeHigh": Conversion.NET_INCOME_ESTIMATE_HIGH,
        "estimatedNetIncomeAvg": Conversion.NET_INCOME_ESTIMATE_AVG,
        "estimatedSgaExpenseLow": Conversion.SGA_ESTIMATE_LOW,
        "estimatedSgaExpenseHigh": Conversion.SGA_ESTIMATE_HIGH,
        "estimatedSgaExpenseAvg": Conversion.SGA_ESTIMATE_AVG,
        "estimatedEpsLow": Conversion.EPS_DILUTED_ESTIMATE_LOW,
        "estimatedEpsHigh": Conversion.EPS_DILUTED_ESTIMATE_HIGH,
        "estimatedEpsAvg": Conversion.EPS_DILUTED_ESTIMATE_AVG,
        "numberAnalystEstimatedRevenue": Conversion.REVENUE_ANALYSTS,
        "numberAnalystsEstimatedEps": Conversion.EPS_DILUTED_ANALYSTS
    }
}