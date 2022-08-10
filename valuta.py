import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.akchabar.kg/ru/exchange-rates/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
table = soup.find('table', id='rates_table')


"""
Заголовок курсов валют
"""
headers = []

def head(headers: list, table):
    for i in table.find_all('th'):
        title = i.text
        if title in ['USD', 'EURO', 'RUB', 'KZT']:
            headers.append(title)
            headers.append('')
        else:
            headers.append(title)

head(headers, table)


""" 
Колонка банков, цен покупок и продаж 
""" 
def column(soup):
    for i in soup.find_all('thead'):
        headers2 =[z.text for z in i.find_all('td')]
    return headers2 

headers2 = column(soup)


""" 
Список баков и цен на валюты 
"""
data =[]
def update_data(data: list):
    for tr in table.find('tbody').find_all('tr'):
        dt = []
        for i in tr:
            dt.append(i.text)
        data.append(dt)
    
update_data(data)


"""
Дата последнего обновления данных
"""
date = []
def add_date(date: list, soup):
    a = soup.find('span', class_='refresh').text
    date.append(a)


add_date(date, soup)


""" 
Добавление двух заголовков и даты 
"""
def add_columns(data: list):
    data.insert(0, headers2)
    data.insert(0, headers)
    data.append(date)

add_columns(data)


""" 
Запись данных в CSV 
"""
def write_to_csv(data):
    with open('valuta.csv', 'w') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

write_to_csv(data)