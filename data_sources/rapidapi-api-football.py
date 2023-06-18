import requests  # pip install requests
import pandas as pd  # pip install pandas
import numpy as np
import json
import os

#######################################################################################################################################

root_endpoint = "https://api-football-v1.p.rapidapi.com/v3"

available_seasons = ['1966', '1972', '1980', '1982', '1986', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

team_map = {
    "Manchester City": 50
}

league_map = {
    "UEFA Champions League": 2,
    "La Liga": 140,
    "Premier League": 39
}

player_map = {
    "E. Haaland": 1100
}

headers = {
    "X-RapidAPI-Key": "fdcd0a1831msh855607adde1935cp19bd72jsn07dca62515d5",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
}

#######################################################################################################################################

def get_available_player_seasons():
    seasons = []
    url = root_endpoint + "/players/seasons"
    response = requests.get(url, headers=headers)
    for season in response.json()["response"]:
        seasons.append(str(season))
    return seasons

def get_current_team_squad(team_id):
    url = root_endpoint + "/players/squads"
    querystring = {"team":team_id}
    response = requests.request("GET", url, headers=headers, params=querystring)

    players = {}

    for player in response.json()["response"][0]["players"]:
        players[player["name"]] = player["id"]

    return players

def get_team_statistics(league_id, season, team_id):
    url = root_endpoint + "/teams/statistics"

    querystring = {"league": league_id, "season": season, "team": team_id}

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = {
        "season": [ season, season, season ],
        "wins": [
            response.json()["response"]["fixtures"]["wins"]["home"],
            response.json()["response"]["fixtures"]["wins"]["away"],
            response.json()["response"]["fixtures"]["wins"]["total"],
        ],
        "played": [
            response.json()["response"]["fixtures"]["played"]["home"],
            response.json()["response"]["fixtures"]["played"]["away"],
            response.json()["response"]["fixtures"]["played"]["total"],
        ]
    }
    df = pd.DataFrame(data, index=["home", "away", "total"])

    print(df)

    # f = open("stats_" + season + "_" + team_id + ".json", "w")
    # f.write(response.text)
    # f.close()

    # return response.json()["response"]

def get_player_statistics(id, season):
    # path = 'C:/Users/lantz/Documents/My Tableau Repository/Datasources/rapidapi-playerstats-player' + str(id) + '-' + season + '.xlsx'
    path = 'C:/Users/lantz/Documents/My Tableau Repository/Datasources/rapidapi-career-playerstats-' + str(id) + '.xlsx'
    url = root_endpoint + "/players"
    querystring = {"id":id, "season":season}
    response = requests.request("GET", url, headers=headers, params=querystring)

    ### set columns ###
    cols = ['player_name', 'player_firstname', 'player_lastname']
    for key in response.json()['response'][0]["statistics"][0].keys():
        for subkey in response.json()['response'][0]["statistics"][0][key]:
            cols.append(key+'_'+subkey)
    stats_pd = pd.DataFrame(columns=cols)

    ### get stat values ###
    # for player in response.json()['response']:
    row = {'player_name': response.json()['response'][0]["player"]["name"], 'player_firstname': response.json()['response'][0]["player"]["firstname"], 'player_lastname': response.json()['response'][0]["player"]["lastname"]}
    for competition in response.json()['response'][0]["statistics"]:
        for stat_name, stat_dict in competition.items():
            for stat, val in stat_dict.items():
                row[stat_name+'_'+stat] = val
        stats_pd.loc[len(stats_pd)] = row
    
    stats_pd.fillna(value=0, inplace=True) # replace None of NaN in same DataFrame

    print(stats_pd)

    ### export data
    if os.path.isfile(path):
        print("\nadding {0} data for {1} season...".format(id, season))
        with pd.ExcelWriter(path, mode='a', if_sheet_exists="overlay") as writer:  
            stats_pd.to_excel(writer, sheet_name='Sheet1', startrow=writer.sheets["Sheet1"].max_row, index=False, header=False)
    else:
        print("\ncreating {0} data file with {1} season...".format(id, season))
        stats_pd.to_excel(path, index=False, header=True)
    print("...export completed.")

def get_player_statistics_by_team(team, season):
    path = 'C:/Users/lantz/Documents/My Tableau Repository/Datasources/rapidapi-playerstats-team' + str(team) + '-' + season + '.xlsx'
    url = root_endpoint + "/players"
    querystring = {"team":team, "season":season}
    response = requests.request("GET", url, headers=headers, params=querystring)

    ### set columns ###
    cols = ['player_name', 'player_firstname', 'player_lastname']
    for key in response.json()['response'][0]["statistics"][0].keys():
        for subkey in response.json()['response'][0]["statistics"][0][key]:
            cols.append(key+'_'+subkey)
    stats_pd = pd.DataFrame(columns=cols)

    ### get stat values ###
    for player in response.json()['response']:
        row = {'player_name': player["player"]["name"], 'player_firstname': player["player"]["firstname"], 'player_lastname': player["player"]["lastname"]}
        for competition in player["statistics"]:
            for stat_name, stat_dict in competition.items():
                for stat, val in stat_dict.items():
                    row[stat_name+'_'+stat] = val
        stats_pd.loc[len(stats_pd)] = row
    print(stats_pd)
    
    # stats.fillna(value=np.nan, inplace=True)
    stats_pd.fillna(value=0, inplace=True) # replace None of NaN in same DataFrame

    ### export data
    if os.path.isfile(path):
        print("\nexporting {0} data for {1} season...".format(team, season))
        with pd.ExcelWriter(path, mode='a', if_sheet_exists="overlay") as writer:  
            stats_pd.to_excel(writer, sheet_name='Sheet1', startrow=writer.sheets["Sheet1"].max_row, index=False, header=False)
    else:
        print("\ncreating {0} data file for {1} season...".format(team, season))
        stats_pd.to_excel(path, index=False, header=True)
    print("...export completed.")

def get_statistics_by_fixture(file_name, fixture_id):
    path = 'C:/Users/lantz/Documents/My Tableau Repository/Datasources/rapidapi-fixturestats-' + file_name + '.xlsx'
    url = root_endpoint + "/fixtures/statistics"
    querystring = {"fixture":fixture_id} 
    response = requests.request("GET", url, headers=headers, params=querystring)

    ### set columns ###
    cols = ['Team Name']
    for stat in response.json()['response'][0]["statistics"]:
        cols.append(stat["type"])
    stats_pd = pd.DataFrame(columns=cols)

    ### get stat values ###
    for team in response.json()['response']:
        row = {'Team Name': team["team"]["name"]}
        for stat in team["statistics"]:
            row[stat["type"]] = stat["value"]
        stats_pd.loc[len(stats_pd)] = row
    
    # stats.fillna(value=np.nan, inplace=True) # replace None with NaN in same DataFrame
    stats_pd.fillna(value=0, inplace=True) # replace None with zero in same DataFrame
    print(stats_pd)

    ### export data
    if os.path.isfile(path):
        print("\nexporting data for fixture {}...".format(fixture_id))
        with pd.ExcelWriter(path, mode='a', if_sheet_exists="overlay") as writer:  
            stats_pd.to_excel(writer, sheet_name='Sheet1', startrow=writer.sheets["Sheet1"].max_row, index=False, header=False)
    else:
        print("\ncreating data file for fixture {}...".format(fixture_id))
        stats_pd.to_excel(path, index=False, header=True)
    print("...export completed.")

#######################################################################################################################################

if __name__ == "__main__":
    print(get_available_player_seasons())

    # get_team_statistics("39", "2020", "50")

    ### Get team squad ###
    # squad = get_current_team_squad(team_map["Manchester City"])
    # print(squad)

    ### Get individual player statistics by season ###
    # seasons = ["2018","2019","2020","2021","2022"]
    # for season in seasons:
    #     get_player_statistics(player_map["E. Haaland"], season)

    ### Player statistics by team ###
    # get_player_statistics_by_team(team_map["Manchester City"], "2022")
    # get_player_statistics_by_team(team_map["Manchester City"], "2021")

    ### 1027909 : 2023 UEFA Champions League Final ###
    # get_statistics_by_fixture("2023_UCL_Final", "1027909")