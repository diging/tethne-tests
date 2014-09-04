from settings import *

import unittest

import psycopg2

from tethne.persistence.psql.paper import SQLPapers, PAPER_TABLE
from tethne.readers import wos
from tethne import Paper, Corpus

dbparams = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'tethne_tests',
    'user': 'tethne',
    'password': 'tethneus',
}
dbargs = ' '.join(
        ['{0}={1}'.format(k,v) for k,v in dbparams.iteritems()]
        )

class TestSQLPapers(unittest.TestCase):
    def setUp(self):

        self.conn = psycopg2.connect(dbargs)
        self.cur = self.conn.cursor()

        try:
            self.cur.execute(PAPER_TABLE.format('tethne_test'))
            self.conn.commit()
            self.cur.execute(PAPER_TABLE.format('tethne_test_citations'))
            self.conn.commit()
        except:
            self.conn.commit()
            try:
                self.cur.execute("""DROP TABLE tethne_test;""")
            except:
                pass
            try:
                self.cur.execute("""DROP TABLE tethne_test_citations;""")
            except:
                pass
            self.conn.commit()

            self.cur.execute(PAPER_TABLE.format('tethne_test'))
            self.cur.execute(PAPER_TABLE.format('tethne_test_citations'))

            self.conn.commit()
        self.cur.close()
        self.sqlpapers = SQLPapers(self.conn, dbparams, table='tethne_test')


        self.papers = wos.read(datapath + '/wos.txt')

    def test_read(self):
        """
        When passed as a kwarg to the WoS reader, should be used as the
        container for parsed :class:`.Paper`\s.
        """

        spapers = wos.read(datapath + '/wos.txt', papers=self.sqlpapers)
        self.assertIsInstance(spapers, SQLPapers)
        self.assertEqual(len(spapers), 10)
        self.assertIsInstance(spapers[0], Paper)

    def test_iter(self):
        spapers = wos.read(datapath + '/wos.txt', papers=self.sqlpapers)
        i = 0
        for s in spapers:
            self.assertIsInstance(s, Paper)
            i += 1
        self.assertEqual(i, len(spapers))   # Should iterate over all Papers.

    def test_corpus(self):
        """
        Should be able to pass a SQLPaper to a :class:`.Corpus`\.
        """
        # Read the data into the SQL database.
        spapers = wos.read(datapath + '/wos.txt', papers=self.sqlpapers)
        del spapers

        # Now start fresh and spin up a Corpus.
        sqlpapers = SQLPapers(self.conn, dbparams, table='tethne_test')
        c = Corpus(sqlpapers)
        
    def test_append(self):
        """
        Should be able to iteratively append :class:`.Paper`\s to the list.
        
        Adding duplicate :class:`.Paper`\s raises a ValueError.
        """
        # Can append Papers.
        try:
            for i in xrange(9):
                self.sqlpapers.append(self.papers[i])
        except Exception as E:
            self.fail('append failed')

        # In-place addition works like append.
        try:
            self.sqlpapers += self.papers[9]
        except Exception as E:
            self.fail('iadd failed')

        # There are 10 entries now!
        self.assertEqual(len(self.sqlpapers), 10)

        # Can't add a duplicate Paper.
        self.assertRaises(ValueError, self.sqlpapers.append, self.papers[2])

    def test_getitem(self):
        # Add some Papers to get.
        for i in xrange(9):
            self.sqlpapers.append(self.papers[i])

        # Get the 0th item in the list.
        paper = self.sqlpapers[0]

        # The result should be a Paper.
        self.assertIsInstance(paper, Paper)

        # It should have the same values as the original Paper.
        for key in self.papers[0].keys():
            if key not in ['citations', 'institutions', 'country' ]:
                self.assertEqual(paper[key], self.papers[0][key])

            # ...including citations.
            elif key == 'citations':
                for i in xrange(len(paper[key])):
                    c_sql = paper[key][i]
                    c_org = self.papers[0][key][i]
                    for k in c_sql.keys():
                        self.assertEqual(c_sql[k], c_org[k])

    def tearDown(self):
        """
        Destroy testing table.
        """
        self.conn.commit()
        self.cur = self.conn.cursor()

        self.cur.execute("""DROP TABLE tethne_test;""")
        self.cur.execute("""DROP TABLE tethne_test_citations;""")
        self.conn.commit()
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    unittest.main()


