import sys
sys.path.append('../tethne')

import unittest
from tethne.readers.wos import WoSParser, read
from tethne import Corpus, Paper

datapath = './tests/data/refactor_data/wos.txt'


class TestWoSParser(unittest.TestCase):
	def test_read(self):
		corpus = read(datapath)
		self.assertIsInstance(corpus, Corpus)


	def test_read_nocorpus(self):
		papers = read(datapath, corpus=False)
		self.assertIsInstance(papers, list)
		self.assertIsInstance(papers[0], Paper)


	def test_parse(self):
		parser = WoSParser(datapath)
		parser.parse()
	
		# Check data types for the most common fields.
		derror = "{0} should be {1}, but is {2}"
		for entry in parser.data:
			self.assertIsInstance(entry.date, int,
								  derror.format('date', 'int', type(entry.date)))
			self.assertIsInstance(entry.authors_full, list,
								  derror.format('authors_full', 'list', 
												type(entry.authors_full)))
			self.assertIsInstance(entry.journal, str,
								  derror.format('journal', 'str', type(entry.journal)))
			self.assertIsInstance(entry.abstract, str,
								  derror.format('abstract', 'str', type(entry.abstract)))
			self.assertIsInstance(entry.authorKeywords, list,
								  derror.format('authorKeywords', 'list', 
												type(entry.authorKeywords)))
			self.assertIsInstance(entry.keywordsPlus, list,
								  derror.format('keywordsPlus', 'list', 
												type(entry.keywordsPlus)))	
			self.assertIsInstance(entry.doi, str,
								  derror.format('doi', 'str', type(entry.doi)))
			self.assertIsInstance(entry.volume, str,
								  derror.format('volume', 'str', type(entry.volume)))		
	
		# Check integrity of tag-to-field mapping.
		for tag, attr in parser.tags.iteritems():
			self.assertFalse(hasattr(entry, tag), 
							 ' '.join(['Tag-to-field translation is corrupted.',
									   '{0} should map to'.format(tag),
									   '{0}, but does not.'.format(attr)]))

		# Check number of records.
		self.assertEqual(len(parser.data), 10, 
						 'Expected 10 entries, but found {0}.'.format(len(parser.data)))

		self.assertTrue(hasattr(parser.data[0], 'citedReferences'))
		for cr in parser.data[0].citedReferences:
			self.assertTrue(hasattr(cr, 'date'))
			if cr.date:
				self.assertIsInstance(cr.date, int)
			self.assertTrue(hasattr(cr, 'journal'))


if __name__ == '__main__':
    unittest.main()