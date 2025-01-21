import requests
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook


def save_to_excel(data, filename):
    # Function to save extracted data to an Excel file
    wb = Workbook()
    ws = wb.active
    ws.append(["Satellite name", "Organisation", "Institution", "Entity type", "Manufacturer", "Operator"])  # Header row
    for item in data:
        ws.append(item)
    wb.save(filename)


if __name__ == '__main__':
    base_url = 'https://www.nanosats.eu/database'
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    links = []
    #print(soup.table)
    for link in soup.table.find_all('a'):
        links.append(link.get('href'))

    links_filtered = [ x for x in links if '.html' in x ]
    links_filtered = [ x for x in links_filtered if 'https://' not in x ]
    #print(links_filtered)
    dict = {}

    for sat_link in links_filtered:
        base_url = 'https://www.nanosats.eu/' + sat_link
        response_sat = requests.get(base_url)
        html_sat = response_sat.text
        soup_sat = BeautifulSoup(html_sat, "lxml")
        table_sat = soup_sat.find('table', id='table-company')
        print(table_sat)

        for row in table_sat.find_all('tr'):

            if row.find('th').get_text() == 'Spacecraft name' or row.find('th').get_text() == 'Spacecraft': #element in istitution exists or has another name
                dict.update({'Spacecraft name': table_sat.find('td').get_text()})
            
            if row.find('th').get_text() == 'Launcher': #element in istitution exists or has another name
                dict.update({'Launcher': table_sat.find('td').get_text()})
            
            if row.find('th').get_text() == 'Organisation': #element in istitution exists or has another name
                dict.update({'Organisation': table_sat.find('td').get_text()})
                
            if row.find('th').get_text() == 'Institution': #element in istitution exists or has another name
                dict.update({'Institution': table_sat.find('td').get_text()})

            if row.find('th').get_text() == 'Entity type': #element in istitution exists or has another name
                dict.update({'Entity type': table_sat.find('td').get_text()})

            if row.find('th').get_text() == 'Manufacturer': #element in istitution exists or has another name
                dict.update({'Manufacturer': table_sat.find('td').get_text()})

            
            
            
            
            

        
    table_to_excel = pd.DataFrame(dict)
    print(table_to_excel) 

