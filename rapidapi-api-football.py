import requests  # pip install requests
import pandas as pd  # pip install pandas
import numpy as np
import json
import os

# League ID 39 -> Premier League
# Team ID 50 -> Manchester City
team_map = {
    "Manchester City": 50
}

league_map = {
    "UEFA Champions League": 2
}

headers = {
    "X-RapidAPI-Key": "fdcd0a1831msh855607adde1935cp19bd72jsn07dca62515d5",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
}


def get_team_statistics(league_id, season, team_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"

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
    url = "https://api-football-v1.p.rapidapi.com/v3/players"

    querystring = {"id":id, "season":season}

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.json())

    # data = {
    #     "season": [ season, season, season ],
    #     "wins": [
    #         response.json()["response"]["fixtures"]["wins"]["home"],
    #         response.json()["response"]["fixtures"]["wins"]["away"],
    #         response.json()["response"]["fixtures"]["wins"]["total"],
    #     ],
    #     "played": [
    #         response.json()["response"]["fixtures"]["played"]["home"],
    #         response.json()["response"]["fixtures"]["played"]["away"],
    #         response.json()["response"]["fixtures"]["played"]["total"],
    #     ]
    # }
    # df = pd.DataFrame(data, index=["home", "away", "total"])

    # print(df)

def get_player_statistics_by_team(team, season):
    path = 'C:/Users/lantz/Documents/My Tableau Repository/Datasources/rapidapi-playerstats-' + str(team) + '-' + season + '.xlsx'

    url = "https://api-football-v1.p.rapidapi.com/v3/players"

    querystring = {"team":team, "season":season}

    response = requests.request("GET", url, headers=headers, params=querystring)

    stats = pd.DataFrame(columns = [
                    'Name', 
                    'Age', 
                    'Position', 
                    'Competition', 
                    'Appearances', 
                    'Rating',
                    'Shots', 
                    'Goals', 
                    # 'Goal Conversion %', 
                    'Total Passes', 
                    'Key Passes', 
                    'Accurate Passes',
                    'Tackles',
                    'Blocks',
                    'Interceptions',
                    'Total Duels',
                    'Duels Won',
                    'Attempted Dribbles',
                    'Successful Dribbles',
                    'Penalties Scored',
                    'Penalties Missed',
                    'Penalties Saved'
                ]
            )
    # print(stats)

    for player in response.json()['response']:
        for i in range(0,len(player["statistics"])):

            # try:
            #     conv_percent = (player["statistics"][i]["goals"]["total"]/player["statistics"][i]["shots"]["total"])*100.0
            # except ZeroDivisionError:
            #     conv_percent = 0

            row = {
                'Name': player["player"]["name"],
                'Age': player["player"]["age"],
                'Position': player["statistics"][i]["games"]["position"],
                'Competition': player["statistics"][i]["league"]["name"],
                'Appearances': player["statistics"][i]["games"]["appearences"],
                'Rating': player["statistics"][i]["games"]["rating"],
                'Shots': player["statistics"][i]["shots"]["total"],
                'Goals': player["statistics"][i]["goals"]["total"],
                # 'Goal Conversion %': conv_percent,
                'Total Passes': player["statistics"][i]["passes"]["total"],
                'Key Passes': player["statistics"][i]["passes"]["key"],
                'Accurate Passes': player["statistics"][i]["passes"]["accuracy"],
                'Tackles': player["statistics"][i]["tackles"]["total"],
                'Blocks': player["statistics"][i]["tackles"]["blocks"] ,
                'Interceptions': player["statistics"][i]["tackles"]["interceptions"],
                'Total Duels': player["statistics"][i]["duels"]["total"],
                'Duels Won': player["statistics"][i]["duels"]["won"],
                'Attempted Dribbles': player["statistics"][i]["dribbles"]["attempts"],
                'Successful Dribbles': player["statistics"][i]["dribbles"]["success"],
                'Penalties Scored': player["statistics"][i]["penalty"]["scored"],
                'Penalties Missed': player["statistics"][i]["penalty"]["missed"],
                'Penalties Saved': player["statistics"][i]["penalty"]["saved"]
            }

            stats.loc[len(stats)] = row
            # stats.loc[player["player"]["name"]] = row
            # print(json.dumps(player, indent=1))
    
    # stats.fillna(value=np.nan, inplace=True)
    stats.fillna(value=0, inplace=True) # replace None of NaN in same DataFrame
    # print(stats)

    ### export data
    if os.path.isfile(path):
        print("\nexporting {0} data for {1} season...".format(team, season))
        with pd.ExcelWriter(path, mode='a', if_sheet_exists="overlay") as writer:  
            stats.to_excel(writer, sheet_name='Sheet1', startrow=writer.sheets["Sheet1"].max_row, index=False, header=False)
    else:
        print("\ncreating {0} data file for {1} season...".format(team, season))
        stats.to_excel(path, index=False, header=True)
    print("...export completed.")

def get_statistics_by_fixture(file_name, fixture_id):
    path = 'C:/Users/lantz/Documents/My Tableau Repository/Datasources/rapidapi-fixturestats-' + file_name + '.xlsx'
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"
    querystring = {"fixture":fixture_id} 
    response = requests.request("GET", url, headers=headers, params=querystring)

    ### set columns ###
    cols = ['Team Name']
    for team in response.json()['response']:
        for stat in team["statistics"]:
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
    # get_team_statistics("39", "2020", "50")
    # get_player_statistics_by_team(team_map["Manchester City"], "2019")

    # 1027909 : 2023 UEFA Champions League Final
    get_statistics_by_fixture("2023_UCL_Final", "1027909")