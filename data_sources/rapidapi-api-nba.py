# py data_sources/rapidapi-api-nba.py

import requests  # pip install requests
import pandas as pd  # pip install pandas
import numpy as np # pip install numpy
import json
import os

#######################################################################################################################################

root_endpoint = "https://api-nba-v1.p.rapidapi.com"

headers = {
	"X-RapidAPI-Key": "fdcd0a1831msh855607adde1935cp19bd72jsn07dca62515d5",
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

def get_games_by_team(team, season):
	url = root_endpoint + "/games"
	querystring = {"team":team, "season":season}
	response = requests.get(url, headers=headers, params=querystring)
	print(response.json())

if __name__ == "__main__":
	# get_seasons()
	get_games_by_team(team_map["Hornets"], "2022")