from math import log

# not currently in use
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

def is_set(number, place):
  return number & (2**place) != 0

class ELPHStream():

  # hypothesis_threshold: all hypotheses with entropy above this value will be pruned
  # memory: max stream size to be maintained/"max items to be remembered"
  def __init__(self, hypothesis_threshold=1, memory=7):
    self.stream = ''
    self.hspace = {}
    self.threshold = hypothesis_threshold
    self.memory = memory

  # record a new event by adding it to the stream and adding applicable hypotheses to the hspace
  # takes event (string) that will be recroded
  def record(self, event):

    # add `*` to hspace
    # maybe only do this if the length is > 0 ?
    self.__add_to_hspace('*', event)

    # generate all subsets of current stream
    # such subsets can be represented as binary strings the length of the stream
    for pattern in range(0, 2**len(self.stream)):

      subset = list(self.stream)
      # check which bits in the binary string are turned on
      for i in range(len(self.stream)):
        if is_set(pattern, i):
          # replace on bits with wildcards
          subset[i] = '*'

      # strip leading wildcards so that begining subsets remain valid with full streams
      subset = ''.join(subset).lstrip('*')
      if len(subset) > 0:
        self.__add_to_hspace(subset, event)

  def push(self, event):
    # add event to stream
    self.stream = self.stream + event
    # restrict stream to the maximum memory
    if len(self.stream) > self.memory:
      self.stream = self.stream[-1 * self.memory:]

  # predict the next element in the stream
  # returns element (string), entropy (double) as a tuple
  def predict(self):
    # early return in case prediction is called on empty hspace
    if len(self.hspace.items()) == 0:
      return None, self.threshold

    subset, lowest_entropy = self.__lowest_entropy_subset()
    result = self.hspace[subset]
    max_count = 0
    best_guess = ''
    for guess, count in result['frequency'].items():
      if count > max_count:
        max_count = count
        best_guess = guess
    return best_guess, lowest_entropy

  # removes hypotheses that are no longer reliable from the hspace
  def prune(self):
    # WHY DO YOU MAKE ME DO THIS, PYTHON?!
    keys_to_delete = []
    for hypothesis in self.hspace.keys():
      if shannon_entropy(self.hspace[hypothesis]) > self.threshold:
        keys_to_delete += [hypothesis]
    for key in keys_to_delete:
      del self.hspace[key]

  # records an instance of the event for the subset in the hspace
  # takes subset (string) observed
  # takes event (string) to record
  def __add_to_hspace(self, subset, event):
    # new subset
    if subset not in self.hspace.keys():
      self.hspace[subset] = { 'count': 1, 'frequency': { event: 1 } }
    # old subset and new event
    elif event not in self.hspace[subset]['frequency']:
      self.hspace[subset]['count'] += 1
      self.hspace[subset]['frequency'][event] = 1
    # existing subset and existing event
    else:
      self.hspace[subset]['count'] += 1
      self.hspace[subset]['frequency'][event] += 1

  # returns lowest entropy subset of the current stream
  def __lowest_entropy_subset(self):
    lowest_entropy = self.threshold
    predictive_subset = '*'

    for subset, histogram in self.hspace.items():
      # use regex or do manually?
      index = -1
      matches = True
      # calculate lengths once beforehand
      while index >= -1 * len(self.stream) and index >= -1 * len(subset) and matches:
        if self.stream[index] != subset[index] and subset[index] != '*':
          matches = False
        index -= 1
      if matches:
        possible_entropy = shannon_entropy(histogram)
        if possible_entropy < lowest_entropy:
          lowest_entropy = possible_entropy
          predictive_subset = subset

    return predictive_subset, lowest_entropy

