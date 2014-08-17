from settings import *
import unittest

from tethne.readers import wos
from tethne.networks import papers
from tethne.writers import graph

import os

import xml.etree.ElementTree as ET

class TestGraphMLWriter(unittest.TestCase):
    def setUp(self):
        self.papers = wos.read(datapath+'/wos.txt')
        self.citation,self.internal = papers.direct_citation(self.papers, node_attribs=['date'])

    def test_date_integer(self):
        graph.to_graphml(self.internal, outpath+'/test_citation_graph.graphml')
        root = ET.parse(outpath+'/test_citation_graph.graphml').getroot()
        keys = root.findall('.//{http://graphml.graphdrawing.org/xmlns}key')
        for key in keys:
            if key.attrib['attr.name'] == 'date':
                self.assertEqual(key.attrib['attr.type'], 'int')

        os.remove(outpath+'/test_citation_graph.graphml')


if __name__ == '__main__':
    unittest.main()