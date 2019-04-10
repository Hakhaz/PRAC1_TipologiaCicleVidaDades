from scraper import get_max_pages
from scraper import trade_spider
from scraper import df_to_csv
import pandas as pd

#Primer s'obtè el nombre màxim de pàgines que s'ha de recòrrrer
max_pages = get_max_pages()
#Es crea el dataframe
df = pd.DataFrame()
#Es truca a la funció trade_spider per obtenir el dataframe que contè tota la informació
df = trade_spider(max_pages)
#Es truca a la funció df_to_csv per guardar la informació del dataframe en un arxiu csv
df_to_csv(df)
