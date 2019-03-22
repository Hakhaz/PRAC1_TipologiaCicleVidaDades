import requests
from bs4 import BeautifulSoup

def trade_spider(max_pages):
    page=1
    while page <= max_pages:
        url = 'https://www.instant-gaming.com/es/busquedas/?q=&page=' + str(page)
        print url
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('a', {'class': 'cover'}):
            href = link.get('href')
            title = link.string
        print(href)
        print(title)
        #get_single_item_data(href)
        page+=1

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for item_name in soup.findAll('h1'):
        print(item_name.string)
    #for item_price in soup.findAll('div', {'class':'prices'}):
        #print(item_price)

trade_spider(1)
#get_single_item_data('https://www.instant-gaming.com/es/2467-comprar-key-uplay-the-division-2/')