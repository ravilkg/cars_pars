import requests
from bs4 import BeautifulSoup
import csv

#План:
#1. количество страниц
#2. количество уролов на странице выдачи
#3. собрать данные

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_ = 'pagination-pages').find_all('a', class_ = 'pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]

    return int(total_pages)

def write_csv(data):
    with open('avito_csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['title'],
                          data['price'],
                          data['desc'],
                          data['url']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_ = 'catalog-list').find_all('div', class_ = 'item_table')

    for ad in ads:
        #title, url, price, descprition
        try:
            title = ad.find('div', class_ = 'description').find('h3').text.strip()
        except:
            title = ''

        try:
            price = ad.find('div', class_='about').text.split('\n')[1].strip()
        except:
            price = ''

        try:
            desc = ad.find('span', class_='params').text.strip()
        except:
            desc = ''

        try:
            url = 'https://www.avito.ru' + ad.find('div', class_='description').find('a').get('href')
        except:
            url = ''

        data = {'title':title,
                'price':price,
                'desc':desc,
                'url':url}

        write_csv(data)

def main():
    url = 'https://www.avito.ru/rossiya/avtomobili?p=2&q=bmw+x3'
    base_url = 'https://www.avito.ru/rossiya/avtomobili?'
    page_part = 'p='
    query_part = '&q=bmw+x3'

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)




if __name__ == '__main__':
    main()