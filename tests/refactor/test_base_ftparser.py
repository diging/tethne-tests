import sys
sys.path.append('../tethne')

import unittest
from tethne.base.ftparser import FTParser

datapath = './tests/data/refactor_data/test.ft'

class TestFTParser(unittest.TestCase):
	def test_badpath(self):
		"""
		If an invalid/non-existant path is passed to the constructor, should raise
		an ``IOError``.
		"""
		
		with self.assertRaises(IOError):
			parser = FTParser('/this/path/doesnt/exist')
			
	def test_start(self):
		"""
		Parser should advance to the first start tag, and instantiate the first data 
		entry.
		"""

		parser = FTParser(datapath, autostart=False)
		parser.start()
		
		self.assertEqual(parser.start_tag, parser.current_tag, 'Cannot identify start.')
		self.assertEqual(len(parser.data), 1, 'First data entry not instantiated.')
		self.assertIsInstance(parser.data[0], parser.entry_class, 
							  ' '.join(['Datum is a {0}'.format(type(parser.data[0])),
							 		    ', expected an {0}'.format(parser.entry_class)]))
		
	def test_next(self):
		"""
		``next`` should return the first line of data.
		"""

		parser = FTParser(datapath)		
		tag, data = parser.next()

		self.assertEqual(tag, 'FI')
		
	def test_handle(self):
		"""
		``handle`` should store the first line of data in the first data entry.
		"""

		parser = FTParser(datapath)		
		tag, data = parser.next()
		parser.handle(tag, data)		

		self.assertEqual(len(parser.data), 1)
		self.assertTrue(hasattr(parser.data[0], tag),
					    ' '.join(['Data line not handled correctly. Tag `{0}` should be',
					    		  'an attribute of the first data entry.'.format(tag)]))

	def test_parse(self):
		parser = FTParser(datapath)		
		parser.parse()
		
		self.assertEqual(len(parser.data[0].TH), 3, 
						 ' '.join(['Multi-line fields are not handled properly. Fields',
						 		   'with multiple lines should be parsed as a list or',
						 		   'array with one value per line.']))
		
		self.assertEqual(len(parser.data), 2,
						 'Expected 2 data entries, found {0}'.format(len(parser.data)))
			
if __name__ == '__main__':
    unittest.main()