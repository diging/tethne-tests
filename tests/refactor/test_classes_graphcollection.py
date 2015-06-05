import sys
sys.path.append('../tethne')

import unittest

import networkx as nx

from tethne.classes.graphcollection_refactor import GraphCollection


datapath = './tests/data/refactor_data/wos.txt'


class TestGraphCollectionCreation(unittest.TestCase):
    def test_init(self):
        G = GraphCollection()

        self.assertTrue(hasattr(G, 'master_graph'))
        self.assertTrue(hasattr(G, 'node_index'))
        self.assertTrue(hasattr(G, 'node_lookup'))
        self.assertTrue(hasattr(G, 'graphs_containing'))

    def test_init_directed(self):
        G = GraphCollection(directed=True)
        graph = nx.DiGraph()
        graph.add_edge('A', 'B', c='d')
        graph.add_edge('B', 'C', c='e')
        graph.node['A']['bob'] = 'dole'
        graph_name = 'test'

        graph2 = nx.DiGraph()
        graph2.add_edge('A', 'B', c='d')
        graph2.add_edge('D', 'C', c='f')
        graph2.node['A']['bob'] = 'dole'
        graph2_name = 'test2'

        G.add(graph_name, graph)
        G.add(graph2_name, graph2)

        # The indexed graph is directed-isomorphic to the original graph.
        matcher = nx.isomorphism.DiGraphMatcher(G[graph_name], graph)
        self.assertTrue(matcher.is_isomorphic)
        matcher = nx.isomorphism.DiGraphMatcher(G[graph2_name], graph2)
        self.assertTrue(matcher.is_isomorphic)

    def test_index(self):
        """
        Index a :class:`networkx.Graph`\, but don't add it to the
        :class:`.GraphCollection`\.
        """
        G = GraphCollection()
        graph = nx.Graph()
        graph.add_edge('A', 'B', c='d')
        graph.add_edge('B', 'C', c='e')
        graph_name = 'test'

        igraph = G.index(graph_name, graph)

        # The number of nodes and edges is unchanged.
        self.assertEqual(len(graph.nodes()), len(igraph.nodes()))
        self.assertEqual(len(graph.edges()), len(igraph.edges()))

        # The indexed graph is isomorphic to the original graph.
        self.assertTrue(nx.isomorphism.is_isomorphic(igraph, graph))

        # Can find original node names in the correct graphs.
        for n in graph.nodes():
            self.assertIn(n, G.node_lookup)
            self.assertIn(graph_name, G.graphs_containing[n])

    def test_add(self):
        """
        Add a :class:`networkx.Graph` to the :class:`.GraphCollection`\.
        """
        G = GraphCollection()
        graph = nx.Graph()
        graph.add_edge('A', 'B', c='d')
        graph.add_edge('B', 'C', c='e')
        graph.node['A']['bob'] = 'dole'
        graph_name = 'test'

        G.add(graph_name, graph)

        # Graph is added to the GraphCollection.
        self.assertIn(graph_name, G)

        # The graph name should be added to edge attributes in the
        #  master_graph.
        for s, t, attrs in G.master_graph.edges(data=True):
            self.assertIn('graph', attrs)
            self.assertEqual(attrs['graph'], graph_name)

        # The number of nodes and edges is unchanged.
        self.assertEqual(len(graph.nodes()), len(G[graph_name].nodes()))
        self.assertEqual(len(graph.edges()), len(G[graph_name].edges()))

        # The indexed graph is isomorphic to the original graph.
        self.assertTrue(nx.isomorphism.is_isomorphic(G[graph_name], graph))

        # Can find original node names in the correct graphs.
        for n, attrs in graph.nodes(data=True):
            self.assertIn(n, G.node_lookup)
            self.assertIn(graph_name, G.graphs_containing[n])

            i = G.node_lookup[n]
            for k, v in attrs.iteritems():
                self.assertIn(k, G.master_graph.node[i])
                self.assertIn(graph_name, G.master_graph.node[i][k])
                self.assertEqual(v, G.master_graph.node[i][k][graph_name])

        # Should raise a ValueError if name has already been used.
        with self.assertRaises(ValueError):
            G.add(graph_name, nx.Graph())


class TestGraphCollectionMethods(unittest.TestCase):
    def setUp(self):
        self.G = GraphCollection()
        self.graph = nx.Graph()
        self.graph.add_edge('A', 'B', c='d')
        self.graph.add_edge('B', 'C', c='e')
        self.graph.node['A']['bob'] = 'dole'
        graph_name = 'test'

        self.graph2 = nx.Graph()
        self.graph2.add_edge('A', 'B', c='d')
        self.graph2.add_edge('D', 'C', c='f')
        self.graph2.node['A']['bob'] = 'dole'
        graph2_name = 'test2'

        self.G.add(graph_name, self.graph)
        self.G.add(graph2_name, self.graph2)

    def test_nodes(self):
        """
        :meth:`.GraphCollection.nodes` should behave like
        :meth:`networkx.Graph.nodes`\, but return values for all of the
        :class:`networkx.Graph`\s in the :class:`.GraphCollection`\.
        """

        joint_nodes = set(self.graph.nodes()) | set(self.graph2.nodes())
        self.assertEqual(len(self.G.nodes(data=True)), len(joint_nodes))
        self.assertTrue(hasattr(self.G.nodes(), '__iter__'),
                        "GraphCollection.nodes() should be iterable.")

        self.assertIsInstance(self.G.nodes(data=True)[0], tuple,
                              "Should return a 2-tuple when data=True")
        self.assertEqual(len(self.G.nodes(data=True)[0]), 2,
                         "Should return a 2-tuple when data=True")

    def test_edges(self):
        """
        :meth:`.GraphCollection.edges` should behave like
        :meth:`networkx.Graph.edges`\, but return values for all of the
        :class:`networkx.Graph`\s in the :class:`.GraphCollection`\.
        """

        self.assertIsInstance(self.G.edges()[0], tuple,
                              "Should return a 2-tuple when data=False")
        self.assertEqual(len(self.G.edges()[0]), 2,
                         "Should return a 3-tuple when data=False")

        self.assertIsInstance(self.G.edges(data=True)[0], tuple,
                              "Should return a 3-tuple when data=True")
        self.assertEqual(len(self.G.edges(data=True)[0]), 3,
                         "Should return a 3-tuple when data=True")

    def test_order(self):
        """
        :meth:`.GraphCollection.order` should return the number of nodes in
        the :class:`.GraphCollection`\. If `piecewise` is True, should return a
        dict containing the order of each :class:`networkx.Graph` in the
        :class:`.GraphCollection`\.
        """

        joint_nodes = set(self.graph.nodes()) | set(self.graph2.nodes())
        self.assertEqual(self.G.order(), len(joint_nodes))

        self.assertIsInstance(self.G.order(piecewise=True), dict,
                              "order() should return a dict if piecewise=True")
        self.assertIn('test', self.G.order(piecewise=True),
                      ''.join(["order(piecewise=True) should return a dict",
                               " with graph names as keys"]))
        self.assertIn('test2', self.G.order(piecewise=True),
                      ''.join(["order(piecewise=True) should return a dict",
                               " with graph names as keys"]))

    def test_size(self):
        """
        :meth:`.GraphCollection.size` should return the number of nodes in the
        :class:`.GraphCollection`\. If `piecewise` is True, should return a
        dict containing the size of each :class:`networkx.Graph` in the
        :class:`.GraphCollection`\.
        """

        N_edges = len(self.graph.edges()) + len(self.graph2.edges())
        self.assertEqual(self.G.size(), N_edges)

        self.assertIsInstance(self.G.size(piecewise=True), dict,
                              "size() should return a dict if piecewise=True")
        self.assertIn('test', self.G.size(piecewise=True),
                      ''.join(["size(piecewise=True) should return a dict",
                               " with graph names as keys"]))
        self.assertIn('test2', self.G.size(piecewise=True),
                      ''.join(["size(piecewise=True) should return a dict",
                               " with graph names as keys"]))


if __name__ == '__main__':
    unittest.main()
