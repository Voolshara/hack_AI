import pandas as pd
import requests
import urllib.parse
import csv
from bs4 import BeautifulSoup
"""
На вход словарь вида
{
'stolbec' : ['data1', data2, 'data3'],
'stolbec2' : ...
}
"""
def Write(data):
    data = pd.DataFrame(data)
    data.to_excel('./output_excel.xlsx', sheet_name='Просьбы жителей по благоустр-ву', index=False)

def Reading(file_name):
    data = pd.read_excel('./' + file_name)
    return data.values
data = Reading('1.xlsx')





data = [('улица', 'дом', 'дата', 'обращение')]
for i in range(1, 159):
    url = 'http://www.jkh.insoc.ru/page/fdb?stype=0&status=6&pg_fdb=' + str(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_='BoxItem')


    for quote in quotes:
        s = quote.text.split("\n")
        k = (s[6])[16:]
        data.append((k[k.find(' ') + 5:k.rfind(' ') - 1], ((s[6])[s[6].rfind(' ') + 3:]), (s[2])[2:-1], (s[8])[2:-1]))












myData = [["Адрес обращения", "Дом", "Дата", "Текст обращения", "Координаты"]]
output = {'Адрес обращения':[], 'Дом':[], 'Дата':[], 'Текст обращения':[], 'Координаты':[]}
for i in range(1, len(data)):
    a = data[i]
    if len(a[3]) < 2:
        continue
    elif a[1] == 'ё':
        a[1] = 1
    elif a[3].lower() == 'пустой' or a[3].lower() == 'пустой.' or a[3].lower() == 'иное':
        continue
    else:
        if len(a[1].split()) > 2:
            a[1] = a[1].split()
            a[1][1] = '/'
            a[1] = ''.join(a[1])
        try:
            adress = "Чебоксары+" + '+'.join(a[0].split(' ')) + '+' + a[1]  # город+улица+дом
            adress = urllib.parse.quote_plus(adress)
            req = "https://nominatim.openstreetmap.org/?addressdetails=1&q={}&format=json&limit=1".format(adress)
            req = requests.get(req).json()
            req = req[0]
            coords=req['lat'] + ' ' + req['lon']
        except Exception:
            try:
                adress = "Чебоксары+" + '+'.join(a[0].split(' ')[1:]) + '+' + a[1]  # город+улица+дом
                adress = urllib.parse.quote_plus(adress)
                req = "https://nominatim.openstreetmap.org/?addressdetails=1&q={}&format=json&limit=1".format(adress)
                req = requests.get(req).json()
                req = req[0]
                coords = req['lat'] + ' ' + req['lon']
            except Exception:
                try:
                    adress = "Новочебоксарск+" + '+'.join(a[0].split(' ')[1:]) + '+' + a[1]  # город+улица+дом
                    adress = urllib.parse.quote_plus(adress)
                    req = "https://nominatim.openstreetmap.org/?addressdetails=1&q={}&format=json&limit=1".format(adress)
                    req = requests.get(req).json()
                    req = req[0]
                    coords = req['lat'] + ' ' + req['lon']
                except Exception:
                    coords = 'NONE'
        output['Адрес обращения'].append(a[0])
        output['Дом'].append(a[1])
        output['Дата'].append(str(a[2]))
        output['Текст обращения'].append(a[3])
        output['Координаты'].append(coords)
        myData.append([a[0], a[1], str(a[2]), str(a[3]), coords])
        print((i / len(data)) * 100)
Write(output)
myFile = open('output_csv.csv', 'w', newline="")
with myFile:
    writer = csv.writer(myFile, delimiter=';', lineterminator="\n")
    writer.writerows(myData)
