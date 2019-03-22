import requests
from bs4 import BeautifulSoup

def trade_spider(max_pages):
    page=1
    while page <= max_pages:
        url = 'https://www.instant-gaming.com/es/busquedas/?q=&page=' + str(page)
        print (url)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text) #Em mostra aquesta línia per pantalla, no entenc el perquè, o si es normal o no
        for link in soup.findAll('a', {'class': 'cover'}):
            href = link.get('href')
            #title = link.string
            print(href)
            #print(title)
            get_single_item_data(href)
        page+=1

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    
    title = soup.find('div',{'class':'title'}).h1
    print(title.string)
    platform = soup.find('div',{'class':'subinfos'}).a.get('class')
    print(platform)
    
    #alternativa sense bucle, ja es buscaran els DLCs quan els hi toqui
    #item_prices = soup.find('div', {'class':'prices'})      
    for item_prices in soup.findAll('div', {'class':'prices'}):
        retail = item_prices.find('span')
        price = item_prices.find('div',{'class':'price'})
        discount = item_prices.find('div',{'class':'discount'})
        print(retail.string)
        print(price.string)
        print(discount.string)
        
       
    release = soup.find('div', {'class':'release'}).span
    print(release.string)
        
    #for item_name in soup.findAll('div', {'class':'stars'}):        
    #    print(item_name)


#trade_spider(1)
#get_single_item_data('https://www.instant-gaming.com/es/2467-comprar-key-uplay-the-division-2/')
get_single_item_data('https://www.instant-gaming.com/es/186-comprar-key-rockstar-grand-theft-auto-v/')
