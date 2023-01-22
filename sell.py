from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sqlite3

conn = sqlite3.connect('database.db')
URL = input ('Input URL from Google Scholar: ')
HOST = 'https://scholar.google.com/'

articles = []

def chrome(url):
    chromedriver = 'C:\\PythonZ\\par\\chromedriver.exe'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=chromedriver, options=options)

    #driver = webdriver.Chrome()
    print('Opening the page...')
    driver.get(url)

    button = driver.find_element_by_id("gsc_bpf_more")

    #print (button.is_enabled())
    i = 1
    while button.is_enabled():
        time.sleep(3)
        button.click()
        time.sleep(3)
        print ('Extending the page (' + str(i) + ')...')
        i = i + 1

    html = driver.page_source
    driver.quit()
    return html

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='gsc_a_tr')

    for item in items:
        cited_by = item.find('a', class_='gsc_a_ac gs_ibl')
        if cited_by:
            cited_by = cited_by.get_text()
        else:
            cited_by = item.find('a', class_='gsc_a_ac gs_ibl gsc_a_acm')
            cited_by = cited_by.get_text() + '(merged)'

        articles.append({
            'TITLE': item.find('a', class_='gsc_a_at').get_text(),
            'AUTHORS': item.find('a', class_='gsc_a_at').find_next('div').get_text(),
            'JOURNAL': item.find('div', class_='gs_gray').find_next('div').get_text(),
            'CITED_BY': cited_by,
            'YEAR': item.find('span', class_='gsc_a_h gsc_a_hc gs_ibl').get_text(),
            'LINK': HOST + item.find('a', class_='gsc_a_at').get('data-href'),
        })


def parse():
    html = chrome(URL)
    get_content(html)

parse()
cursor = conn.cursor()
cursor.executemany('INSERT INTO citations VALUES(:TITLE, :AUTHORS, :JOURNAL, :CITED_BY, :YEAR, :LINK);', articles)
conn.commit()
print('The page was successfully inserted to database')
conn.close()