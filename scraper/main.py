from scraper import get_max_pages
from scraper import trade_spider
from scraper import df_to_csv
import pandas as pd


max_pages = get_max_pages()
df = pd.DataFrame()

df = trade_spider(max_pages)
df_to_csv(df)
