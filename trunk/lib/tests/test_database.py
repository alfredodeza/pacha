import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
import unittest
import database

class TestAppend(unittest.TestCase):

    def test_create_database(self):
        """Check if the db file was created"""
        db = database.Worker('/tmp/testdatabase.db')
        expected = os.path.isfile('/tmp/testdatabase.db')
        self.assertTrue(expected)

    def tearDown(self):
        """Delete the database file that was created for the test"""
        os.remove('/tmp/testdatabase.db')

if __name__ == '__main__':
    unittest.main()
