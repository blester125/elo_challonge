import pickle
import sys

from challonge import *
from elo_player import *

USERNAME = '' 
API_KEY = ''
SUBDOMAIN = ''
config_file = open("config.txt", 'r')
for line in config_file:
  parts = line.split(":")
  if len(parts) >= 2:
    if parts[1].endswith("\n"):
      parts[1] = parts[1][:-1]
  if parts[0] == "username":
    USERNAME = parts[1]
  elif parts[0] == "APIKey":
    API_KEY = parts[1]
  elif parts[0] == "subdomain":
    SUBDOMAIN = parts[1]

def elo(players, t_list):
  # Challonge Log-in
  api.set_credentials(USERNAME, API_KEY)
  tourns = tournaments.index(SUBDOMAIN)
  #bracket_url = "moal-MoaL1MeleeSingles"
  #tournament = tournaments.show(bracket_url)
  for tournament in tourns:
    if tournament['id'] in t_list:
      continue  
    # MoaL only
    tournament_name = tournament['name']
    if ('Singles' in tournament_name 
          and 'Melee' in tournament_name
          and 'MoaL' in tournament_name):
      print tournament_name
      tournament_parse(tournament, players)
      t_list.append(tournament['id'])

def tournament_parse(tournament, players):
  matchs = matches.index(tournament['id'])
  for match in matchs:
    winner = match['winner-id']
    player1 = participants.show(tournament['id'], match['player1-id'])
    player2 = participants.show(tournament['id'], match['player2-id'])
    player1_name = player1['display-name']
    player2_name = player2['display-name']
    if player1_name in players:
      player1_obj = players[player1_name]
    else:
      player1_obj = player(player1_name)
      players[player1_name] = player1_obj
    if player2_name in players:
      player2_obj = players[player2_name]
    else:
      player2_obj = player(player2_name)
      players[player2_name] = player2_obj
    if player1['id'] == winner:
      report_and_rank(player1_obj, player2_obj)
    else:
      report_and_rank(player2_obj, player1_obj)
  pickle.dump(players, open("elo.pkl", "wb"))
  pickle.dump(t_list, open("tourn.pkl", "wb"))

def display(players, t_list):
  api.set_credentials(USERNAME, API_KEY)
  print "ELO analysis was done on the following tournaments."
  for i in t_list:
    tournament = tournaments.show(i)
    print tournament['name']
  list = []
  for key in players:
    list.append(players[key])
  list.sort(key=lambda x: x.score, reverse=True)
  for i in list:
    i.toString()

if __name__ == "__main__":
  try:
    arg = sys.argv[1]
  except IndexError:
    print "Usage: python elo.py elo|display"
    exit()
  # load in player dict
  try:
    players = pickle.load(open("elo.pkl", "rb"))
  except IOError:
    players = {}
  # load in tournament list
  try:
    t_list = pickle.load(open("tourn.pkl", "rb"))
  except IOError:
    t_list = []
  if arg == "elo":
    elo(players, t_list)
  elif arg == "display":
    display(players, t_list)
  else:
    print "Useage: python elo.py elo|display"