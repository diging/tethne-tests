from settings import *
from sensitive import *

import unittest

from tethne.services.dspace import DSpace
    
collectionid = 43
endpoint = 'https://dstools.hpsrepository.asu.edu/rest/'


class TestDSpace(unittest.TestCase):
    def setUp(self):
        self.service = DSpace(publickey, privatekey, endpoint)        
        
    def test_list_collections(self):
        result = self.service.list_collections()
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result, list)
        
    def test_list_items(self):
        result = self.service.list_items(collectionid)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result, list)
    
    def test_get_bitstream_save(self):
        result = self.service.get_bitstream(22862, temppath+'/22862.txt')
        self.assertIsInstance(result, file)

    def test_get_bitstream_contents(self):
        result = self.service.get_bitstream(22862)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        
        

if __name__ == '__main__':
    unittest.main()


