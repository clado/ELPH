

class ELPHStream():

  # optional acceptedKeys parameter to generate keys in advance
  def __init__(self, acceptedKeys = []):
    self.stream = []
    # should start with null string if not generating keys in advance?
    self.histogram = {} #{'':{}}

    # experiment with generating matches in advance

    ''' Algorithm 1: generate and add keys from smallest to largest length, '''
    ''' O(8 * (a + 1)^7 * (a + 1)), requires lstrip '''

    # if input keys to generate with, generate keys
    if (len(acceptedKeys) > 0):
      keys = ['']
      # generate keys of length 0-8
      for i in range(8):
        newKeys = []
        for oldKey in keys:
          # add old keys to histogram, unless it's all wild cards
          self.histogram[oldKey.lstrip('.')] = {}
          # generate new keys for each possible key
          newKeys.append(oldKey + '.')
          for key in acceptedKeys:
            newKeys.append(oldKey + key)
        keys = newKeys
      del self.histogram['']


    ''' Algorithm 2: generate all keys of length 7, then add '''
    ''' O(7 * (a + 1)^7 * (a + 1) + (a + 1)^7) '''

    # if (len(acceptedKeys) > 0):
    #   keys = ['']
    #   newKeys = []
    #   for i in range(7):
    #     newKeys = []
    #     for oldKey in keys:
    #       newKeys.append(oldKey + '.')
    #       for key in acceptedKeys:
    #         newKeys.append(oldKey + key)
    #     keys = newKeys
    #   for i in newKeys:
    #     self.histogram[i] = {}
    #   del self.hisogram['.......']

    # print("~~~" + str(len(self.histogram.keys())) + "~~~") # should be 16383

  def record(self, asdf):
    pass
    # compare speed of regex vs. manual...


ELPHStream(['r','p','s'])

