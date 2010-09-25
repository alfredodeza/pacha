import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
import unittest
from pacha import database

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

    def test_update_rev(self):
        """Updates the DB revision information"""
        db = database.Worker(db='/tmp/pacha.db')
        db.insert(path='/tmp/foo', type='dir',
                revision='1')
        db.closedb()
        db = database.Worker(db='/tmp/pacha.db')
        db.update_rev(path='/tmp/foo', revision='2')
        for i in db.get_repo('/tmp/foo'):
            actual = i[4]
        expected = '2'
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

    def test_add_config(self):
        """Add a configuration file path"""
        db= database.Worker(db='/tmp/pacha.db')
        db.add_config('/foo')
        config = [i for i in db.get_config_path()][0][0]
        self.assertEqual(config, u'/foo')

    def test_add_config_unique(self):
        """You can't add duplicates to the config table"""
        db = database.Worker(db='/tmp/pacha.db')
        db.add_config('/foo')
        db.add_config('/foo')
        db.add_config('/foo')
        actual = [i for i in db.get_config_path()]
        expected = [(u'/foo',)]
        self.assertEqual(actual, expected)
 

    def test_remove_config(self):
        """Add and then remove a configuration file path"""
        db = database.Worker(db='/tmp/pacha.db')
        db.add_config('/foo')
        db.remove_config()
        config = [i for i in db.get_config_path()]
        self.assertEqual(config, [])
        
    def test_get_config_path(self):
        """Add a config path and then query it"""
        db = database.Worker(db='/tmp/pacha.db')
        db.add_config('/foo')
        actual = [i for i in db.get_config_path()][0][0]
        expected = u'/foo'
        self.assertEqual(actual, expected) 
 
    def test_insert_meta(self):
        db = database.Worker(db='/tmp/pacha.db')
        db.insert_meta('/foo', 'alfredo', 'admin', 'rwx', 'dir')
        actual = [i for i in db.get_meta('/foo')]
        expected = [(1, u'/foo', u'alfredo', u'admin', u'rwx', u'dir')]
        self.assertEqual(actual, expected) 


if __name__ == '__main__':
    unittest.main()
