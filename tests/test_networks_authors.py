from settings import *

import unittest
import random

import networkx
from tethne.readers import wos
from tethne.networks import authors

class TestCoauthors(unittest.TestCase):
    def setUp(self):
        self.papers = wos.read(datapath + '/wos.txt')

    def test_coauthors(self):
        coauthors = authors.coauthors(self.papers)

        self.assertIsInstance(coauthors, networkx.Graph)
        self.assertGreater(len(coauthors.nodes()), 0)
        self.assertGreater(len(coauthors.edges()), 0)

    def test_coauthors_auuri(self):
        for paper in self.papers:
            Nauthors = len(paper.authors())
            paper['auuri'] = [ random.randint(0,200) for x in xrange(Nauthors) ]
        coauthors = authors.coauthors(self.papers, auuri=True)

        self.assertIsInstance(coauthors, networkx.Graph)
        self.assertGreater(len(coauthors.nodes()), 0)
        self.assertGreater(len(coauthors.edges()), 0)

    def test_coauthors_geocode(self):
        coauthors = authors.coauthors(self.papers, geocode=True)

        self.assertIsInstance(coauthors, networkx.Graph)
        self.assertGreater(len(coauthors.nodes()), 0)
        self.assertGreater(len(coauthors.edges()), 0)
        self.assertIn('latitude', coauthors.nodes(data=True)[0][1])

if __name__ == '__main__':
    unittest.main()