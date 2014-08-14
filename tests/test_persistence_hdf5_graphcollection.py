from settings import *

import unittest

import warnings

from tethne.readers import wos, dfr
from tethne.classes import Corpus, GraphCollection
from tethne.networks.authors import coauthors
from tethne.persistence.hdf5.graphcollection import *
from tethne.persistence.hdf5.util import get_h5file, get_or_create_group

import os

import networkx as nx
from scipy.sparse import coo_matrix

dfrdatapath = '{0}/dfr'.format(datapath)
ngrams = dfr.ngrams(dfrdatapath, 'uni')
papers = dfr.read(dfrdatapath)

D = Corpus(papers, index_by='doi')
D.slice('date', method='time_period', window_size=1)

class TestSparseArray(unittest.TestCase):
    def setUp(self):
        self.I = [0,0,1,2,2,3,4,5,5]
        self.J = [1,2,5,3,4,1,8,4,3]
        self.K = [1,1,1,1,2,3,2,1,1]

        self.h5name = 'HDF5Graph_test.h5'
        self.h5path = temppath + '/' + self.h5name
        self.h5file,a,b = get_h5file('HDF5Graph', self.h5path)
        self.group = get_or_create_group(self.h5file, 'testgroup')
        self.sparse = SparseArray(  self.h5file, self.group, 'sparse',
                                  self.I, self.J, self.K  )

    def test_len(self):
        self.assertEqual(len(self.sparse), len(self.I))
    
    def test_shape(self):
        A = coo_matrix(self.K, (self.I, self.J)).tocsr()
        
        self.assertEqual(A.shape, self.sparse.shape)
        
    def test_num_edges(self):
        self.assertEqual(self.sparse.num_edges(), 9)

    def test_getitem(self):
        self.assertEqual(self.sparse[3,1], 3)

    def test_get_neighbors(self):
        self.assertEqual(set(self.sparse.get_neighbors(1)), set([0,3,5]) )

    def test_get_edges(self):
        self.assertEqual(   self.sparse.get_edges(data=True),
                            zip(self.I, self.J, self.K) )
    
    def test_nodes(self):
        expected = [0,1,2,3,4,5,8]
        self.assertEqual(set(self.sparse.nodes()), set(expected))
        self.assertEqual(len(self.sparse.nodes()), len(expected))

    def tearDown(self):
        os.remove(self.h5path)

class TestHDF5NodeAttributes(unittest.TestCase):
    def setUp(self):
        self.h5name = 'HDF5Graph_test.h5'
        self.h5path = temppath + '/' + self.h5name
        self.h5file,a,b = get_h5file('HDF5Graph', self.h5path)
        self.group = get_or_create_group(self.h5file, 'testgroup')
    
        self.attribs = {
            0: {
                'size': 5,
                'name': 'bob',
            },
            1: {
                'size': 10,
                'name': 'alice',
            },
        }
        
        self.node = HDF5NodeAttributes(self.h5file, self.group, self.attribs)
        self.graph = Graph()
        for node, attribs in self.attribs.iteritems():
            self.graph.add_node(node, attribs)
                
    def test_getitem(self):
        self.assertEqual(self.graph.node[0], self.node[0])
    
    def test_get_nodes(self):
        self.assertEqual(   self.graph.nodes(data=True),
                            self.node.get_nodes(data=True)  )
    
    def test_items(self):
        self.assertEqual(self.graph.node.items(), self.node.items())

    def test_str(self):
        self.assertEqual(str(self.node), str(self.graph.node))

    def tearDown(self):
        os.remove(self.h5path)

class TestHDF5Graph(unittest.TestCase):
    def setUp(self):
        self.h5name = 'HDF5Graph_test.h5'
        self.h5path = temppath + '/' + self.h5name
        self.h5file,a,b = get_h5file('HDF5Graph', self.h5path)
        self.group = get_or_create_group(self.h5file, 'testgroup')

        g = nx.Graph()
        g.add_edge(0,1)
        g.add_edge(1,2, weight=5)
        g.add_edge(5,0, {'weight':3, 'girth':'wtf'})
        g.add_node(0, {'size':0.5, 'label':'bob'})
        self.g = g
    
        self.hg = HDF5Graph(self.h5file, self.group, 'testGraph', g)

    def test_edges(self):
        self.assertEqual(self.hg.edges(), self.g.edges())
    
    def test_nodes(self):
        self.assertEqual(self.hg.nodes(), self.g.nodes())
    
    def test_edges_data(self):
        self.assertEqual(self.hg.edges(data=True), self.g.edges(data=True))
    
    def test_nodes_data(self):
        self.assertEqual(self.hg.nodes(data=True), self.g.nodes(data=True))
    
    def test_len(self):
        self.assertEqual(len(self.hg), len(self.g))
    
    def test_getitem(self):
        self.assertEqual(self.hg[0], self.g[0])
    
    def test_node(self):
        self.assertEqual(self.hg.node[0], self.g.node[0])
    
    def test_edge(self):
        self.assertEqual(self.hg.edge[0], self.g.edge[0])
    
    def test_betweenness(self):
        hg_bc = nx.betweenness_centrality(self.hg)
        g_bc = nx.betweenness_centrality(self.g)
        self.assertEqual(hg_bc, g_bc)
    
    def test_closeness(self):
        hg_bc = nx.closeness_centrality(self.hg)
        g_bc = nx.closeness_centrality(self.g)
        self.assertEqual(hg_bc, g_bc)
    
    def test_edge_betweenness(self):
        hg_bc = nx.edge_betweenness(self.hg)
        g_bc = nx.edge_betweenness(self.g)
        self.assertEqual(hg_bc, g_bc)

    def test_to_graph(self):
        g = self.hg.to_graph()

        self.assertEqual(g.node.items(), self.hg.node.items())
        self.assertEqual(g.node.items(), self.g.node.items())

        self.assertEqual(g.edge.items(), self.hg.edge.items())
        self.assertEqual(g.edge.items(), self.g.edge.items())

        self.assertEqual(g.nodes(data=True), self.hg.nodes(data=True))
        self.assertEqual(g.nodes(data=True), self.g.nodes(data=True))
        self.assertEqual(g.edges(data=True), self.hg.edges(data=True))
        self.assertEqual(g.edges(data=True), self.g.edges(data=True))

    def test_add_node(self):
        self.assertRaises(NotImplementedError, self.hg.add_node, 20)

    def test_add_edge(self):
        self.assertRaises(NotImplementedError, self.hg.add_edge, 20, 21)

    def test_get_edges(self):
        self.assertEqual(self.g.edges(), self.hg.edge.get_edges())
        self.assertEqual(   self.g.edges(data=True),
                            self.hg.edge.get_edges(data=True)   )

    def test_edge(self):
        self.assertEqual(str(self.g.edge), str(self.hg.edge))
        self.assertEqual(self.g.edge.items(), self.hg.edge.items())

    def tearDown(self):
        os.remove(self.h5path)

class TestGraphCollection(unittest.TestCase):
    def setUp(self):
        self.h5name = 'HDF5GraphCollection_test.h5'
        self.h5path = temppath + '/' + self.h5name
        self.h5file,a,b = get_h5file('HD5GraphCollection', self.h5path)
    
        self.G_ = GraphCollection()

        for k,v in D.get_slices('date', papers=True).iteritems():
            self.G_[k] = coauthors(v)

        self.G = HDF5GraphCollection(self.G_, datapath=self.h5path)

    def test_to_hdf5(self):
        HG = HDF5GraphCollection(datapath=self.h5path)
        self.assertEqual(HG.graphs.keys(), self.G_.graphs.keys())
        for key, graph in HG.graphs.iteritems():
            self.assertEqual(   set(graph.nodes()),
                                set(self.G_[key].nodes())   )
            self.assertEqual(   set(graph.edges()),
                                set(self.G_[key].edges())   )

    def test_open(self):
        dpath = self.G.path

        G2 = HDF5GraphCollection(GraphCollection(), dpath)

        self.assertEqual(set(G2.nodes()), set(self.G.nodes()))
        self.assertEqual(set(G2.edges()), set(self.G.edges()))
        self.assertEqual(len(G2.node_index), len(self.G.node_index))
        self.assertEqual(G2.node_distribution(), self.G.node_distribution())
        self.assertEqual(G2.edge_distribution(), self.G.edge_distribution())
        self.assertEqual(   G2.attr_distribution()[0],
                            self.G.attr_distribution()[0]  )
        self.assertEqual(   G2.attr_distribution()[1],
                            self.G.attr_distribution()[1]  )


    def test_from_hdf5(self):
        HG = from_hdf5(self.G)
        self.assertEqual(set(HG.nodes()), set(self.G.nodes()))
        self.assertEqual(set(HG.edges()), set(self.G.edges()))
        self.assertEqual(len(HG.node_index), len(self.G.node_index))
        self.assertEqual(HG.node_distribution(), self.G.node_distribution())
        self.assertEqual(HG.edge_distribution(), self.G.edge_distribution())
        self.assertEqual(   HG.attr_distribution()[0],
                            self.G.attr_distribution()[0]  )
        self.assertEqual(   HG.attr_distribution()[1],
                            self.G.attr_distribution()[1]  )

    def test_nodes(self):
        """
        should return a list of integers
        """
        
        pcgpath = cg_path + 'persistence.hdf5.HDF5GraphCollection.nodes.png'
        with Profile(pcgpath):
            nodes = self.G.nodes()

        self.assertIsInstance(nodes, list)
        self.assertIsInstance(nodes[0], int)
        self.assertEqual(set(self.G.nodes()), set(self.G_.nodes()))

    def test_edges(self):
        """
        should return a list of (int,int) tuples.
        """
        
        pcgpath = cg_path + 'persistence.hdf5.HDF5GraphCollection.edges.png'
        with Profile(pcgpath):
            edges = self.G.edges()

        self.assertIsInstance(edges, list)
        self.assertIsInstance(edges[0], tuple)
        self.assertIsInstance(edges[0][0], int)
        self.assertIsInstance(edges[0][1], int)
        for e in self.G.edges():
            self.assertTrue(
                e in self.G_.edges() or (e[1],e[0]) in self.G_.edges()  )

    def test_index_graph(self):
        """
        index should be as large as set of unique nodes in all graphs
        """

        unodes = set([ n for g in self.G.graphs.values() for n in g.nodes() ])
        self.assertEqual(len(self.G.node_index), len(unodes))
        self.assertEqual(len(self.G.node_index), len(self.G_.node_index))

    def test__plot(self):
        """
        :func:`._plot` should return a :class:`matplotlib.figure.Figure`
        """

        xvalues = range(0, 10)
        yvalues = range(0, 10)
        
        pcgpath = cg_path + 'persistence.hdf5.HDF5GraphCollection._plot.png'
        with Profile(pcgpath):
            fig = self.G._plot((xvalues, yvalues), 'test')

    def test_node_distribution(self):
        """
        :func:`.node_distribution` should return a tuple of ([keys],[values]).
        """

        pcgpath = cg_path + 'persistence.hdf5.HDF5GraphCollection.node_distribution.png'
        with Profile(pcgpath):
            data = self.G.node_distribution()

        self.assertIsInstance(data, tuple)
        self.assertIsInstance(data[0], list)
        self.assertIsInstance(data[1], list)
        self.assertEqual(len(data[0]), len(data[1]))
        self.assertEqual(data, self.G_.node_distribution())

    def test_plot_node_distribution(self):
        """
        :func:`.plot_node_distribution` should return a
        :class:`matplotlib.figure.Figure`
        """

        pcgpath = cg_path + 'persistence.hdf5.HDF5GraphCollection.plot_node_distribution.png'
        with Profile(pcgpath):
            fig = self.G.plot_node_distribution()

#        self.assertIsInstance(fig, matplotlib.figure.Figure)

    def test_edge_distribution(self):
        """
        :func:`.edge_distribution` should return a tuple of ([keys],[values]).
        """

        pcgpath = cg_path + 'persistence.hdf5.HDF5GraphCollection.edge_distribution.png'
        with Profile(pcgpath):
            data = self.G.edge_distribution()

        self.assertIsInstance(data, tuple)
        self.assertIsInstance(data[0], list)
        self.assertIsInstance(data[1], list)
        self.assertEqual(len(data[0]), len(data[1]))
        self.assertEqual(data, self.G_.edge_distribution())

    def test_plot_edge_distribution(self):
        """
        :func:`.plot_edge_distribution` should return a
        :class:`matplotlib.figure.Figure`
        """

        pcgpath = cg_path + 'persistence.hdf5.HDF5GraphCollection.plot_edge_distribution.png'
        with Profile(pcgpath):
            fig = self.G.plot_edge_distribution()

#        self.assertIsInstance(fig, matplotlib.figure.Figure)

    def test_attr_distribution(self):
        """
        :func:`.attr_distribution` should return a tuple of ([keys],[values]).
        """

        pcgpath = cg_path + 'persistence.hdf5.HDF5GraphCollection.attr_distribution.png'
        with warnings.catch_warnings(record=False) as w:
            warnings.simplefilter('ignore') # Some slices have no values.
            with Profile(pcgpath):
                data = self.G.attr_distribution()

        self.assertIsInstance(data, tuple)
        self.assertIsInstance(data[0], list)
        self.assertIsInstance(data[1], list)
        self.assertEqual(len(data[0]), len(data[1]))
        self.assertEqual(data[0], self.G_.attr_distribution()[0])
        self.assertEqual(data[1], self.G_.attr_distribution()[1])

    def test_plot_attr_distribution(self):
        """
        :func:`.plot_attr_distribution` should return a
        :class:`matplotlib.figure.Figure`
        """

        pcgpath = cg_path + 'persistence.hdf5.HDF5GraphCollection.plot_attr_distribution.png'
        with warnings.catch_warnings(record=False) as w:
            warnings.simplefilter('ignore') # Some slices have no values.
            with Profile(pcgpath):
                fig = self.G.plot_attr_distribution()

    def tearDown(self):
        os.remove(self.h5path)

if __name__ == '__main__':
    unittest.main()