from settings import *

import tethne.readers as rd
import tethne.writers as wr
import tethne.utilities as util
import unittest
import networkx as nx
import os

class TestCorpusWriter(unittest.TestCase):
    """
    Tests for :mod:`tethne.writers.corpora`\.
    """

    def setUp(self):
        self.corpus = rd.dfr.read_corpus(datapath + '/dfr', features=['uni'])
        meta = ['date', 'jtitle', 'atitle']
        self.metadata = ( meta, { p: { k:paper[k] for k in meta }
                           for p,paper in self.corpus.papers.iteritems() } )

    def test_to_documents(self):
        pkey = self.metadata[1].keys()[5]
        pkey2 = self.metadata[1].keys()[6]
        mkey = self.metadata[0][2]
        
        del self.metadata[1][pkey][mkey]
        del self.metadata[1][pkey2]
    
        dpath, metapath = wr.corpora.to_documents(
                            temppath + '/corpus',
                            self.corpus.features['unigrams']['features'],
                            metadata = self.metadata,
                            vocab = self.corpus.features['unigrams']['index'] )
        self.assertIsInstance(dpath, str)
        self.assertIsInstance(metapath, str)

if __name__ == '__main__':
    unittest.main()