import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('database.db')

URL = input("Please, enter the URL of a person from Google scholar you want to parse "
            "(ex. https://scholar.google.com/citations?user=mfZtyl4AAAAJ&hl=en):\n")
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 'accept': '*/*'}
HOST = 'https://scholar.google.com/'
articles = []
def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='gsc_a_tr')

    
    for item in items:

        journal = item.find('div', class_='gs_gray').find_next('div')
        if journal:
            journal = journal.get_text()
        else:
            journal = 'no info'

        cited_by = item.find('a', class_='gsc_a_ac gs_ibl')
        if cited_by:
            cited_by = cited_by.get_text()
        else:
            cited_by = 'was not cited'

        articles.append({
            'TITLE': item.find('a', class_='gsc_a_at').get_text(),
            'AUTHORS': item.find('a', class_='gsc_a_at').find_next('div').get_text(),
            'JOURNAL': journal,
            'CITED_BY': cited_by,
            'YEAR': item.find('span', class_='gsc_a_h gsc_a_hc gs_ibl').get_text(),
            'LINK': HOST + item.find('a', class_='gsc_a_at').get('data-href'),
        })

    #return articles

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
        
    else:
        print('Error')
    
parse()
cursor = conn.cursor()
cursor.executemany('INSERT INTO citations VALUES(:TITLE, :AUTHORS, :JOURNAL, :CITED_BY, :YEAR, :LINK);', articles)
conn.commit()
conn.close()
