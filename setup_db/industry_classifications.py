import requests
import re
from bs4 import BeautifulSoup, element
from finance_database import Database
from finance_database.utils import HEADERS

def get_gsci_classification() -> dict:
    url = "https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard"
    html = requests.get(url=url, headers=HEADERS).text
    soup = BeautifulSoup(html, "lxml")
    
    sectors = {}
    table = soup.find("table", {"class": "wikitable"}).find("tbody")
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) == 8:
            sector_code = int(cells[0].text)
            sector = cells[1].text.split("(")[0].strip()        
            industry_group_code = int(cells[2].text)
            industry_group = cells[3].text   .strip()      
            industry_code = int(cells[4].text)
            industry = cells[5].text.strip() 
            sub_industry_code = int(cells[6].text)
            sub_industry = cells[7].text.strip()

        elif len(cells) == 6:
            industry_group_code = int(cells[0].text)
            industry_group = cells[1].text   .strip()      
            industry_code = int(cells[2].text)
            industry = cells[3].text.strip() 
            sub_industry_code = int(cells[4].text)
            sub_industry = cells[5].text.strip() 

        elif len(cells) == 4:
            industry_code = int(cells[0].text)
            industry = cells[1].text.strip() 
            sub_industry_code = int(cells[2].text)
            sub_industry = cells[3].text.strip()

        elif len(cells) == 2:
            sub_industry_code = int(cells[0].text)
            sub_industry = cells[1].text.strip()

        if sector not in sectors:
            sectors[sector] = {
                "code": sector_code,
                "industry_groups": {}
            }

        if industry_group not in sectors[sector]["industry_groups"]:
            sectors[sector]["industry_groups"][industry_group] = {
                "code": industry_group_code,
                "industries": {}
            }

        if industry not in sectors[sector]["industry_groups"][industry_group]["industries"]:
            sectors[sector]["industry_groups"][industry_group]["industries"][industry] = {
                "code": industry_code,
                "sub_industries": {}
            }

        if sub_industry not in sectors[sector]["industry_groups"][industry_group]["industries"][industry]["sub_industries"]:
            sectors[sector]["industry_groups"][industry_group]["industries"][industry]["sub_industries"][sub_industry] = {
                "code": sub_industry_code
            }
    
    return sectors

def get_sic_classification() -> dict:
    html = requests.get("https://www.naics.com/everything-sic/").text
    soup = BeautifulSoup(html, "lxml")
    table = soup.find_all("table")[0]
    
    divisions = {}
    total_divisions = len(table.find_all("tr")[1:-1])
    for index, row in enumerate(table.find_all("tr")[1:-1]):
        division_name = row.find_all("td")[1].text
        print(f"Division {index+1:>2} of {total_divisions}: {division_name}")
        
        url = row.find("td").find("a").get("href")
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        rows = soup.find("table").find_all("tr")
        
        no_businesses = int(rows[-1].find_all("td")[-1].text.replace(",", ""))
        description = soup.find("div", {"id": "sicdivdescr"}).text

        divisions[division_name] = {
            "code": index+1,
            "no_businesses": no_businesses,
            "description": description.strip(),
            "major_groups": {}
        }
        
        for row in rows[1:-1]:
            cells = row.find_all("td")
            code = cells[0].text.strip()
            
            if len(code) == 2:
                code = int(code + "00")
                no_businesses = int(cells[2].text.replace(",", ""))
                
                url = cells[0].find("a").get("href")
                major_group_name, description, industry_groups = parse_sic_major_group_page(url)
                
                divisions[division_name]["major_groups"][major_group_name] = {
                    "code": code,
                    "no_businesses": no_businesses,
                    "description": description.strip(),
                    "industry_groups": industry_groups
                }
    
    return divisions

def parse_sic_major_group_page(url) -> tuple:
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    content = soup.find('div', {'class':'entry-content'})

    anchor_table = content.find("table")
    header = anchor_table.find_previous("h4")
    
    name = re.findall('Major Group: [0-9]+—(.+)', header.text)[0]
    
    description = ""
    for tag in header.next_siblings:
        if isinstance(tag, element.Tag) and tag.name != "br":
            break
        description += tag.text
    
    description = description.strip()
    
    industry_groups = {}
    industry_group_tags = content.find_all('h6')
    for industry_group in industry_group_tags:
        group_code, group_name = re.findall('Industry Group ([0-9]+): (.+)', industry_group.text)[0]
        group_code = int(group_code + '0')
        
        industry_groups[group_name] = {
            "code": group_code,
            "no_businesses": None,
            "description": None,
            "industries": {}
        }
        
        total_businesses = 0
        industries = {}
        industry_tags = industry_group.find_next("table").find_all('tr')
        for industry in industry_tags:
            cells = industry.find_all("td")
            code = int(cells[0].text)
            no_businesses = int(cells[2].text.replace(",", ""))

            url = cells[0].find("a").get("href")
            name, description = parse_sic_industry_page(url)
            industries[name] = {
                "code": code,
                "no_businesses": no_businesses,
                "description": description
            }
            
            total_businesses += no_businesses
        
        industry_groups[group_name]["no_businesses"] = no_businesses
        industry_groups[group_name]["industries"] = industries
            
    return name, description, industry_groups
    
def parse_sic_industry_page(url) -> tuple:
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")

    anchor_table = soup.find("table")
    header = anchor_table.find_previous("h6")
    
    name = re.findall('Industry: [0-9]+—(.+)', header.text)[0]

    description = ""
    for tag in header.next_siblings:
        if isinstance(tag, element.Tag) and tag.name != "br":
            break
        description += tag.text
    
    description = description.strip()    
    return name, description

def insert_gics_classifcation(db) -> None:
    gics_sectors = get_gsci_classification()
    for sector in gics_sectors.keys():
        db.cur.execute(
            "INSERT INTO industry_classification_gics (code, name, is_sector) VALUES(?, ?, ?)",
            (gics_sectors[sector]["code"], sector, True)
        )
        sector_id = db.cur.execute("SELECT industry_id FROM industry_classification_gics WHERE code = ?", (gics_sectors[sector]["code"],)).fetchone()[0]

        for industry_group in gics_sectors[sector]["industry_groups"].keys():
            db.cur.execute(
                "INSERT INTO industry_classification_gics (code, name, is_industry_group, parent_id) VALUES(?, ?, ?, ?)",
                (gics_sectors[sector]["industry_groups"][industry_group]["code"], industry_group, True, sector_id)
            )
            group_id = db.cur.execute("SELECT industry_id FROM industry_classification_gics WHERE code = ?", (gics_sectors[sector]["industry_groups"][industry_group]["code"],)).fetchone()[0]

            for industry in gics_sectors[sector]["industry_groups"][industry_group]["industries"]:
                db.cur.execute(
                    "INSERT INTO industry_classification_gics (code, name, is_industry, parent_id) VALUES(?, ?, ?, ?)",
                    (
                        gics_sectors[sector]["industry_groups"][industry_group]["industries"][industry]["code"],
                        industry,
                        True,
                        group_id
                    )
                )
                industry_id = db.cur.execute("SELECT industry_id FROM industry_classification_gics WHERE code = ?", (gics_sectors[sector]["industry_groups"][industry_group]["industries"][industry]["code"],)).fetchone()[0]

                for sub_industry in gics_sectors[sector]["industry_groups"][industry_group]["industries"][industry]["sub_industries"]:
                    db.cur.execute(
                        "INSERT INTO industry_classification_gics (code, name, is_sub_industry, parent_id) VALUES(?, ?, ?, ?)",
                        (
                            gics_sectors[sector]["industry_groups"][industry_group]["industries"][industry]["sub_industries"][sub_industry]["code"],
                            sub_industry,
                            True,
                            industry_id
                        )
                    )

def insert_sic_classification(db) -> None:
    sic_divisions = get_sic_classification()
    for division in sic_divisions:
        db.cur.execute(
            "INSERT INTO industry_classification_sic (code, name, no_businesses, is_division, description) VALUES (?, ?, ?, ?, ?)",
            (
                sic_divisions[division]["code"],
                division,
                sic_divisions[division]["no_businesses"],
                True,
                sic_divisions[division]["description"]
            )
        )
        division_id = db.cur.execute("SELECT industry_id FROM industry_classification_sic WHERE code = ?", (sic_divisions[division]["code"],)).fetchone()[0]

        for major_group in sic_divisions[division]["major_groups"]:
            db.cur.execute(
                "INSERT INTO industry_classification_sic (code, name, no_businesses, is_major_group, description, parent_id) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    sic_divisions[division]["major_groups"][major_group]["code"],
                    major_group,
                    sic_divisions[division]["major_groups"][major_group]["no_businesses"],
                    True,
                    sic_divisions[division]["major_groups"][major_group]["description"],
                    division_id
                )
            )
            major_group_id = db.cur.execute("SELECT industry_id FROM industry_classification_sic WHERE code = ?", (sic_divisions[division]["major_groups"][major_group]["code"],)).fetchone()[0]

            for industry_group in sic_divisions[division]["major_groups"][major_group]["industry_groups"]:
                db.cur.execute(
                    "INSERT INTO industry_classification_sic (code, name, no_businesses, is_industry_group, description, parent_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        sic_divisions[division]["major_groups"][major_group]["industry_groups"][industry_group]["code"],
                        industry_group,
                        sic_divisions[division]["major_groups"][major_group]["industry_groups"][industry_group]["no_businesses"],
                        True,
                        sic_divisions[division]["major_groups"][major_group]["industry_groups"][industry_group]["description"],
                        major_group_id
                    )
                )
                industry_group_id = db.cur.execute("SELECT industry_id FROM industry_classification_sic WHERE code = ?", (sic_divisions[division]["major_groups"][major_group]["industry_groups"][industry_group]["code"],)).fetchone()[0]

                for industry in sic_divisions[division]["major_groups"][major_group]["industry_groups"][industry_group]["industries"]:
                    db.cur.execute(
                        "INSERT INTO industry_classification_sic (code, name, no_businesses, is_industry, description, parent_id) VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            sic_divisions[division]["major_groups"][major_group]["industry_groups"][industry_group]["industries"][industry]["code"],
                            industry,
                            sic_divisions[division]["major_groups"][major_group]["industry_groups"][industry_group]["industries"][industry]["no_businesses"],
                            True,
                            sic_divisions[division]["major_groups"][major_group]["industry_groups"][industry_group]["industries"][industry]["description"],
                            industry_group_id
                        )
                    )