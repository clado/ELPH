from math import log

def __shannon_entropy(histogram):
  entropy = 0
  for event in histogram.frequency:
    entropy += (histogram.frequency[event] / histogram.count) * log(histogram.frequency[event] / histogram.count)
  return entropy * -1

def __reliable_entropy(histogram):
  entropy = log(1 / histogram.count) / histogram.count
  for event in histogram.frequency:
    entropy += (histogram.frequency[event] / histogram.count) * log(histogram.frequency[event] / histogram.count)
  return entropy * -1

class ELPHStream():

  def __init__(self, hypothesis_threshold=1, memory=7):
    self.__stream = ''
    self.__histogram = {}
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
        if subset not in self.__histogram.keys():
          self.__histogram[subset] = { 'count': 1, 'frequency': { event: 1} }
        # old subset and new event
        elif event not in self.__histogram[subset]:
          self.__histogram[subset]['count'] += 1
          self.__histogram[subset]['frequency'][event] = 1
        # existing subset and existing event
        else:
          self.__histogram[subset]['count'] += 1
          self.__histogram[subset]['frequency'][event] += 1

    # add event to stream and restrict stream to the maximum memory
    self.__stream = self.__stream + event
    if (len(self.__stream) > self.__memory):
      self.__stream = self.__stream[-1 * self.__memory:]

  # TODO:
  def predict(self):
    pass

  def __prune(self):
    subsets = self.__histogram.keys()
    for subset in subets:
      if __shannon_entropy(self.__histogram[subset]) > hypothesis_threshold:
        del self.__histogram[subset]

s = ELPHStream()
s.record('s')
s.record('f')
s.record('5')
s.record('3')

