#### Author:       Lantz Lowe
#### Updated:      May 29, 2023

from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as strain
import requests
import pandas as pd
import numpy as np


# site = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
site = 'https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats#all_stats_standard'

result = requests.get(site)
src = result.content
soup = bs(src,'html.parser')

################        Find table in html: ordered by PTS descending       ################
table = soup.find(name='table',id='stats_standard_9')

################        Turn table into pandas DataFrame        ################
stats = pd.DataFrame([[td.text for td in row.findAll('td')] for row in table.tbody.findAll('tr')])

### get player names
names = []
for row in table.tbody.findAll('tr'):
    for name in row.find('th'):
        names.append(name.text)
players = pd.DataFrame(names)
stats = pd.merge(players, stats, left_index=True, right_index=True) # Merge player names and stats based on table indices

### get table columns
cols = []
for col in table.thead.findAll('tr'):
    for th in col.findAll('th'):
        if th.text == '': # skip column groups
            cols.clear()
            continue
        cols.append(th.text)
stats.columns = cols
try:
    stats = stats.drop(['Matches'],axis=1)
except:
    print("error removing matches column...")

### Print ENTIRE DataFrame
print("\n*** ALL STATS FOR ALL PLAYERS ***")
print(stats)

stats.to_csv('man_city.csv')