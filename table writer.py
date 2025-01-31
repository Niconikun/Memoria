import requests
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

class Loader:
    def __init__(self, desc="Program started. Executing...", end="Links extracted from nanosats.eu/database and saved. Extracting data...", timeout=0.1):
        
        """ A loader-like context manager Args: 
        desc (str, optional): The loader's description. Defaults to "Loading...".
        end (str, optional): Final print. Defaults to "Done!".
        timeout (float, optional): Sleep time between prints. Defaults to 0.1. """

        self.desc = desc
        self.end = end
        self.timeout = timeout
        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False
    
    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)
    
    def __enter__(self):
        self.start()
    
    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)
        
    def __exit__(self, exc_type, exc_value, tb): # handle exceptions with those variables ^
        self.stop()


if __name__ == '__main__':
    
    with Loader("Program started. Executing..."):
        for i in range(10):
            sleep(0.25)
    
    base_url = 'https://www.nanosats.eu/database'
    headers_base = requests.utils.default_headers()
    headers_base.update(
        {
            'User-Agent': 'Niconikun 1.0'
        }
    )
    response = requests.get(base_url, headers=headers_base)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    links = []
    #print(soup.table)
    for link in soup.table.find_all('a'):
        links.append(link.get('href'))

    links_filtered = [ x for x in links if '.html' in x ]
    links_filtered = [ x for x in links_filtered if 'https://' not in x ]
    links_filtered = [ x for x in links_filtered if 'http://' not in x ]
    links_filtered = [ x for x in links_filtered if 'hiber.html' not in x ]
    links_filtered = [ x for x in links_filtered if 'sai-2.html' not in x ]
    links_filtered = [ x for x in links_filtered if 'ymir.html' not in x ]
    links_table = pd.DataFrame(links_filtered, columns=['Links']).to_excel("Linksnanosats.xlsx")#Save in dataframe and remove hiber links
    print(len(links_filtered))
    links_filtered = links_filtered[0:450]
    #print(links_filtered)
    #print(links_filtered)
    dict = {'Link': [], 'Satellite': [], 'Entity name': [], 'Institution': [], 'Entity type': [], 'Entity': [], 'Type': []}
    counter = 1
    for sat_link in links_filtered:
        loader = Loader(desc='Retrieving data from: ' + 'https://www.nanosats.eu/' + sat_link, end='Done! ' + str(counter) + ' out of ' + str(len(links_filtered)) + ' left.').start()
        base_url = 'https://www.nanosats.eu/' + sat_link
        headers_sat = requests.utils.default_headers()
        headers_sat.update(
            {
                'User-Agent': 'Niconikun 1.0'
            }
        )
        response_sat = requests.get(base_url, headers=headers_sat)
        
        html_sat = response_sat.text
        soup_sat = BeautifulSoup(html_sat, "lxml")
        table_sat = soup_sat.find('table', id='table-company')
        #print(table_sat)
        dict['Link'].append(sat_link)

        for category in ['Satellite', 'Entity name', 'Institution', 'Entity type', 'Entity', 'Type']: #do another for loop outside the row one, e the value of th iterates. thats how u solve the existence issue
            # add category Entity Name
            checker = 0
            for row in table_sat.find_all('tr'):
                #print(row)
                #print()

                #if row.find('th').get_text() == 'Spacecraft name' or row.find('th').get_text() == 'Spacecraft': #element in istitution exists or has another name
                 #   dict.update({'Spacecraft name': table_sat.find('td').get_text()})

                if row.find('th').text == category: #element in istitution exists or has another name
                    text = row.find('td').text.strip()
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
        counter +=1
        loader.stop()
        
        
    table_to_excel = pd.DataFrame(dict).to_excel("output.xlsx")
    #print(table_to_excel)
    #print()

