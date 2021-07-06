import requests
from bs4 import BeautifulSoup
import re
from finance_database import Database

def sic_list() -> dict:
    url = requests.get('https://www.naics.com/search/').text
    soup = BeautifulSoup(url, 'lxml')
    table = soup.find_all('table')[1]
    divisions_table = table.find_all('tr')[1:-1]

    divisions = {}

    for index, division in enumerate(divisions_table):
        division_char = division.find_all('a')[0].text
        division_url = division.find_all('a')[0].get('href')
        division_name = division.find_all('a')[2].text
        division_no_businesses = int(division.find_all('td')[-1].text.replace(',', ''))
        division_site = requests.get(division_url).text
        divisions[index] = {}
        divisions[index]['character'] = division_char
        divisions[index]['name'] = division_name
        divisions[index]['no_businesses'] = division_no_businesses
        divisions[index]['major_groups'] = {}
        soup = BeautifulSoup(division_site, 'lxml')
        table = soup.find('table')
        rows = table.find_all('tr')[1:-1]
        for row in rows:
            code = row.find_all('a')[0].text
            if len(code) == 2:
                major_group_url = row.find_all('a')[0].get('href')
                major_group_no_businesses = int(row.find_all('td')[-1].text.replace(',', ''))
                major_group_site = requests.get(major_group_url).text
                soup = BeautifulSoup(major_group_site, 'lxml')
                div = soup.find('div', {'class':'entry-content'})
                major_group_id, major_group_name = re.findall('Major Group: ([0-9]+)—(.+)', div.find('h4').text)[0]
                major_group_id = int(major_group_id + '00')

                divisions[index]['major_groups'][major_group_id] = {}
                divisions[index]['major_groups'][major_group_id]['name'] = major_group_name
                divisions[index]['major_groups'][major_group_id]['no_businesses'] = major_group_no_businesses
                divisions[index]['major_groups'][major_group_id]['industry_groups'] = {}

                industry_groups = div.find_all('h6')
                for industry_group in industry_groups:
                    group_id, group_name = re.findall('Industry Group ([0-9]+): (.+)', industry_group.text)[0]
                    group_id = int(group_id + '0')

                    divisions[index]['major_groups'][major_group_id]['industry_groups'][group_id] = {}
                    divisions[index]['major_groups'][major_group_id]['industry_groups'][group_id]['name'] = group_name
                    divisions[index]['major_groups'][major_group_id]['industry_groups'][group_id]['industries'] = {}

                industries = div.find_all('tr')[1:]
                for industry in industries:
                    industry_id = int(industry.find_all('a')[0].text)
                    industry_name = industry.find_all('a')[1].text
                    industry_no_businesses = int(industry.find_all('td')[-1].text.replace(',', ''))
                    group_id = int(str(industry_id)[:-1] + '0')

                    divisions[index]['major_groups'][major_group_id]['industry_groups'][group_id]['industries'][industry_id] = {}
                    divisions[index]['major_groups'][major_group_id]['industry_groups'][group_id]['industries'][industry_id]['name'] = industry_name
                    divisions[index]['major_groups'][major_group_id]['industry_groups'][group_id]['industries'][industry_id]['no_businesses'] = industry_no_businesses
    
    for division_id in divisions.keys():
        for major_group_id in divisions[division_id]['major_groups'].keys():
            for group_id in divisions[division_id]['major_groups'][major_group_id]['industry_groups']:
                divisions[division_id]['major_groups'][major_group_id]['industry_groups'][group_id]['no_businesses'] = sum([
                    divisions[division_id]['major_groups'][major_group_id]['industry_groups'][group_id]['industries'][industry_id]['no_businesses']
                    for industry_id in 
                    divisions[division_id]['major_groups'][major_group_id]['industry_groups'][group_id]['industries'].keys()
                ])
    return divisions

def insert_sic_data(data, db_con) -> None:
    cur = db_con.cursor()
    for division_id in data.keys():
        cur.execute(
            "INSERT INTO sic_divisions VALUES (?, ?, ?, ?)",
            (
                division_id,
                data[division_id]['character'],
                data[division_id]['name'],
                data[division_id]['no_businesses']
            )
        )
        db_con.commit()
        for major_group_id in data[division_id]['major_groups'].keys():
            cur.execute(
                """
                INSERT INTO sic_industries(id, name, no_businesses, division_id)
                VALUES (?, ?, ?, ?)
                """,
                (
                    major_group_id,
                    data[division_id]['major_groups'][major_group_id]['name'],
                    data[division_id]['major_groups'][major_group_id]['no_businesses'],
                    division_id
                )
            )
            for group_id in data[division_id]['major_groups'][major_group_id]['industry_groups'].keys():
                cur.execute(
                    """
                    INSERT INTO sic_industries(id, name, no_businesses, major_group_id, division_id)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        group_id,
                        data[division_id]['major_groups'][major_group_id]['industry_groups'][group_id]['name'],
                        data[division_id]['major_groups'][major_group_id]['industry_groups'][group_id]['no_businesses'],
                        major_group_id,
                        division_id
                    )
                )
                for industry_id in data[division_id]['major_groups'][major_group_id]['industry_groups'][group_id]['industries'].keys():
                    cur.execute(
                        """
                        INSERT INTO sic_industries VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            industry_id,
                            data[division_id]['major_groups'][major_group_id]['industry_groups'][group_id]['industries'][industry_id]['name'],
                            data[division_id]['major_groups'][major_group_id]['industry_groups'][group_id]['industries'][industry_id]['no_businesses'],
                            group_id,
                            major_group_id,
                            division_id
                        )
                    )
    db_con.commit()

if __name__ == '__main__':
    db = Database()
    con = db.connection
    cur = db.cursor
    data = sic_list()
    insert_sic_data(data, con)
    con.commit()
    con.close()