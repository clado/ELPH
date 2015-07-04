from random import randint
from elph import ELPHStream

# probably shouldn't be global variables, but also don't really belong on each instance of an elph stream
# does python have final/static variables?
# using an array so it can be indexed
valid_moves = ['R', 'P', 'S']
opponent_move_map = {'R': 'P', 'P': 'S', 'S': 'R'}
agent_move_map = {'R': 'S', 'P': 'R', 'S': 'P'}

class RoshamboELPHStream():

  def __init__(self, hypothesis_threshold=1, memory=7):
    self.__agent_moves = ELPHStream(hypothesis_threshold, memory)
    self.__opponent_moves = ELPHStream(hypothesis_threshold, memory)

  def move(self, opponent_move=None):
    if opponent_move != None:
      self.__opponent_moves.record(opponent_move)

    # should we be pruning every turn?
    self.__agent_moves.prune()
    self.__opponent_moves.prune()

    opponent_hypothesis, opponent_entropy = self.__opponent_moves.predict()
    agent_hypothesis, agent_entropy = self.__agent_moves.predict()

    print(agent_hypothesis, opponent_hypothesis)

    next_move = self.__transform_prediction(opponent_move_map, opponent_hypothesis)
    
    # not sure if I'm using the agent move map correctly...
    if agent_entropy < opponent_entropy:
      next_move = self.__transform_prediction(agent_move_map, agent_hypothesis)

    self.__agent_moves.record(next_move)
    return next_move

  def __transform_prediction(self, move_map, prediction=None):
    if prediction in valid_moves:
      return move_map[prediction]
    random_number = randint(0, len(valid_moves) - 1)
    return valid_moves[random_number]

