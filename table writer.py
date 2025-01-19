import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

def get_table_data(url):
    # Function to fetch table data from a given URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')  # Assuming table exists in the page
    # Extract data from the table and return relevant links

def extract_information(link):
    # Function to extract "institution", "provider", "manufacturer" from a linked page
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract institution, provider, and manufacturer information from the page

def save_to_excel(data, filename):
    # Function to save extracted data to an Excel file
    wb = Workbook()
    ws = wb.active
    ws.append(["Satellite name", "Organisation", "Institution", "Entity type", "Manufacturer", "Operator"])  # Header row
    for item in data:
        ws.append(item)
    wb.save(filename)

def main():
    base_url = 'http://https://www.nanosats.eu/database'  # Replace with your base URL
    # Example URLs or logic to iterate through pages
    urls = [f'{base_url}/page1', f'{base_url}/page2', ...]
    extracted_data = []

    for url in urls:
        table_data = get_table_data(url)
        for row in table_data:
            link = row['link']  # Assuming 'link' is the key for the URL in the row data
            satellitename, organisation, institution, entitytype, manufacturer, operator = extract_information(link)
            extracted_data.append([satellitename, organisation, institution, entitytype, manufacturer, operator])

    save_to_excel(extracted_data, 'extracted_data.xlsx')

if __name__ == '__main__':
    main()
