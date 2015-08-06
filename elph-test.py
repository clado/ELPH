import elph
import unittest

class TestELPHStreamDefaults(unittest.TestCase):

  def setUp(self):
    self.s = elph.ELPHStream()
    self.s.record('A')
    self.s.push('A')
    self.s.record('A')
    self.s.push('A')
    self.s.record('A')
    self.s.push('A')
    self.s.record('A')
    self.s.push('A')

    # this doesn't look correct to me. Need to debug
    # was A*A** already degreed useless?
    self.resulting_hspace = {'A*A': {'count': 1, 'frequency': {'A': 1}},
      'AAA': {'count': 1, 'frequency': {'A': 1}},
      'A*': {'count': 2, 'frequency': {'A': 2}},
      'AA*': {'count': 1, 'frequency': {'A': 1}},
      'AA': {'count': 2, 'frequency': {'A': 2}},
      'A**': {'count': 1, 'frequency': {'A': 1}},
      'A': {'count': 3, 'frequency': {'A': 3}}
      }

  def test_record(self):
    hypotheses = self.s.hspace.items()
    for hypothesis, histogram in hypotheses:
      self.assertEqual(self.s.hspace[hypothesis]['frequency'], self.resulting_hspace[hypothesis]['frequency'],
        'incorrectly recorded frequency of a hypothesis')
      self.assertEqual(self.s.hspace[hypothesis]['count'], self.resulting_hspace[hypothesis]['count'],
        'incorrectly recorded count of a subset')

  def test_push(self):
    self.assertEqual(set(self.s.hspace.keys()), set(self.resulting_hspace.keys()),
      'recorded incorrect subsets to hspace')


class example_from_prediction_paper(unittest.TestCase):

  def setUp(self):
    self.s = ELPHSteam(1, 2)
    self.s.record('A')
    self.s.push('A')
    self.s.record('B')
    self.s.push('B')
    self.s.record('A')
    self.s.push('A')
    self.s.record('C')
    self.s.push('C')
    self.s.record('A')
    self.s.push('A')
    self.s.record('B')
    self.s.push('B')
    self.s.record('A')
    self.s.push('A')
    self.s.record('D')
    self.s.push('D')

  def test_stream():
    pass

  def test_stream_memory(self):
    self.assertEqual(self.s.memory, 7,
      'default memory is not 7')
    self.assertEqual(len(self.s.stream), self.s.memory,
      'stream was not truncated to length of memory')


suite = unittest.TestLoader().loadTestsFromTestCase(TestELPHStreamDefaults)
unittest.TextTestRunner(verbosity=2).run(suite)
