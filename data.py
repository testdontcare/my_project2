import pandas as pd
#import urllib request import urlopen
import json

df = pd.read_csv('https://raw.githubusercontent.com/ThuwarakeshM/geting-started-with-plottly-dash/main/life_expectancy.csv',
                sep=',')
all_cont = df['continent'].unique()

df_region = pd.read_csv('data/region_eco_2022.csv',
                sep=',', decimal=',', )

with open('data/russia copy.geojson','r',encoding='UTF-8') as response:
        counties = json.loads(response.read())
