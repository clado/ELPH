from math import log

def shannon_entropy(histogram):
  entropy = 0
  for event in histogram['frequency']:
    entropy += (histogram['frequency'][event] / histogram['count']) * log(histogram['frequency'][event] / histogram['count'])
  return entropy * -1

def reliable_entropy(histogram):
  entropy = log(1 / histogram['count']) / histogram['count']
  for event in histogram['frequency']:
    entropy += (histogram['frequency'][event] / histogram['count']) * log(histogram['frequency'][event] / histogram['count'])
  return entropy * -1

class ELPHStream():

  def __init__(self, hypothesis_threshold=1, memory=7):
    self.__stream = ''
    self.__hspace = {}
    self.__threshold = hypothesis_threshold
    self.__memory = memory

  def record(self, event):

    # generate all subsets of current stream
    # such subsets can be represented as binary strings the length of the stream
    for pattern in range(1, 2**len(self.__stream)):

      subset = list(self.__stream)
      # check which bits in the binary string are turned on
      for i in range(len(self.__stream)):
        if pattern ^ 2**i:
          # replace on bits with wildcards
          subset[i] = '*'

      # strip leading wildcards so that begining subsets remain valid with full streams
      subset = ''.join(subset).lstrip('*')
      if len(subset) > 0:
        # new subset
        if subset not in self.__hspace.keys():
          self.__hspace[subset] = { 'count': 1, 'frequency': { event: 1} }
        # old subset and new event
        elif event not in self.__hspace[subset]:
          self.__hspace[subset]['count'] += 1
          self.__hspace[subset]['frequency'][event] = 1
        # existing subset and existing event
        else:
          self.__hspace[subset]['count'] += 1
          self.__hspace[subset]['frequency'][event] += 1

    # add event to stream
    self.__stream = self.__stream + event
    # restrict stream to the maximum memory
    if len(self.__stream) > self.__memory:
      self.__stream = self.__stream[-1 * self.__memory:]

  # predict the next element in the stream
  # returns element (string), entropy (double) as a tuple
  def predict(self):
    lowest_entropy = self.__threshold
    predictive_subset = ''

    for subset, histogram in self.__hspace.items():
      # use regex or do manually?
      index = -1
      matches = True
      # calcualte lengths once beforehand
      while index >= -1 * len(self.__stream) and index >= -1 * len(subset) and matches:
        if self.__stream[index] != subset[index] and subset[index] != '*':
          matches = False
        index -= 1
      if matches:
        # using naive approach for now...
        possible_entropy = shannon_entropy(histogram)
        if possible_entropy < lowest_entropy:
          lowest_entropy = possible_entropy
          predictive_subset = subset

    result = self.__hspace[predictive_subset]
    max_count = 0
    best_guess = ''
    for guess, count in result['frequency'].items():
      if count > max_count:
        max_count = count
        best_guess = guess
    return best_guess, lowest_entropy

  # should be public so that we can call this at custom times?
  # allow threshold to be overwritten?
  def __prune(self):
    for subset, histogram in self.__hspace.items():
      if shannon_entropy(histogram) > self.__threshold:
        del self.__hspace[subset]

