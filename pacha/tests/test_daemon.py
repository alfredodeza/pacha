import os
import unittest
import sys
import shutil

import pacha
from pacha      import daemon, host
from mock       import MockSys

class TestWatcher(unittest.TestCase):

    def setUp(self):
        # make sure we do not have db file 
        test_dir = '/tmp/pacha_test'
        remote_dir = '/tmp/remote_pacha'
        pacha_host = '/tmp/pacha_test_host'
        if os.path.isdir(test_dir):
            shutil.rmtree(test_dir)
        if os.path.isdir(remote_dir):
            shutil.rmtree(remote_dir)
        if os.path.isdir(pacha_host):
            shutil.rmtree(pacha_host)
        pacha.DB_DIR = '/tmp/pacha_test'
        pacha.DB_FILE ='/tmp/pacha_test/pacha_test.db' 
        pacha.permissions.DB_FILE ='/tmp/pacha_test/pacha_test.db' 
        pacha.hg.DB_FILE ='/tmp/pacha_test/pacha_test.db' 
        pacha.database.DB_FILE = '/tmp/pacha_test/pacha_test.db'
        pacha.database.DB_DIR = '/tmp/pacha_test'
        pacha.daemon.PID_DIR = '/tmp/pacha_test'

        os.makedirs('/tmp/remote_pacha/hosts/%s' % host.hostname())
        os.mkdir(test_dir)
        conf = open('/tmp/pacha_test/pacha.conf', 'w')
        conf.write('[DEFAULT]\n')
        conf.write('pacha.ssh.user = %s\n' % self.username)
        conf.write('pacha.host = %s\n' % host.hostname())
        conf.write('pacha.hosts.path = /tmp/remote_pacha/hosts\n')
        conf.close()

    def tearDown(self):
        # make sure we do not have db file 
        test_dir = '/tmp/pacha_test'
        remote_dir = '/tmp/remote_pacha'
        pacha_host = '/tmp/pacha_test_host'
        if os.path.isdir(test_dir):
            shutil.rmtree(test_dir)
        if os.path.isdir(remote_dir):
            shutil.rmtree(remote_dir)
        if os.path.isdir(pacha_host):
            shutil.rmtree(pacha_host)

    def test_init(self):
        """Should get a normpath from a path"""
        path = "/tmp/"
        watch = daemon.Watcher(path)
        actual = watch.path 
        expected = "/tmp"
        self.assertEqual(actual, expected) 
        self.assertEqual(watch.dir_path, expected)

    def test_init_dir(self):
        """convert a path ending in file to a path ending in dir"""
        path = "/tmp/file.txt"
        watch = daemon.Watcher(path)
        actual = watch.dir_path 
        expected = "/tmp"
        self.assertEqual(actual, expected) 
        self.assertEqual(watch.path, '/tmp/file.txt')

    def test_report_unmodified(self):
        """if a file hasn't changed do not do anything"""

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
