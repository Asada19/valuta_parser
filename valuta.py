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
for i in table.find_all('th'):
    title = i.text
    if title in ['USD', 'EURO', 'RUB', 'KZT']:
        headers.append(title)
        headers.append('')
    else:
        headers.append(title)


""" 
Колонка банков, цен покупок и продаж 
""" 
for i in soup.find_all('thead'):
    headers2 =[z.text for z in i.find_all('td')]


""" 
Список баков и цен на валюты 
"""
data =[]
for tr in table.find('tbody').find_all('tr'):
    dt = []
    for i in tr:
        dt.append(i.text)
    data.append(dt)
    

"""
Дата последнего обновления данных
"""
date = []
a = soup.find('span', class_='refresh').text
date.append(a)


""" Добавление двух заголовков и даты """
data.insert(0, headers2)
data.insert(0, headers)
data.append(date)


""" 
Запись данных в CSV 
"""
with open('valuta.csv', 'w') as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row)
