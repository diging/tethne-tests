from settings import *
from sensitive import *
import tempfile
from tethne.readers import dspace
from tethne.services.dspace import DSpace
from tethne import Paper, Corpus

import os

import unittest

collectionid = 43
endpoint = 'https://dstools.hpsrepository.asu.edu/rest/'

class TestReaderDSpace(unittest.TestCase):
#    def test_download_collection(self):
#        path = temppath + '/dspace'
#        items, bitstreams, outpath = dspace.download_collection(publickey, privatekey, endpoint, collectionid, path)
#        
#        self.assertIsInstance(items, list)
#        self.assertGreater(len(items), 0)
#        self.assertEqual(bitstreams, None)  # Didn't ask for bitstreams.
#        self.assertEqual(path, outpath)
        
    def test_read(self):
        metapath = '/Users/erickpeirson/Desktop/genecology_texts/metadata.pickle'
        papers = dspace.read(metapath)
        self.assertIsInstance(papers, list)
        self.assertGreater(len(papers), 0)
        self.assertIsInstance(papers[0], Paper)

    def test_read_corpus(self):
        metapath = '/Users/erickpeirson/Desktop/genecology_texts/metadata.pickle'
        corpus = dspace.read_corpus(metapath)
        self.assertIsInstance(corpus, Corpus)
        self.assertGreater(len(corpus.all_papers()), 0)        
                
    def test_add_bitstreams(self):
        metapath = '/Users/erickpeirson/Desktop/genecology_texts/metadata.pickle'
        bitstreampath = '/Users/erickpeirson/Desktop/genecology_texts/bitstreams.pickle'
        corpus = dspace.read_corpus(metapath)

        corpus = dspace.add_bitstreams(corpus, bitstreampath)
        
        self.assertIsInstance(corpus, Corpus)
        self.assertGreater(len(corpus.all_papers()), 0)
        self.assertGreater(len(corpus.all_papers()[0]['contents']), 0)             
    
    def test_read_corpus_bitstreams(self):
        metapath = '/Users/erickpeirson/Desktop/genecology_texts/metadata.pickle'
        bitstreampath = '/Users/erickpeirson/Desktop/genecology_texts/bitstreams.pickle'
        
        corpus = dspace.read_corpus(metapath, bitstreampath)
        self.assertIsInstance(corpus, Corpus)
        self.assertGreater(len(corpus.all_papers()), 0)
        self.assertGreater(len(corpus.all_papers()[0]['contents']), 0)
        
        corpus.contents_to_features()

if __name__ == '__main__':
    unittest.main()
