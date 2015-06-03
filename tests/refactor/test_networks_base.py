import sys
sys.path.append('../tethne')

import unittest

from tethne.networks.base import cooccurrence, coupling
from tethne.classes.corpus import Corpus
from tethne.readers.wos_refactor import WoSParser

import networkx as nx

datapath = './tests/data/refactor_data/wos.txt'

class TestBaseNeworkMethods(unittest.TestCase):
    def setUp(self):
        papers = WoSParser(datapath).parse()
        self.corpus = Corpus(papers, index_features=['authors', 'citations'])

    def test_coocurrence(self):
        g = cooccurrence(self.corpus, 'authors')

        self.assertIsInstance(g, nx.Graph)
        self.assertGreater(len(g.nodes()), 0)
        self.assertGreater(len(g.edges()), 0)

    def test_coupling(self):
        g = coupling(self.corpus, 'citations')

        self.assertIsInstance(g, nx.Graph)
        self.assertGreater(len(g.nodes()), 0)
        self.assertGreater(len(g.edges()), 0)
        for s,t,attrs in g.edges(data=True):
            self.assertEqual(len(attrs['features']), attrs['weight'])

    def test_coupling_min_weight(self):
        """
        Limit edges to weight >= 3.
        """

        min_weight = 3
        g = coupling(self.corpus, 'citations')
        g2 = coupling(self.corpus, 'citations', min_weight=min_weight)

        self.assertIsInstance(g, nx.Graph)
        self.assertGreater(len(g2.nodes()), 0)
        self.assertGreater(len(g.nodes()), len(g2.nodes()))
        self.assertGreater(len(g2.edges()), 0)
        self.assertGreater(len(g.edges()), len(g2.edges()))

        for s, t, attrs in g2.edges(data=True):
            self.assertGreaterEqual(attrs['weight'], min_weight)

if __name__ == '__main__':
    unittest.main()
    