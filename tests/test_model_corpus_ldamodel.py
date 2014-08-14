from settings import *

import unittest

from tethne.model.corpus import ldamodel

import numpy

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.dt_path = '{0}/mallet/dt.dat'.format(datapath)
        self.wt_path = '{0}/mallet/wt.dat'.format(datapath)
        self.meta_path = '{0}/mallet/tethne_meta.csv'.format(datapath)
        self.loader = ldamodel.MALLETLoader(self.dt_path, self.wt_path, self.meta_path)
    

    def test__handle_top_doc(self):
        """
        :func:`._handle_top_doc` should return a Numpy matrix with non-zero
        values, and a `doc_index` that maps indices to document ids.
        """
    
        pcgpath = cg_path + 'model.corpus.ldamodel.MALLETLoader._handle_top_doc.png'
        with Profile(pcgpath):
            td, doc_index = self.loader._handle_top_doc()#self.dt_path)

        self.assertIsInstance(td, numpy.matrixlib.defmatrix.matrix)
        self.assertEqual(td.shape, (241,20))
        self.assertGreater(numpy.sum(td), 0.)
        
        self.assertIsInstance(doc_index, dict)
        self.assertIsInstance(doc_index.keys()[0], int)
        self.assertIsInstance(doc_index.values()[0], str)
        self.assertEqual(len(doc_index), td.shape[0])
        
    def test__handle_word_top(self):
        """
        :func:`._handle_word_top` should return a Numpy matrix with non-zero
        values, and a `vocabulary` dict mapping indices to words.
        """
    
        pcgpath = cg_path + 'model.corpus.ldamodel.MALLETLoader._handle_word_top.png'
        with Profile(pcgpath):
            wt, vocabulary = self.loader._handle_word_top()#self.wt_path)

        self.assertIsInstance(wt, numpy.matrixlib.defmatrix.matrix)
        self.assertEqual(wt.shape, (20, 51290))
        self.assertGreater(numpy.sum(wt), 0.)
        
        self.assertIsInstance(vocabulary, dict)
        self.assertIsInstance(vocabulary.keys()[0], int)
        self.assertIsInstance(vocabulary.values()[0], str)
        self.assertEqual(len(vocabulary), wt.shape[1])
        
    def test__handle_metadata(self):
        """
        :func:`._handle_metadata` should return a dictionary mapping int : dict.
        Values (dict) should contain an `'id'` field.
        """
        self.loader._handle_top_doc()
    
        pcgpath = cg_path + 'model.corpus.ldamodel.MALLETLoader._handle_metadata.png'
        with Profile(pcgpath):
            meta = self.loader._handle_metadata()#self.meta_path)
            
        self.assertIsInstance(meta, dict)
        self.assertEqual(len(meta), 241)
        self.assertIsInstance(meta.keys()[0], int)
        self.assertIsInstance(meta.values()[0], dict)
        self.assertIsInstance(meta.values()[0]['id'], str)

    def test_load(self):
        """
        :func:`.from_mallet` should return a :class:`.LDAModel`.
        """
        
        pcgpath = cg_path + 'model.corpus.ldamodel.MALLETLoader.load.png'
        with Profile(pcgpath):
            model = self.loader.load()

        self.assertIsInstance(model, ldamodel.LDAModel)
        self.assertEqual(model.Z, 20)
        self.assertEqual(model.M, 241)
        self.assertEqual(model.W, 51290)

    def test_from_mallet(self):
        """
        :func:`.from_mallet` should return a :class:`.LDAModel`.
        """
        
        pcgpath = cg_path + 'model.corpus.ldamodel.from_mallet.png'
        with Profile(pcgpath):
            model = ldamodel.from_mallet(   self.dt_path,
                                            self.wt_path,
                                            self.meta_path  )

        self.assertIsInstance(model, ldamodel.LDAModel)
        self.assertEqual(model.Z, 20)
        self.assertEqual(model.M, 241)
        self.assertEqual(model.W, 51290)

class TestLDAModel(unittest.TestCase):
    def setUp(self):
        self.dt_path = '{0}/mallet/dt.dat'.format(datapath)
        self.wt_path = '{0}/mallet/wt.dat'.format(datapath)
        self.meta_path = '{0}/mallet/tethne_meta.csv'.format(datapath)
        self.model = ldamodel.from_mallet(  self.dt_path,
                                            self.wt_path,
                                            self.meta_path  )

    def test_list_topic(self):
        """
        :func:`.list_topic` should yield a list with ``Nwords`` words.
        """
        Nwords = 10
        
        pcgpath = cg_path + 'model.corpus.ldamodel.LDAModel.list_topic.png'
        with Profile(pcgpath):
            result = self.model.list_topic(0, Nwords=Nwords)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], str)
        self.assertEqual(len(result), Nwords)
        
    def test_print_topic(self):
        """
        :func:`.print_topic` should yield a string with ``Nwords`` words.
        """
        Nwords = 10
        
        pcgpath = cg_path + 'model.corpus.ldamodel.LDAModel.print_topic.png'
        with Profile(pcgpath):
            result = self.model.print_topic(0, Nwords=Nwords)
        
        self.assertIsInstance(result, str)
        self.assertEqual(len(result.split(', ')), Nwords)

    def test_list_topics(self):
        """
        :func:`.list_topics` should yield a dict { k : [ w ], }.
        """

        Nwords = 10

        pcgpath = cg_path + 'model.corpus.ldamodel.LDAModel.list_topics.png'
        with Profile(pcgpath):
            result = self.model.list_topics(Nwords=Nwords)

        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.keys()[0], int)
        self.assertIsInstance(result.values()[0], list)
        self.assertIsInstance(result.values()[0][0], str)
        self.assertEqual(len(result), self.model.Z)

    def test_print_topics(self):
        Nwords = 10

        pcgpath = cg_path + 'model.corpus.ldamodel.LDAModel.print_topics.png'
        with Profile(pcgpath):
            result = self.model.print_topics(Nwords=Nwords)

        self.assertIsInstance(result, str)
        self.assertEqual(len(result.split('\n')), self.model.Z)

    def test__item_description(self):
        result = self.model._item_description(0)
    
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], int)
        self.assertIsInstance(result[0][1], float)
        self.assertEqual(len(result), self.model.Z)

    def test__dimension_description(self):
        result = self.model._dimension_description(0)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], int)
        self.assertIsInstance(result[0][1], float)
        self.assertEqual(len(result), self.model.W)

    def test__dimension_items(self):
        """
        With threshold=0., should return a list with model.M entries.
        """
        result = self.model._dimension_items(0, threshold=0.)
    
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], str)
        self.assertIsInstance(result[0][1], float)
        self.assertEqual(len(result), self.model.M)
    
    def test__dimension_items_threshold(self):
        """
        With threshold=0.05, should return a shorter list.
        """
        
        threshold = 0.05
        result = self.model._dimension_items(0, threshold=threshold)
    
        self.assertEqual(len(result), 83)
        for r in result:
            self.assertGreaterEqual(r[1], threshold)

if __name__ == '__main__':
    unittest.main()