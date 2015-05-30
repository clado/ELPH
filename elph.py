
class ELPHStream():

  def __init__(self):
    self.stream = ''
    self.histogram = {}

  def record(self, event):

    # generate all subsets of current stream
    # such subsets can be represented as binary strings the length of the stream
    for pattern in range(1, 2**len(self.stream)):

      subset = list(self.stream)
      # check which bits in the binary string are turned on
      for i in range(len(self.stream)):
        if pattern ^ 2**i:
          # replace on bits with wildcards
          subset[i] = '*'

      # strip leading wildcards so that begining subsets remain valid with full streams
      subset = ''.join(subset).lstrip('*')
      if len(subset) > 0:
        # new subset
        if subset not in self.histogram.keys():
          self.histogram[subset] = { 'count': 1, 'frequency': { event: 1} }
        # old subset and new event
        elif event not in self.histogram[subset]:
          self.histogram[subset]['count'] += 1
          self.histogram[subset]['frequency'][event] = 1
        # existing subset and existing event
        else:
          self.histogram[subset]['count'] += 1
          self.histogram[subset]['frequency'][event] += 1

    # add event to stream and restrict stream to seven elements max
    self.stream = self.stream + event
    if (len(self.stream) > 7):
      self.stream = self.stream[-7:]

  # TODO:
  def predict(self):
    pass


s = ELPHStream()
s.record('s')
s.record('f')
s.record('5')
s.record('3')

