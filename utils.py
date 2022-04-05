from pathlib import Path

db_path = rf"{Path(__file__).parent}\database.db"

sec_base_url = "https://www.sec.gov/Archives"

headers = {
        "Connection": "keep-alive",
        "Expires": "-1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        )
    }

commodities = {
    "WTI Crude Oil": {
        "exchange": "CME",
        "sector": "energy",
        "group": "crude-oil",
        "name": "light-sweet-crude",
        "sector name": "Energy"
    },
    "Heating Oil": {
        "exchange": "CME",
        "sector": "energy",
        "group": "refined-products",
        "name": "heating-oil",
        "sector name": "Energy"
    },
    "Natural Gas": {
        "exchange": "CME",
        "sector": "energy",
        "group": "natural-gas",
        "name": "natural-gas",
        "sector name": "Energy"
    },
    "Cocoa": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "softs",
        "name": "cocoa",
        "sector name": "Agriculture"
    },
    "Coffee": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "softs",
        "name": "coffee",
        "sector name": "Agriculture"
    },
    "Corn": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "grain-and-oilseed",
        "name": "corn",
        "sector name": "Agriculture"
    },
    "Cotton": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "softs",
        "name": "cotton",
        "sector name": "Agriculture"
    },
    "Milk": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "dairy",
        "name": "class-iii-milk",
        "sector name": "Agriculture"
    },
    "Oats": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "grain-and-oilseed",
        "name": "oats",
        "sector name": "Agriculture"
    },
    "Soybean": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "grain-and-oilseed",
        "name": "soybean",
        "sector name": "Agriculture"
    },
    "Soybean Meal": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "grain-and-oilseed",
        "name": "soybean-meal",
        "sector name": "Agriculture"
    },
    "Soybean Oil": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "grain-and-oilseed",
        "name": "soybean-oil",
        "sector name": "Agriculture"
    },
    "Sugar": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "softs",
        "name": "sugar-no11",
        "sector name": "Agriculture"
    },
    "Wheat": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "grain-and-oilseed",
        "name": "wheat",
        "sector name": "Agriculture"
    },
    "Feeder Cattle": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "livestock",
        "name": "feeder-cattle",
        "sector name": "Livestock"
    },
    "Lean Hogs": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "livestock",
        "name": "lean-hogs",
        "sector name": "Livestock"
    },
    "Live Cattle": {
        "exchange": "CME",
        "sector": "agricultural",
        "group": "livestock",
        "name": "live-cattle",
        "sector name": "Livestock"
    },
    "Aluminum": {
        "exchange": "CME",
        "sector": "metals",
        "group": "base",
        "name": "aluminum",
        "sector name": "Industrial Metals"
    },
    "Copper": {
        "exchange": "CME",
        "sector": "metals",
        "group": "base",
        "name": "copper",
        "sector name": "Industrial Metals"
    },
    "Lead": {
        "exchange": "CME",
        "sector": "metals",
        "group": "base",
        "name": "lead",
        "sector name": "Industrial Metals"
    },
    "Zinc": {
        "exchange": "CME",
        "sector": "metals",
        "group": "base",
        "name": "zinc",
        "sector name": "Industrial Metals"
    },
    "Gold": {
        "exchange": "CME",
        "sector": "metals",
        "group": "precious",
        "name": "gold",
        "sector name": "Precious Metals"
    },
    "Palladium": {
        "exchange": "CME",
        "sector": "metals",
        "group": "precious",
        "name": "palladium",
        "sector name": "Precious Metals"
    },
    "Platinum": {
        "exchange": "CME",
        "sector": "metals",
        "group": "precious",
        "name": "platinum",
        "sector name": "Precious Metals"
    },
    "Silver": {
        "exchange": "CME",
        "sector": "metals",
        "group": "precious",
        "name": "silver",
        "sector name": "Precious Metals"
    }
}