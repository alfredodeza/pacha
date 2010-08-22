import os
import unittest
import sys

from pacha import daemon

class MockSys(object):
    """Can grab messages sent to stdout or stderr"""
    def __init__(self):
        self.message = ""

    def write(self, string):
        self.message = string 
        pass


class TestWatcher(unittest.TestCase):

    def test_init(self):
        """Should get a normpath from a path"""
        path = "/path/to/a/single/file.txt/"
        watch = daemon.Watcher(path)
        actual = watch.path 
        expected = "/path/to/a/single/file.txt"
        self.assertEqual(actual, expected) 

class TestRunners(unittest.TestCase):

    def test_init_chdir(self):
        """Should change dir"""
        init = daemon.Runners('/')
        actual = os.getcwd()
        expected = '/'
        self.assertEqual(actual, expected) 

if __name__ == '__main__':
    unittest.main()
