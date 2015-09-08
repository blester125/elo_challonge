import math

class player(object):
  def __init__(self, name, score=1200):
    self.name = name
    self.score = score

  def toString(self):
    print self.name + ": " + str(self.score)

def calculate_expected(playerA_rank, playerB_rank):
  expected_win_A = (1)/(1 + math.pow(10, 
                                    ((playerB_rank - playerA_rank)/400.0)))
  expected_win_B = (1)/(1 + math.pow(10, 
                                    ((playerA_rank - playerB_rank)/400.0)))
  return (expected_win_A, expected_win_B)

def calculate_new_rank(player_rank, expected, score):
  k = 24
  if player_rank < 2100:
    k = 32
  if player_rank > 2400:
    k = 16
  return player_rank + k * (score - expected)

def report_and_rank(winner, loser):
  expected_values = calculate_expected(winner.score, loser.score)
  winner_score = expected_values[0]
  loser_score = expected_values[1]
  winner.score = int(round(calculate_new_rank(winner.score, 
                                              winner_score, 1), 0))
  loser.score = int(round(calculate_new_rank(loser.score,
                                             loser_score, 0), 0))

if __name__ == '__main__':
  p1 = player('1')
  p2 = player('2')
  p1.toString()
  p2.toString()
  report_and_rank(p1, p2)
  p1.toString()
  p2.toString()