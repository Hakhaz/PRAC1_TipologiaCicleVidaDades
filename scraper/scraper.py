import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import datetime

def get_max_pages():
    url = 'https://www.instant-gaming.com/es/busquedas/?q=&page=1'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'lxml')
    pagination = soup.find('ul', {'class':'pagination bottom'})
    pageMax = 1
    for pages in pagination.findAll('li'):
        try:
            page=int(pages.string)
        except ValueError:
            page=-1
        if page > pageMax:
            pageMax = page
    return(pageMax)

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

def trade_spider(max_pages):
    print('Start scraper. Total pages:',max_pages)
    page=1
    df = pd.DataFrame()
    while page <= max_pages:
        url = 'https://www.instant-gaming.com/es/busquedas/?q=&page=' + str(page)
        print('Start scraper page',page)

        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,'lxml')
        for link in soup.findAll('a', {'class': 'cover'}):
            href = link.get('href')
            

            if link.parent.get('data-dlc') == '0':
                category = 'GAME'
            elif link.parent.get('data-dlc') == '1':
                category = 'DLC'
            else:
                category = 'UNKNOWN'
                
            
            data = get_single_item_data(href)
            data.append(category)
            
            now = datetime.datetime.now()
            day = now.strftime("%d")
            month = switch_month(now.strftime("%B"))
            year = now.strftime("%Y")
            dateExtraction = day + " " + month + " " + year
            data.append(dateExtraction)


            df = df.append(pd.DataFrame([data]),ignore_index=True)
        print('End scraper page',page)
        page+=1
    print('End scraper')
    return (df)

def df_to_csv(df):
    columns = ['name','platform','original_price(€)','discounted_price(€)','discount(%)','release_date','users_rating','category','extraction_date']   
    now = datetime.datetime.now()
    fileName = 'GamesDataPrices_'+now.strftime("%Y%m%d_%H%M")+'.csv'
    print('File "' + fileName + '" generated.')
    df.to_csv(fileName, sep=',', header=columns)
    
    
def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'lxml')
    
    title = soup.find('div',{'class':'title'}).h1.get_text()
    platform = soup.find('div',{'class':'subinfos'}).a.get_text()
    
    item_prices = soup.find('div', {'class':'prices'})      
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

    data = [title,platform,retail,price,discount,release_date,users_rating]
    return (data)



