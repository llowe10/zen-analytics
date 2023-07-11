# python data_sources/rapidapi-api-nba.py

import requests  # pip install requests
import pandas as pd  # pip install pandas
import numpy as np # pip install numpy
import json
import os
from datetime import datetime

#######################################################################################################################################

root_endpoint = "https://api-nba-v1.p.rapidapi.com"

headers = {
	"X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

team_map = {
    "Hornets": "5",
    "Cavs": "7"
}

def get_seasons():
	url = root_endpoint + "/seasons"
	response = requests.get(url, headers=headers)
	print(response.json())

def get_games_by_team(team_id, season):
	url = root_endpoint + "/games"
	querystring = {"team":team_id, "season":season}
	response = requests.get(url, headers=headers, params=querystring)

	### set columns ###
	cols = [
		'id','season','date','arena','homeTeam','homeScore',
		'homeQ1Points','homeQ2Points','homeQ3Points','homeQ4Points','homeQ5Points',
		'visitingTeam','visitingScore',
		'visitingQ1Points','visitingQ2Points','visitingQ3Points','visitingQ4Points','visitingQ5Points',
		'timesTied','leadChanges'
		]
	stats_pd = pd.DataFrame(columns=cols)

	### get stat values ###
	for game in response.json()['response']:
		home_quarter_points = game["scores"]["home"]["linescore"]
		visitor_quarter_points = game["scores"]["visitors"]["linescore"]
		row = {
			'id': game["id"],
			'season':game["season"],
			'date':game["date"]["start"][:-5],
			'arena':game["arena"]["name"],
			'homeTeam':game["teams"]["home"]["name"],
			'homeScore':game["scores"]["home"]["points"],
			'visitingTeam':game["teams"]["visitors"]["name"],
			'visitingScore':game["scores"]["visitors"]["points"],
			'timesTied':game["timesTied"],
			'leadChanges':game["leadChanges"]
		}
		for i in range(0,len(home_quarter_points)):
			row['homeQ{}Points'.format(i+1)] = home_quarter_points[i]
			row['visitingQ{}Points'.format(i+1)] = visitor_quarter_points[i]
		stats_pd.loc[len(stats_pd)] = row

	### Convert data types
	date_format = '%Y-%m-%dT%H:%M:%S'
	cols = list(stats_pd.columns)
	for col in cols:
		if col in ['arena','homeTeam','visitingTeam']:
			stats_pd[col] = stats_pd[col].astype(str)
		elif col == 'date':
			stats_pd[col] = pd.to_datetime(stats_pd[col], format=date_format) # datetime.strptime(str(stats_pd[col]), date_format)
		else:
			stats_pd[col] = stats_pd[col].apply(pd.to_numeric)
	# print(stats_pd.info())

	stats_pd.to_csv(r"C:\Users\lantz\OneDrive\Documents\My Tableau Repository\Datasources\api-nba\hornets_2022_games.csv",index=False)
	print("{0} season data export for team {1} completed.".format(season,team_id))

def get_team_season_stats(team_id, season):
	url = root_endpoint + "/statistics"
	querystring = {"id":team_id, "season":season}
	response = requests.get(url, headers=headers, params=querystring)
	print(response.json())

def get_game_stats(game_id):
	url = root_endpoint + "/games/statistics"
	querystring = {"id":game_id}
	response = requests.get(url, headers=headers, params=querystring)
	print(response.json())

if __name__ == "__main__":
	# get_seasons()
	get_games_by_team(team_map["Hornets"], "2022")