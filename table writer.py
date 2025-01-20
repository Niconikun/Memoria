import requests
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

def main():
    base_url = 'https://www.nanosats.eu/database'
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    #soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'table-wrapper nc'})  # Assuming table exists in the page
    # Extract data from the table and return relevant links
    headers = []
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            headers = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    save_to_excel(extracted_data, 'extracted_data.xlsx')

if __name__ == '__main__':
    main()

