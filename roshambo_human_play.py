from roshambo_elph import RoshamboELPHStream


valid_moves = {'R', 'P', 'S'}
win_map = {'R': 'S', 'P': 'R', 'S': 'P'}

def is_a_tie(player_one_move, player_two_move):
  if player_one_move == player_two_move:
    return True
  return False

def player_one_won(player_one_move, player_two_move):
  if win_map[player_one_move] == player_two_move:
    return True
  return False

def print_statistics(games_played, games_won):
  print('Games Played:', games_played)
  print('Games ELPH won:', games_won)
  print('ELPH win percentage: ' + str((games_played / games_won) * 100) + '%')
  print('Pretty graphics to come if you ask nicely')

def main():
  print('Welcome to roshambo elph stuff')

  rounds = int(input('Please input the number of games you would like to play: '))

  elph_agent = RoshamboELPHStream()

  game = 0
  previous_move = None
  games_elph_won = 0
  while game < rounds:
    game += 1

    print('Game', game, 'of', rounds)
    player_move = input('Make your move: ').upper()
    while player_move not in valid_moves:
      player_move = input('Please choose one from "r", "p", "s"\nMake your move: ').upper()

    agent_move = elph_agent.move(previous_move)

    if player_one_won(agent_move, player_move):
      games_elph_won += 1
      print('ELPH won.')
    elif is_a_tie(agent_move, player_move):
      print('It was a tie.')
    else:
      print('You won.')

    previous_move = player_move

  print_statistics(rounds, games_elph_won)


main()

