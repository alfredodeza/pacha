import os
import unittest
import sys

from pacha import daemon
from mock import MockSys

class TestWatcher(unittest.TestCase):

    def test_init(self):
        """Should get a normpath from a path"""
        path = "/tmp/"
        watch = daemon.Watcher(path)
        actual = watch.path 
        expected = "/tmp"
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

if __name__ == '__main__':
    unittest.main()
