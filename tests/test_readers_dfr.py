from settings import *

import unittest

from tethne.readers import dfr
from tethne.writers import corpora
from tethne import Paper, Corpus

class TestFromDir(unittest.TestCase):
    def setUp(self):
        self.dfrdatapath = '{0}/dfr'.format(datapath)

    def test_ngrams_from_dir(self):
        pcgpath = cg_path + 'readers.dfr.ngrams_from_dir.png'
        with Profile(pcgpath):
            self.unigrams = dfr.ngrams_from_dir(datapath, N='uni')

        self.assertEqual(len(self.unigrams), 241)
        self.assertIsInstance(self.unigrams, dict)
        self.assertIsInstance(self.unigrams.values()[0], list)
        self.assertIsInstance(self.unigrams.values()[0][0], tuple)

    def test_corpus_from_dir(self):
        pcgpath = cg_path + 'readers.dfr.corpus_from_dir.png'
        with Profile(pcgpath):
            C = dfr.corpus_from_dir(datapath)

        self.assertIsInstance(C, Corpus)
        self.assertEqual(len(C.papers), 241)

    def test_corpus_from_dir_ngrams(self):
        pcgpath = cg_path + 'readers.dfr.corpus_from_dir[ngrams].png'
        with Profile(pcgpath):
            C = dfr.corpus_from_dir(datapath, features=('uni',))
        
        self.assertEqual(len(C.papers), 241)
        self.assertEqual(len(C.features['unigrams']['features']), 241)

    def test_read_corpus(self):
        pcgpath = cg_path + 'readers.dfr.read_corpus.png'
        with Profile(pcgpath):
            C = dfr.read_corpus(self.dfrdatapath, features=('uni',))

        self.assertIsInstance(C, Corpus)
        self.assertEqual(len(C.papers), 241)
        self.assertEqual(len(C.features['unigrams']['features']), 241)

class TestNGrams(unittest.TestCase):
    def setUp(self):
        self.dfrdatapath = '{0}/dfr'.format(datapath)

    def test_ngrams_heavy(self):
        """
        In 'heavy' mode (default), :func:`.ngrams` should return a dict.
        """

        pcgpath = cg_path + 'readers.dfr.ngrams[heavy].png'
        with Profile(pcgpath):
            self.unigrams = dfr.ngrams(self.dfrdatapath, N='uni')

        self.assertEqual(len(self.unigrams), 241)
        self.assertIsInstance(self.unigrams, dict)
        self.assertIsInstance(self.unigrams.values()[0], list)
        self.assertIsInstance(self.unigrams.values()[0][0], tuple)
        
    def test_ngrams_light(self):
        """
        'light' mode should behave just like 'heavy'
        """
        
        pcgpath = cg_path + 'readers.dfr.ngrams[light].png'
        with Profile(pcgpath):
            self.unigrams = dfr.ngrams(self.dfrdatapath, N='uni', mode='light')

        self.assertEqual(len(self.unigrams), 241)
        self.assertIsInstance(self.unigrams, dfr.GramGenerator)
        self.assertIsInstance(self.unigrams.values()[0], list)
        self.assertIsInstance(self.unigrams.values()[0][0], tuple)   

    def test_write_corpus(self):
        """
        Result of :func:`.ngrams` should be ready to write as a corpus.
        """

        self.unigrams = dfr.ngrams(self.dfrdatapath, N='uni')
        ret = corpora.to_documents('/tmp/', self.unigrams)
        self.assertIsInstance(ret, tuple)
       
    def test_write_corpus_light(self):
        """
        Result of :func:`.ngrams` in 'light' mode should be ready to write as 
        a corpus.
        """

        self.unigrams = dfr.ngrams(self.dfrdatapath, N='uni', mode='light')
        ret = corpora.to_documents('/tmp/', self.unigrams)
        self.assertIsInstance(ret, tuple)

         
class TestGramGenerator(unittest.TestCase):
    def setUp(self):
        self.dfrdatapath = '{0}/dfr'.format(datapath)
        
    def test_len(self):
        """
        Should return the number of XML files in /wordcounts
        """
        
        pcgpath = cg_path + 'readers.dfr.GramGenerator.__init__.png'
        with Profile(pcgpath):
            g = dfr.GramGenerator(self.dfrdatapath+'/wordcounts', 'wordcount')
        
        self.assertEqual(len(g), 241)
        
    def test_generators(self):
        """
        Should yield something when iterated upon.
        """
        
        g = dfr.GramGenerator(self.dfrdatapath+'/wordcounts', 'wordcount')

        for i in g:
            self.assertNotEqual(i, None)
    
    def test_items(self):
        """
        :func:`GramGenerator.items` should return a new indexable
        :class:`.GramGenerator` that returns tuples.
        """
        
        g = dfr.GramGenerator(self.dfrdatapath+'/wordcounts', 'wordcount')
        self.assertIsInstance(g.items(), dfr.GramGenerator)
        self.assertIsInstance(g.items()[0], tuple)
        
    def test_iteritems(self):
        """
        :func:`GramGenerator.iteritems` should return a new indexable
        :class:`.GramGenerator` that returns tuples.
        """
        
        g = dfr.GramGenerator(self.dfrdatapath+'/wordcounts', 'wordcount')
        self.assertIsInstance(g.iteritems(), dfr.GramGenerator)
        self.assertIsInstance(g.items()[0], tuple)                

    def test_values(self):
        """
        :func:`GramGenerator.values` should return a new indexable
        :class:`.GramGenerator` that returns lists of tuples.
        """
        
        g = dfr.GramGenerator(self.dfrdatapath+'/wordcounts', 'wordcount')
        self.assertIsInstance(g.values(), dfr.GramGenerator)
        self.assertIsInstance(g.values()[0], list)                
        self.assertIsInstance(g.values()[0][0], tuple)  
        
    def test_keys(self):
        """
        :func:`GramGenerator.keys` should return a new indexable
        :class:`.GramGenerator` that returns strings.
        """
        
        g = dfr.GramGenerator(self.dfrdatapath+'/wordcounts', 'wordcount')
        self.assertIsInstance(g.keys(), dfr.GramGenerator)
        self.assertIsInstance(g.keys()[0], str)                
    
    def test_getitem(self):
        """
        :func:`GramGenerator.__getitem__` should return a key,value tuple.
        """
        
        g = dfr.GramGenerator(self.dfrdatapath+'/wordcounts', 'wordcount')
        self.assertIsInstance(g[0], tuple)
        self.assertIsInstance(g[0][0], str)     # Key.
        self.assertIsInstance(g[0][1], list)    # Value.
        self.assertIsInstance(g[0][1][0], tuple)        

class TestRead(unittest.TestCase):
    def setUp(self):
        self.dfrdatapath = '{0}/dfr'.format(datapath)

        pcgpath = cg_path + 'readers.dfr.read.png'
        with Profile(pcgpath):
            self.papers = dfr.read(self.dfrdatapath)

    def test_number(self):
        """
        Each article should be converted.
        """

        self.assertEqual(len(self.papers), 241)

    def test_type(self):
        """
        Should produce a list of :class:`.Paper`
        """

        self.assertIs(type(self.papers[0]), Paper)

    def test_handle_authors(self):
        """
        _handle_authors should generate lists of author surnames (aulast) and
        author first-initialis (auinit) of the same length.
        """

        aulast = self.papers[1]['aulast']
        expected = ['PIGOTT']
        self.assertListEqual(aulast, expected )

        auinit = self.papers[1]['auinit']
        expected = ['C']
        self.assertListEqual(auinit, expected )

        self.assertEqual(len(aulast), len(auinit))

    def test_handle_authors_raises(self):
        """
        If parameter is not a list or a string, should raise a ValueError.
        """

        with self.assertRaises(ValueError):
            dfr._handle_authors(1234)

    def test_handle_pubdate(self):
        """
        _handle_pubdate should yield a four-digit integer from a DfR pubdate
        string.
        """

        pubdate = self.papers[0]['date']
        self.assertIs(type(pubdate), int)   # Integer

        self.assertEqual(len(str(pubdate)), 4) # Four-digit

    def test_handle_pagerange(self):
        """
        _handle_pagerange should yield start and end pages, as strings.
        """

        start = self.papers[0]['spage']
        end = self.papers[0]['epage']

        self.assertIs(type(start), str) # Strings
        self.assertIs(type(end), str)

                                      
if __name__ == '__main__':
    unittest.main()                                      