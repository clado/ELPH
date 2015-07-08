import elph
import unittest

class TestELPHStreamDefaults(unittest.TestCase):

  def setUp(self):
    self.s = elph.ELPHStream()
    self.s.record('A')
    self.s.record('A')
    self.s.record('A')
    self.s.record('A')
    self.s.record('A')
    self.s.record('A')
    self.s.record('A')
    self.s.record('A')
    self.s.record('A')

    # this doesn't look correct to me. Need to debug
    # was A*A** already degreed useless?
    self.resulting_hspace = { 'A': {'frequency': {'A': 8}, 'count': 8},
      'A*': {'frequency': {'A': 7}, 'count': 7},
      'A**': {'frequency': {'A': 6}, 'count': 6},
      'A***': {'frequency': {'A': 5}, 'count': 5},
      'A****': {'frequency': {'A': 4}, 'count': 4},
      'A*****': {'frequency': {'A': 3}, 'count': 3},
      'A******': {'frequency': {'A': 2}, 'count': 2} }

  def test_record(self):
    self.assertEqual(list(self.s.hspace.keys()), list(self.resulting_hspace.keys()),
      'recorded incorrect subsets to hspace')

  def test_hspace_frequencies(self):
    hypotheses = self.s.hspace.items()
    for hypothesis, histogram in hypotheses:
      self.assertEqual(self.s.hspace[hypothesis]['frequency'], self.resulting_hspace[hypothesis]['frequency'],
        'incorrectly recorded frequency of a hypothesis')
      self.assertEqual(self.s.hspace[hypothesis]['count'], self.resulting_hspace[hypothesis]['count'],
        'incorrectly recorded count of a subset')

  def test_stream_memory(self):
    self.assertEqual(self.s.memory, 7,
      'default memory is not 7')
    self.assertEqual(len(self.s.stream), self.s.memory,
      'stream was not truncated to length of memory')


class example_from_prediction_paper(unittest.TestCase):

    def setUp(self):
      self.s = ELPHSteam(1, 2)
      self.s.record('A')
      self.s.record('B')
      self.s.record('A')
      self.s.record('C')
      self.s.record('A')
      self.s.record('B')
      self.s.record('A')
      self.s.record('D')

    def test_stream():
      pass



suite = unittest.TestLoader().loadTestsFromTestCase(TestELPHStreamDefaults)
unittest.TextTestRunner(verbosity=2).run(suite)
