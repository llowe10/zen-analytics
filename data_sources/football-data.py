import requests
import json
import os

api_token = '749d535ef3fd4603bcfcc66d0c3e05c5'

def matches():
    uri = 'https://api.football-data.org/v4/matches'
    headers = { 'X-Auth-Token': api_token }

    response = requests.get(uri, headers=headers)
    for match in response.json()['matches']:
        print(json.dumps(match, indent=1))

def team(id):
    uri = 'https://api.football-data.org/v4/teams/'+ id +'/'
    headers = { 'X-Auth-Token': api_token }

    response = requests.get(uri, headers=headers)
    print(json.dumps(response.json(), indent=1))

def team_matches(id):
    uri = 'https://api.football-data.org/v4/teams/'+ id +'/matches/'
    headers = { 'X-Auth-Token': api_token }
    # filters = {"venue": "HOME"}
    filters = {}

    if filters:
        response = requests.get(uri, headers=headers, params=filters)
    else:
       response = requests.get(uri, headers=headers)

    home_count = 0
    away_count = 0
    for match in response.json()['matches']:
        if (match['score']['winner'] == "HOME_TEAM") and (match['homeTeam']['shortName'] == "Man City"):
            home_count += 1
        if (match['score']['winner'] == "AWAY_TEAM") and (match['awayTeam']['shortName'] == "Man City"):
            away_count += 1
        # print(json.dumps(match, indent=1))
        # print()
    print("Manchester City home wins: {}".format(home_count))
    print("Manchester City away wins: {}".format(away_count))

if __name__ == "__main__":
    # matches()
    # team("65")
    team_matches("65")