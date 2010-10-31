import getpass
import os
import unittest
import shutil

import pacha
from guachi             import ConfigMapper
from pacha              import daemon, host
from pacha.database     import Worker
from mock               import MockSys

DICT_CONF = dict(
        frequency       = 60,
        master          = 'False',
        host            = '%s' % host.hostname(),
        ssh_user        = '%s' % getpass.getuser(),
        ssh_port        = 22,
        hosts_path      = '/tmp/remote_pacha/hosts',
        hg_autocorrect  = 'True',
        log_enable      = 'False',
        log_path        = 'False',
        log_level       = 'DEBUG',
        log_format      = '%(asctime)s %(levelname)s %(name)s %(message)s',
        log_datefmt     = '%H=%M=%S'
        )




class SingleRepository(unittest.TestCase):

    username = getpass.getuser()
    dict_conf = dict(
            ssh_user = username,
            host = host.hostname(),
            hosts_path = '/tmp/remote_pacha/hosts'
            )

    def setUp(self):
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
        pacha.daemon.DB_FILE = '/tmp/pacha_test/pacha_test.db'

        os.makedirs('/tmp/remote_pacha/hosts/%s' % host.hostname())
        os.mkdir(test_dir)
        conf = open('/tmp/pacha_test/pacha.conf', 'w')
        conf.write('[DEFAULT]\n')
        conf.write('pacha.ssh.user = %s\n' % self.username)
        conf.write('pacha.host = %s\n' % host.hostname())
        conf.write('pacha.hosts.path = /tmp/remote_pacha/hosts\n')
        conf.close()
        conf = ConfigMapper('/tmp/pacha_test/pacha_test.db').stored_config()
        for k, v in DICT_CONF.items():
            conf[k] = v


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
        watch = daemon.SingleRepository(path)
        actual = watch.path 
        expected = "/tmp"
        self.assertEqual(actual, expected) 
        self.assertEqual(watch.dir_path, expected)

    def test_init_dir(self):
        """convert a path ending in file to a path ending in dir"""
        path = "/tmp/file.txt"
        watch = daemon.SingleRepository(path)
        actual = watch.dir_path 
        expected = "/tmp"
        self.assertEqual(actual, expected) 
        self.assertEqual(watch.path, '/tmp/file.txt')

    def test_is_modified_true(self):
        """Return true when a directory timestamp is newer than the tracked
        one"""
        db = Worker('/tmp/pacha_test/pacha_test.db')
        db.insert('/tmp',None, None, timestamp=1)
        watch = daemon.SingleRepository('/tmp')
        self.assertTrue(watch.is_modified())

    def test_is_modified_false(self):
        """Return false when the directory timestamp is older than the tracked
        one"""
        db = Worker('/tmp/pacha_test/pacha_test.db')
        db.insert('/tmp',None, None, timestamp=9997446874)
        watch = daemon.SingleRepository('/tmp')
        self.assertFalse(watch.is_modified())


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
