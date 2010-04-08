import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
from time import sleep
import unittest
from lib import database

class TestWorker(unittest.TestCase):

    def tearDown(self):
        """Remove all the files that the database may have created"""
        try:
            os.remove('/tmp/pacha.db')
        except:
            pass # do not care if you could not remove that file

    def test_init(self):
        """Check if the db file was created"""
        database.Worker(db='/tmp/pacha.db')
        db = os.path.isfile('/tmp/pacha.db')
        self.assertTrue(db)

    def test_insert_path(self):
        """Do a simple insert of a path into db"""
        db = database.Worker(db='/tmp/pacha.db')
        db.insert(path='/tmp/foo', type="dir")
        # create the connection again:
        db = database.Worker(db='/tmp/pacha.db')
        for i in db.get_repo('/tmp/foo'):
            actual = i[1]
        expected = u'/tmp/foo'
        self.assertEqual(actual, expected)

    def test_insert_type(self):
        """Do a simple insert of a path and its type into db"""
        db = database.Worker(db='/tmp/pacha.db')
        db.insert(path='/tmp/foo', type="dir")
        # create the connection again:
        db = database.Worker(db='/tmp/pacha.db')
        for i in db.get_repo('/tmp/foo'):
            actual = i[3]
        expected = u'dir'
        self.assertEqual(actual, expected)

    def test_remove(self):
        """Remove a record from the db"""
        db = database.Worker(db='/tmp/pacha.db')
        db.insert('/tmp/foo')
        db = database.Worker(db='/tmp/pacha.db')
        db.insert('/tmp/fooo')
        db = database.Worker(db='/tmp/pacha.db')
        db.remove('/tmp/foo')
        db = database.Worker(db='/tmp/pacha.db')
        for i in db.get_repos():
            actual = i[1]
        expected = u'/tmp/fooo'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
