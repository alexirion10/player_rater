import sys
import os
import csv
import requests
import json
import argparse
import pandas
import re
from selenium import webdriver
from bs4 import BeautifulSoup

pitcher = ('SP', 'RP')
math = ['Mike Trout', 'Chris Sale', 'Mookie Betts', 'Edwin Diaz', 'Jacob deGrom']

# AVG, STDEV
AB_AVG = 446.638796
AB_STDEV = 108.6588197
R_AVG = 62.24080268
R_STDEV = 19.76354048
HR_AVG = 17.34782609
HR_STDEV = 8.108343712
RBI_AVG = 61.25083612
RBI_STDEV = 20.11806184
SB_AVG = 7.565217391
SB_STDEV = 8.068162431
OBP_AVG = 0.324337793
OBP_STDEV = 0.024914763
SLG_AVG = 0.437722408
SLG_STDEV = 0.046053334

IP_AVG = 104.5949833
IP_STDEV = 50.48724945
K_AVG = 103.0668896
K_STDEV = 49.5575952
W_AVG = 6.2909699
W_STDEV = 3.675460807
SV_AVG = 3.7090301
SV_STDEV = 8.55297068
ERA_AVG = 3.93270903
ERA_STDEV = 0.553831395
WHIP_AVG = 1.289665552
WHIP_STDEV = 0.115778175
IPGS_AVG = 4.506244539
IPGS_STDEV = 5.815211725 # QS ?

class Player:
    '''
    Holds stats I want for each player
    '''
    def __init__(self, pandas_row):
        self.name = pandas_row['Player']
        self.team = pandas_row['Team']
        self.position = pandas_row['Positions'].split(',', 1)[0]
        self.score = 0

        self.ab = pandas_row['AB']
        self.r = pandas_row['R']
        self.hr = pandas_row['HR']
        self.rbi = pandas_row['RBI']
        self.sb = pandas_row['SB']
        self.obp = pandas_row['OBP']
        self.slg = pandas_row['SLG']
        self.ip = pandas_row['IP']
        self.k = pandas_row['K']
        self.wins = pandas_row['W']
        self.saves = pandas_row['SV']
        self.era = pandas_row['ERA']
        self.whip = pandas_row['WHIP']
        self.qs = 0
        self.ip_per_gs = 0 if self.ip == 0 or pandas_row['GS'] == 0 else self.ip / pandas_row['GS']

        self.compute_score()

    def compute_score(self):
        self.score = 0
        if self.position in pitcher:
            self.score += (self.k - K_AVG)/K_STDEV
            self.score += (self.wins - W_AVG)/W_STDEV
            self.score += (self.saves - SV_AVG)/SV_STDEV
            self.score += -1*(self.era - ERA_AVG)/ERA_STDEV
            self.score += -1*(self.whip - WHIP_AVG)/WHIP_STDEV
            # self.score *= (6/5)
            self.score += (self.ip_per_gs - IPGS_AVG)/IPGS_STDEV
            self.score += (self.ip - IP_AVG)/IP_STDEV
        else :
            self.score += (self.r - R_AVG)/R_STDEV
            self.score += (self.hr - HR_AVG)/HR_STDEV
            self.score += (self.rbi - RBI_AVG)/RBI_STDEV
            self.score += (self.sb - SB_AVG)/SB_STDEV
            self.score += (self.obp - OBP_AVG)/OBP_STDEV
            self.score += (self.slg - SLG_AVG)/SLG_STDEV
            self.score += (self.ab - AB_AVG)/AB_STDEV
        print(self.name + ',' + self.position + ',' + str(self.score))

    def str(self):
        print(json.dumps(vars(self), indent=4, sort_keys=False))
        # print(', '.join('{%s: '%s'}' % item for item in vars(self).items()))


def fantasypros_real_rater():
    response = requests.get(url='https://www.fantasypros.com/mlb/stats/hitters.php?range={}'.format('2018'))
    print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
    # beautiful soup parse here response.json()
    return

def fantasypros_2019_projection():
    list_of_players = []
    dataframe = pandas.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/fantasypros_2019_projections.csv'))
    # print(dataframe.head())
    for index, row in dataframe.iterrows():
        list_of_players.append(Player(row))
    # with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/fantasypros_2019_ranks.csv'), 'w') as output:
    #     for player in list_of_players():
    #         player.score()
            # output.write...

def espn_real_rater():
    return

def espn_2019_projection():
    browser = webdriver.Safari() #replace with .Firefox(), or with the browser of your choice
    url = "http://fantasy.espn.com/baseball/playerrater?leagueId=200702"
    browser.get(url)
    innerHTML = browser.execute_script("return document.Scripts.playerrater.js") #returns the inner HTML as a string
    print(innerHTML)


def main():
    # setuptools = ()
    parser = argparse.ArgumentParser(description='Fantasy Baseball Player Rater')
    parser.add_argument("-v", "--verbose", help="verbose output", action="store_false")
    # parser.add_argument("square", type=int, help="display a square of a given number")
    parser.parse_args()

    # fantasypros_real_rater()
    fantasypros_2019_projection()
    # espn_real_rater()
    # espn_2019_projection()


if __name__ == '__main__':
    main()




