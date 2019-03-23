import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def trade_spider(max_pages):
    page=1    
    df = pd.DataFrame()
    #columns = ['name','platform','original_price','price','discount','release_data','users_rating','category']
    while page <= max_pages:
        url = 'https://www.instant-gaming.com/es/busquedas/?q=&page=' + str(page)
        print (url)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text) #Em mostra aquesta línia per pantalla, no entenc el perquè, o si es normal o no
        for link in soup.findAll('a', {'class': 'cover'}):
            href = link.get('href')
            print(href)
            category = link.parent.get('data-dlc') #0 = jocs, 1 = dlc
            #print('category: {}'.format(category))
            
            data = get_single_item_data(href)
            data.append(category)
            print(data)

            df = df.append(pd.DataFrame([data]),ignore_index=True) #amb [[data]] ho posa com una fila. Poc elegant pero funciona.
        page+=1
        
        df.to_csv('data.csv', sep=',')

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    
    title = soup.find('div',{'class':'title'}).h1.get_text()
    platform = soup.find('div',{'class':'subinfos'}).a.get_text()
    #print(title)
    #print(platform)
    
    item_prices = soup.find('div', {'class':'prices'})      
    try:
        retail = item_prices.find('span').string
    except:
        retail = ''
    price = item_prices.find('div',{'class':'price'}).string
    
    try:
        discount = item_prices.find('div',{'class':'discount'}).string
    except:
        discount = ''
    #print(retail)
    #print(price)
    #print(discount)       
       
    release_date = soup.find('div', {'class':'release'}).contents[3].get_text()
    users_rating = soup.find('div', {'class':'productreviews'}).contents[1].span.get_text()
    #print(release_date)
    #print(users_rating)
    
    #data = [title, platform]
    #writer.writerow(data)
    
    data = [title,platform,retail,price,discount,release_date,users_rating]
    return (data)
    
#Exemple per a probar l'escriptura al csv de la primera pàgina
#with open('data.csv', 'w') as csvFile:
#    writer = csv.writer(csvFile, delimiter=',')
trade_spider(1)
#get_single_item_data('https://www.instant-gaming.com/es/2467-comprar-key-uplay-the-division-2/')
#get_single_item_data('https://www.instant-gaming.com/es/186-comprar-key-rockstar-grand-theft-auto-v/')

#Exemple per a probar l'escriptura al csv de únicament tres jocs
#with open('data.csv', 'w') as csvFile:
#    writer = csv.writer(csvFile, delimiter=',')
#    get_single_item_data('https://www.instant-gaming.com/es/2467-comprar-key-uplay-the-division-2/')
#    get_single_item_data('https://www.instant-gaming.com/es/186-comprar-key-rockstar-grand-theft-auto-v/')
#    get_single_item_data('https://www.instant-gaming.com/es/3979-comprar-key-origin-apex-legends-2150-apex-coins/')
