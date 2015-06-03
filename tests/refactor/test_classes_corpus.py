import sys
sys.path.append('../tethne')

import unittest
from tethne.readers.wos_refactor import WoSParser
from tethne.classes.corpus import Corpus
from tethne.utilities import _iterable

datapath = './tests/data/refactor_data/wos.txt'


class TestCorpus(unittest.TestCase):
	def setUp(self):
		parser = WoSParser(datapath)
		self.papers = parser.parse()
		
	def test_init(self):
		"""
		Check for clean initialization.
		"""

		try:
			corpus = Corpus(self.papers, index_by='wosid')	
		except Exception as E:
			failure_msg = ' '.join(['Initialization failed with exception',
									'{0}: {1}'.format(E.__class__.__name__,
                                                      E.message)])
			self.fail(failure_msg)

	def test_indexing(self):
		"""
		Check for successful indexing.
		"""

		index_fields = ['date', 'journal', 'authors']
		corpus = Corpus(self.papers, index_by='wosid')
		
		for field in index_fields:
			corpus.index(field)
			self.assertIn(field, corpus.indices,
                          '{0} not indexed.'.format(field))
			
			expected = len(set([o for p in corpus.papers
							    for o in _iterable(getattr(p, field))]))
			self.assertEqual(len(corpus.indices[field]), expected,
							 'Index for {0} is the wrong size.'.format(field))



if __name__ == '__main__':
    unittest.main()