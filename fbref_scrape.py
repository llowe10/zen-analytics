#### Author:       Lantz Lowe
#### Updated:      May 29, 2023

import os
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as strain
import requests
import pandas as pd
import numpy as np
import openpyxl


def get_player_stats(site, table_id, file_name):
    # site = 'https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats#all_stats_standard'
    # site = 'https://fbref.com/en/squads/b8fd03ef/2022-2023/all_comps/Manchester-City-Stats-All-Competitions'

    result = requests.get(site)
    src = result.content
    soup = bs(src,'html.parser')

    ################        Find table in html: ordered by PTS descending       ################
    # table = soup.find(name='table',id='stats_standard_9')
    # table = soup.find(name='table',id='stats_standard_combined')
    table = soup.find(name='table',id=table_id)

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
    print(cols)
    stats.columns = cols
    try:
        stats = stats.drop(['Matches'],axis=1)
    except:
        print("error removing matches column...")

    ### export data
    print("\n*** exporting data to csv ***")
    # print(stats)
    # stats.to_csv('C:/Users/lantz/Documents/My Tableau Repository/Datasources/man_city.csv')
    stats.to_csv('C:/Users/lantz/Documents/My Tableau Repository/Datasources/' + file_name)

def get_squad_stats(site, table_id, file_name, season):
    path = 'C:/Users/lantz/Documents/My Tableau Repository/Datasources/' + file_name + '.xlsx'
    result = requests.get(site)
    src = result.content
    soup = bs(src,'html.parser')
    table = soup.find(name='table',id=table_id)

    ### create initial pandas dataframe
    squads = pd.DataFrame([[th.text for th in row.findAll('th')] for row in table.tbody.findAll('tr')])
    stats = pd.DataFrame([[td.text for td in row.findAll('td')] for row in table.tbody.findAll('tr')])
    stats_pd = pd.merge(squads, stats, left_index=True, right_index=True) # Merge squads and stats

    ### get table columns
    cols = []
    for col in table.thead.findAll('tr'):
        for th in col.findAll('th'):
            if th.text == '': # skip column groups
                cols.clear()
                continue
            cols.append(th.text)

    ### remove group columns
    diff = len(cols) - len(stats_pd.columns)
    if diff > 0:
        cols = cols[diff:]

    # print(cols)
    stats_pd.columns = cols
    stats_pd.insert(1, 'Season', season)

    ### export data
    # print(stats_pd)
    if os.path.isfile(path):
        print("\nexporting {0} data to {1}...".format(season, file_name))
        with pd.ExcelWriter(path, mode='a', if_sheet_exists="overlay") as writer:  
            stats_pd.to_excel(writer, sheet_name='Sheet1', startrow=writer.sheets["Sheet1"].max_row, index=False, header=False)
    else:
        print("\ncreating {1} with {0} data...".format(season, file_name))
        stats_pd.to_excel(path, index=False, header=True)
    print("...export completed.")

if __name__ == "__main__":
    # get_player_stats('https://fbref.com/en/squads/b8fd03ef/2022-2023/all_comps/Manchester-City-Stats-All-Competitions','stats_standard_combined','man_city.csv')
    get_squad_stats('https://fbref.com/en/comps/9/gca/Premier-League-Stats','stats_squads_gca_for','prem_squad_goal_shot_creation','2022-23')
    get_squad_stats('https://fbref.com/en/comps/9/2021-2022/gca/2021-2022-Premier-League-Stats','stats_squads_gca_for','prem_squad_goal_shot_creation','2021-22')
    get_squad_stats('https://fbref.com/en/comps/9/2020-2021/gca/2020-2021-Premier-League-Stats','stats_squads_gca_for','prem_squad_goal_shot_creation','2020-21')