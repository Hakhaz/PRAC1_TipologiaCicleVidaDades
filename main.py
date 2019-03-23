import requests
from bs4 import BeautifulSoup
import csv

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
            category = link.parent.get('data-dlc') #0 = jocs, 1 = dlc
            print('category: {}'.format(category))
            get_single_item_data(href)
        page+=1

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    
    title = soup.find('div',{'class':'title'}).h1.get_text()
    print(title)
    #platform = soup.find('div',{'class':'subinfos'}).a.get('class')
    platform = soup.find('div',{'class':'subinfos'}).a.get_text()
    print(platform)
    
    #alternativa sense bucle, ja es buscaran els DLCs quan els hi toqui
    item_prices = soup.find('div', {'class':'prices'})      
    #for item_prices in soup.findAll('div', {'class':'prices'}):
    try:
        retail = item_prices.find('span').string
    except:
        retail = ''
    price = item_prices.find('div',{'class':'price'}).string
    
    try:
        discount = item_prices.find('div',{'class':'discount'}).string
    except:
        discount = ''
    print(retail)
    print(price)
    print(discount)
       
       
    release_date = soup.find('div', {'class':'release'})
    print(release_date.string)
    
    users_rating = soup.find('div', {'class':'productreviews'}).contents[1].span.get_text()
    print(users_rating)
    
    data = [title, platform]
    writer.writerow(data)
    
    #for item_name in soup.findAll('div', {'class':'stars'}):        
    #    print(item_name)

#Exemple per a probar l'escriptura al csv de la primera pàgina
with open('data.csv', 'w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',')
    trade_spider(1)
#get_single_item_data('https://www.instant-gaming.com/es/2467-comprar-key-uplay-the-division-2/')
#get_single_item_data('https://www.instant-gaming.com/es/186-comprar-key-rockstar-grand-theft-auto-v/')

#Exemple per a probar l'escriptura al csv de únicament tres jocs
with open('data.csv', 'w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',')
    get_single_item_data('https://www.instant-gaming.com/es/2467-comprar-key-uplay-the-division-2/')
    get_single_item_data('https://www.instant-gaming.com/es/186-comprar-key-rockstar-grand-theft-auto-v/')
    get_single_item_data('https://www.instant-gaming.com/es/3979-comprar-key-origin-apex-legends-2150-apex-coins/')
