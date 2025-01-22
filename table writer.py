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
    links_filtered = links_filtered[0:10]
    print(links_filtered)
    #print(links_filtered)
    dict = {'Spacecraft name': [], 'Spacecraft': [], 'Name': [], 'Launcher': [], 'Organisation': [], 'Institution': [], 'Entity type': [], 'Entity': [], 'Manufacturer': []}
    counter = 0
    for sat_link in links_filtered:
        base_url = 'https://www.nanosats.eu/' + sat_link
        response_sat = requests.get(base_url)
        html_sat = response_sat.text
        soup_sat = BeautifulSoup(html_sat, "lxml")
        table_sat = soup_sat.find('table', id='table-company')
        #print(table_sat)

        for category in ['Spacecraft name', 'Spacecraft', 'Name', 'Launcher', 'Organisation', 'Institution', 'Entity type', 'Entity', 'Manufacturer']: #do another for loop outside the row one, where the value of th iterates. thats how u solve the existence issue
            checker = 0
            for row in table_sat.find_all('tr'):
                #print(row)
                #print()

                #if row.find('th').get_text() == 'Spacecraft name' or row.find('th').get_text() == 'Spacecraft': #element in istitution exists or has another name
                 #   dict.update({'Spacecraft name': table_sat.find('td').get_text()})

                if row.find('th').text == category: #element in istitution exists or has another name
                    text = row.find('td').renderContents()
                    #print ('The word is: ', text)
                    #print()
                    dict[category].append(text)
                    #dict.update({category: row.find('td').renderContents() })
                    checker = 1
            if checker == 0:
                dict[category].append('None')
                #print(dict)
                #print()
        #print(counter)
        #counter +=1
        
        
    table_to_excel = pd.DataFrame(dict).to_excel("output.xlsx")
    #print(table_to_excel)
    #print()

