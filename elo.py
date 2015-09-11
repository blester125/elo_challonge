import pickle
import sys

from challonge import *
from elo_player import *

def obtain_config_info():
  USERNAME = '' 
  API_KEY = ''
  SUBDOMAIN = ''
  FILTER = []
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
    elif parts[0] == "filter":
    	FILTER.append(parts[1])
  return (USERNAME, API_KEY, SUBDOMAIN, FILTER)

def elo(players, t_list, USERNAME, API_KEY, SUBDOMAIN, url_filter):
  api.set_credentials(USERNAME, API_KEY)
  tourns = tournaments.index(SUBDOMAIN)
  for tournament in tourns:
    if tournament['id'] in t_list:
      continue  
    tournament_name = tournament['name']
    if all(word in tournament_name for word in url_filter):
      tournament_parse(tournament, players, USERNAME, API_KEY)

def tournament_parse(tournament, players, USERNAME, API_KEY):
  api.set_credentials(USERNAME, API_KEY)
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
  t_list.append(tournament['id'])
  pickle.dump(t_list, open("tourn.pkl", "wb"))

def display(players, t_list, USERNAME, API_KEY):
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
  # Ask for file names
  try:
    players = pickle.load(open("elo.pkl", "rb"))
  except IOError:
    players = {}
  try:
    t_list = pickle.load(open("tourn.pkl", "rb"))
  except IOError:
    t_list = []
  USERNAME, API_KEY, SUBDOMAIN, url_filter = obtain_config_info()
  if arg == "elo":
    elo(players, t_list, USERNAME, API_KEY, SUBDOMAIN, url_filter)
  elif arg == "display":
    display(players, t_list, USERNAME, API_KEY)
  else:
    print "Useage: python elo.py elo|display"