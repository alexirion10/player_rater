import requests
import json
import base64
import pandas
import re

SET_OF_PLAYERS = set()

"""
 1. Get top 500 player stats
 2. Sum all stats to get a baseline...
 3. Score the value of each stat
 4. score each player
 5. rank!
"""

# class PlayerStats:
    #     name
    ### hitting ####
    #     runs
    #     HR
    #     TB
    #     RBI
    #     SBN
    #     OPS
    ### Pitching ###
    #     K
    #     QS
    #     W
    #     SV
    #     ERA
    #     WHIP

def format_name(name):
    name = re.sub('.\'', '', name).strip().lower().replace('jr','')
    return name

class Player:
    def __init__(self, json):
        player = json['player']
        self.firstName = format_name(player['FirstName'])
        self.lastName = format_name(player['LastName'])
        self.position = player['Position'].strip().upper()
        self.team = json['team']['Abbreviation'].strip().upper()
        self.score = 0

        if self.position == 'P':
            stats = json['stats']
            self.r = 0
            self.hr = 0
            self.rbi = 0
            self.sbn = 0
            self.obp = 0
            self.slg = 0
            self.k = stats['PitcherStrikeouts']['#text']
            self.qs = 0 # stats['']['#text'] ??????  InningsPitched  ... StrikeoutsPer9Innings ...GamesStarted
            self.wins = stats['Wins']['#text']
            self.saves = stats['Saves']['#text']
            self.era = stats['EarnedRunAvg']['#text']
            self.whip = stats['WalksAndHitsPerInningPitched']['#text']
            self.kper9 = stats['StrikeoutsPer9Innings']['#text']
        else:
            stats = json['stats']
            self.r = stats['Runs']['#text']
            self.hr = stats['Homeruns']['#text']
            self.rbi = stats['RunsBattedIn']['#text']
            self.sbn = int(stats['StolenBases']['#text']) - int(stats['CaughtBaseSteals']['#text'])
            self.obp = stats['BatterOnBasePct']['#text']
            self.slg = stats['BatterSluggingPct']['#text']
            self.k = 0
            self.qs = 0
            self.wins = 0
            self.saves = 0
            self.era = 0
            self.whip = 0
            self.kper9 = 0

    def compute_score(self):
        self.score = 1

    def str(self):
        print(json.dumps(vars(self), indent=4, sort_keys=False))
        # print(', '.join("{%s: '%s'}" % item for item in vars(self).items()))


def create_player(player_data):
    """
    ToDo: 
      - add player data to pandas data frame?
      - total all stats across all players?
    Param: a JSON blob of the following form and creates a class from it
    {
        "player": {
          "ID": "12370",
          "LastName": "Abreu",
          "FirstName": "Albert",
          "Position": "P"
        },
        "team": {
          "ID": "114",
          "City": "New York",
          "Name": "Yankees",
          "Abbreviation": "NYY"
        },
        "stats": {
          "GamesPlayed": {
            "@abbreviation": "G",
            "#text": "0"
          },...
        }
    }
    """
    if 'JerseyNumber' not in player_data['player']:
        print('No JerseyNumber ' + player_data['player']['FirstName'] + ' ' + player_data['player']['LastName'])

    x = Player(player_data)
    if str(x.firstName + ' ' + x.lastName) in SET_OF_PLAYERS:
        x.str()
    else:
        print('Not in players list: ' + str(x.firstName + ' ' + x.lastName))
    

    
def read_in_players():
    with open('2018_players.txt', 'r') as players:
        for player in players:
            SET_OF_PLAYERS.add(player.strip().lower())


def api_v2(api_credentials):
    # v2 API. Need to get credentials to work
    # response = requests.get(
    #             url='https://api.mysportsfeeds.com/v2.1/pull/mlb/2018-regular/player_stats_totals.json',
    #             headers={"Authorization": "Basic " + base64.b64encode('{}:{}'.format(api_credentials['apikey_token'],'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')}
    #           )
    # print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
    # return response.json()['playerStatsTotals']
    return ()


def api_v1(api_credentials):
    response = requests.get(
                url='https://api.mysportsfeeds.com/v1.2/pull/mlb/{}-regular/cumulative_player_stats.json'.format('2018'),
                params={},
                headers={"Authorization": "Basic " + base64.b64encode('{}:{}'.format(api_credentials['user'], api_credentials['pw']).encode('utf-8')).decode('ascii')}
              )
    print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
    return response.json()["cumulativeplayerstats"]['playerstatsentry']


def main():
    read_in_players()
    api_credentials = {}

    with open('login.json') as f:
        api_credentials = json.load(f)

    list_of_players = api_v1(api_credentials)
    # list_of_players = api_v2(credentials)

    print(len(list_of_players))
    for i, player_data in enumerate(list_of_players):
        if i > 20:
            return
        create_player(player_data)


if __name__ == '__main__':
    main()




