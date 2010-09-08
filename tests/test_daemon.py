import os
import unittest
import sys

from pacha import daemon
from mock import MockSys
#class MockSys(object):
#    """Can grab messages sent to stdout or stderr"""
#    def __init__(self):
#        self.message = ""
#
#    def write(self, string):
#        self.message = string 
#        pass
#

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

class TestFrecuency(unittest.TestCase):

    def test_freq_string(self):
        "Return an integer if we send a string"
        actual = daemon.frecuency("10")
        expected = 10
        self.assertEqual(actual, expected) 

    def test_freq_valueerror(self):
        "Get 60 secs back if we have something other than an int"
        actual =  daemon.frecuency("")
        expected = 60
        self.assertEqual(actual, expected) 

    def test_freq_under_ten(self):
        "If we have less than 10 secs return 60 secs"
        actual = daemon.frecuency("4")
        expected = 60
        self.assertEqual(actual, expected) 

    def test_freq_exception(self):
        "No matter what we send we get 60 secs back"
        actual = daemon.frecuency({})
        expected = 60 
        self.assertEqual(actual, expected) 

class RunCommand(unittest.TestCase):

    def test_run_command_stdout(self):
        sys.stderr = MockSys()
        actual = daemon.run_command(std="stdout", cmd="""echo "foo" """)
        expected = ['foo\n']
        self.assertEqual(actual, expected) 

    def test_run_command_stderr(self):
        sys.stderr = MockSys()
        actual = daemon.run_command(std="stderr", cmd=""" echo "error message" 1>&2 """)
        expected = ['error message\n']
        self.assertEqual(actual, expected) 

if __name__ == '__main__':
    unittest.main()
