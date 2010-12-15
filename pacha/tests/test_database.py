from time           import time

import os
import shutil
import unittest

from guachi         import ConfigMapper
from pacha          import database

class TestWorker(unittest.TestCase):

    def setUp(self):
        """Remove all the files that the database may have created"""
        if os.path.exists('/tmp/pacha_test'):
            shutil.rmtree('/tmp/pacha_test')
        os.makedirs('/tmp/pacha_test')
        f = open('/tmp/pacha_test/foo', 'w')
        f.write('foo')
        f.close
        try:
            os.remove('/tmp/pacha.db')
        except:
            pass # do not care if you could not remove that file

    def tearDown(self):
        """Remove all the files that the database may have created"""
        try:
            shutil.rmtree('/tmp/pacha_test')
        except:
            pass # do not care if you could not remove that file
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
        db.insert(path='/tmp/pacha_test', type="dir")
        # create the connection again:
        db = database.Worker(db='/tmp/pacha.db')
        for i in db.get_repo('/tmp/pacha_test'):
            actual = i[1]
        expected = u'/tmp/pacha_test'
        self.assertEqual(actual, expected)

    def test_timestamp(self):
        """Add a repo and check the timestamp"""
        db = database.Worker(db='/tmp/pacha.db')
        tstamp = int(time())
        db.insert(path='/tmp/pacha_test', type="dir", timestamp=tstamp)
        # create the connection again:
        db = database.Worker(db='/tmp/pacha.db')
        actual = [i[4] for i in db.get_repo('/tmp/pacha_test')][0]
        expected = u'%s' % tstamp
        self.assertEqual(actual, expected)


    def test_insert_type(self):
        """Do a simple insert of a path and its type into db"""
        db = database.Worker(db='/tmp/pacha.db')
        db.insert(path='/tmp/pacha_test', type="dir")
        # create the connection again:
        db = database.Worker(db='/tmp/pacha.db')
        for i in db.get_repo('/tmp/pacha_test'):
            actual = i[3]
        expected = u'dir'
        self.assertEqual(actual, expected)

    def test_update_timestamp(self):
        """Updates the DB timestamp information"""
        db = database.Worker(db='/tmp/pacha.db')
        db.insert(path='/tmp/pacha_test', type='dir',
                timestamp='0')
        db.closedb()
        db = database.Worker(db='/tmp/pacha.db')
        db.update_timestamp(path='/tmp/pacha_test', timestamp='1')
        for i in db.get_repo('/tmp/pacha_test'):
            actual = i[4]
        expected = '1'
        self.assertEqual(actual, expected)

    def test_remove(self):
        """Remove a record from the db"""
        db = database.Worker(db='/tmp/pacha.db')
        db.insert('/tmp/pacha_test')
        db = database.Worker(db='/tmp/pacha.db')
        db.remove('/tmp/pacha_test')
        db = database.Worker(db='/tmp/pacha.db')
        actual = [i for i in db.get_repos()]
        expected = []
        self.assertEqual(actual, expected)

    def test_add_config(self):
        """Add a configuration file path"""
        db = ConfigMapper('/tmp/pacha.db').stored_config()
        db['path'] = '/foo'
        expected = '/foo'
        actual = db['path']
        self.assertEqual(actual, expected) 

    def test_add_config_unique(self):
        """You can't add duplicates to the config table"""
        db = ConfigMapper('/tmp/pacha.db').stored_config()
        db['path'] = '/foo'
        db['path'] = '/foo'
        db['path'] = '/foo'
        actual = db['path']
        expected = u'/foo'
        self.assertEqual(actual, expected)
 

    def test_remove_config(self):
        """Add and then remove a configuration file path"""
        db = ConfigMapper('/tmp/pacha.db').stored_config()
        db['path'] = '/foo'        
        db['path'] = ''
        actual = db['path']
        expected = ''
        self.assertEqual(actual, expected) 
        
 
    def test_insert_meta(self):
        db = database.Worker(db='/tmp/pacha.db')
        db.insert_meta('/foo', 'alfredo', 'admin', 'rwx', 'dir')
        actual = [i for i in db.get_meta('/foo')]
        expected = [(1, u'/foo', u'alfredo', u'admin', u'rwx', u'dir')]
        self.assertEqual(actual, expected) 


if __name__ == '__main__':
    unittest.main()
