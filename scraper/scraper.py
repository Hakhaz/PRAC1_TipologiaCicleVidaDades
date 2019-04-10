import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import datetime

'''Mitjançant aquesta funció obtenim el màxim nombre de pàgines que necessitem recòrrer
per obtenir la informació de tots els jocs de la pàgina web'''
def get_max_pages():
    url = 'https://www.instant-gaming.com/es/busquedas/?q=&page=1'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'lxml')
    pagination = soup.find('ul', {'class':'pagination bottom'})
    pageMax = 1
    '''En cas d'error, degut a que nomès hi hauría una pàgina, assignem el valor -1, i posteriorment
    assignariem a la variable pageMax el valor 1'''
    for pages in pagination.findAll('li'):
        try:
            page=int(pages.string)
        except ValueError:
            page=-1
        if page > pageMax:
            pageMax = page
    return(pageMax)

'''En aquesta funció creem un diccionari per, posteriorment,
a partir del mes obtingut de la system date, convertir aquest valor que es troba en anglès al castellà, 
per tal de mantenir el mateix format en totes les dates del nostre dataset.'''
def switch_month(month):
    switcherMonth = {
        "January": "enero",
        "February": "febrero",
        "March":"marzo",
        "April":"abril",
        "May":"mayo",
        "June":"junio",
        "July":"julio",
        "August":"agosto",
        "September":"septiembre",
        "October":"octubre",
        "November":"noviembre",
        "December":"diciembre"
    }
    return(switcherMonth.get(month, "None"))

#Aquesta funció inicia el scraper.
def trade_spider(max_pages):
    print('Start scraper. Total pages:',max_pages)
    page=1
    #Assignem un User-Agent
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    #Definim el dataframe on anirem guardant els valors recollits
    df = pd.DataFrame()
    #En aquest bucle anirem recorrent cada pàgina
    while page <= max_pages:
        url = 'https://www.instant-gaming.com/es/busquedas/?q=&page=' + str(page)
        print('Start scraper page',page)

        source_code = requests.get(url,headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,'lxml')
        #En aquest bucle entrarem a cada joc que es troba a la pàgina que estem recorrent en cada moment.
        for link in soup.findAll('a', {'class': 'cover'}):
            href = link.get('href')
            
            if link.parent.get('data-dlc') == '0':
                category = 'GAME'
            elif link.parent.get('data-dlc') == '1':
                category = 'DLC'
            else:
                category = 'UNKNOWN'
                
            #Truquem a la funció get_single_item_data() per recuperar la informació de cada joc de la pàgina que estem recorrent en cada moment.
            data = get_single_item_data(href)
            data.append(category)
            
            '''S'obtè la data actual, el dia, mes i any per separat.
            trucant a la funció switch¨_month() transformem el mes de l'anglès al castellà i,
            finalment, li donem el format corrresponent a la data.'''
            now = datetime.datetime.now()
            day = now.strftime("%d")
            month = switch_month(now.strftime("%B"))
            year = now.strftime("%Y")
            dateExtraction = day + " " + month + " " + year
            data.append(dateExtraction)

            #Afegim al dataframe la informació recollida de cada joc per posteriorment passar aquesta informació a un arxiu csv.
            df = df.append(pd.DataFrame([data]),ignore_index=True)
        print('End scraper page',page)
        page+=1
    print('End scraper')
    return (df)

'''Aquesta funció ens genera l'arxiu csv amb la informació de cada joc recollida i guardada al dataframe obtingut de la funció trade_spider().
Se li assignen els noms de les columnes del dataset tambè'''
def df_to_csv(df):
    columns = ['name','platform','original_price(€)','discounted_price(€)','discount(%)','release_date','users_rating','category','extraction_date']   
    now = datetime.datetime.now()
    fileName = 'GamesDataPrices_'+now.strftime("%Y%m%d_%H%M")+'.csv'
    print('File "' + fileName + '" generated.')
    df.to_csv(fileName, sep=',', header=columns)
    
#Aquesta funció obtè tota la informació dels diferents jocs, a partir de la url de cada joc.    
def get_single_item_data(item_url):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    source_code = requests.get(item_url, headers=headers)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'lxml')
    
    title = soup.find('div',{'class':'title'}).h1.get_text()
    platform = soup.find('div',{'class':'subinfos'}).a.get_text()
    
    item_prices = soup.find('div', {'class':'prices'})
    
    '''En les variables de retail, price i discount, el·liminem l'ultim caràcter, ja que sería el simbol de la moneda, per guardar únicament el valor.
    En el cas de donar un error a l'hora de recuperar el valor, ja que no es trobaría aquest camp a l'estructura de la pàgina web, li assignariem un valor buit
    a la variable.'''
    try:
        retail = item_prices.find('span').string
        retail = retail[:-1]
    except:
        retail = ''
    
    price = item_prices.find('div',{'class':'price'}).string
    price = price[:-1]
    
    try:
        discount = item_prices.find('div',{'class':'discount'}).string
        discount = discount[1:-1]
    except:
        discount = ''
     
       
    release_date = soup.find('div', {'class':'release'}).contents[3].get_text()
    users_rating = soup.find('div', {'class':'productreviews'}).contents[1].span.get_text()
    
    #Guardem tota la informació del joc per posteriorment guardar la variable data al dataframe.
    data = [title,platform,retail,price,discount,release_date,users_rating]
    return (data)
