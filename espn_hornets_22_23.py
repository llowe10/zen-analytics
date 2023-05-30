#### Author:       Lantz Lowe
#### Updated:      May 29, 2023

from bs4 import BeautifulSoup as soap
from bs4 import SoupStrainer as strain
import requests
import pandas as pd
import numpy as np


site = 'https://www.espn.com/nba/team/stats/_/name/cha'

result = requests.get(site)
src = result.content
soup = soap(src,'html.parser')

################        Find table in html: ordered by PTS descending       ################
table = soup.find(name='table',attrs={'class':'Table Table--align-right Table--fixed Table--fixed-left'})

################        Turn table into pandas DataFrame        ################
players = pd.DataFrame([[td.text for td in row.findAll('td')] for row in table.tbody.findAll('tr')])
players = players.rename(columns={0:"NAME/POS"})

table_stats = soup.find(name='table',attrs={'class':'Table Table--align-right'})

### get table columns
# cols = [[th.text for th in col.findAll('th')] for col in table_stats.thead.findAll('tr')]
cols = {}
ind = 0
for col in table_stats.thead.findAll('tr'):
    for th in col.findAll('th'):
        cols[ind] = th.text
        ind += 1
print(cols)

### get table data
stats = pd.DataFrame([[td.text for td in row.findAll('td')] for row in table_stats.tbody.findAll('tr')])
stats = stats.rename(columns=cols)
#stats.index = ['ROZIER','HAYWARD','BALL','GRAHAM','WASHINGTON','BRIDGES','MONK','ZELLER','MCDANIELS','WANAMAKER','BIYOMBO','CA.MARTIN','CO.MARTIN','RILLER','CAREYJR.','DARLING','RICHARDS','TOTAL']
stats = pd.merge(players, stats, left_index=True, right_index=True) # Merge player names and stats based on table indices
# for each index, set index equal to last name in all caps

################        Convert certain columns to numeric      ################
# stats["GP"] = pd.to_numeric(stats["GP"])
# stats["GS"] = pd.to_numeric(stats["GS"])
# stats["MIN"] = pd.to_numeric(stats["MIN"])
# stats["PTS"] = pd.to_numeric(stats["PTS"])
# stats["OREB"] = pd.to_numeric(stats["OREB"])
# stats["DREB"] = pd.to_numeric(stats["DREB"])
# stats["REB"] = pd.to_numeric(stats["REB"])
# stats["AST"] = pd.to_numeric(stats["AST"])
# stats["STL"] = pd.to_numeric(stats["STL"])
# stats["BLK"] = pd.to_numeric(stats["BLK"])
# stats["TO"] = pd.to_numeric(stats["TO"])
# stats["FOULS"] = pd.to_numeric(stats["FOULS"])
# stats["AST/TO"] = pd.to_numeric(stats["AST/TO"])

### Print ENTIRE DataFrame
print("\n*** ALL STATS FOR ALL PLAYERS ***")
print(stats)