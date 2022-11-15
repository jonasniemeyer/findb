from pathlib import Path

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