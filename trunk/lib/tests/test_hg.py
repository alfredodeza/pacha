import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
from time import sleep
import shutil
import unittest
import getpass
from subprocess import Popen, PIPE
from hg import Hg, update
import host


class TestHg(unittest.TestCase):

    username = getpass.getuser()

    def test_clone(self):
        """Clones the test repo to localhost"""
        config = open('/tmp/test_pacha/pacha.conf', 'w')
        config.write('user = %s\n' % self.username)
        config.write('host = localhost\n')
        config.write('path = /tmp/remote_pacha\n')
        config.close()
        os.mkdir('/tmp/remote_pacha')
#        os.mkdir('/tmp/remote_pacha/%s' % self.username)
        os.mkdir('/tmp/remote_pacha/localhost')

        hg = Hg(port=22, host='localhost', user=self.username, path='/tmp/test_pacha', 
            test=True, conf='/tmp/test_pacha/pacha.conf')
        hg.initialize()
        hg.hg_add()
        hg.commit()
        hg.clone()
        result = os.path.isdir('/tmp/remote_pacha')
        self.assertTrue(result)

    def setUp(self):
        """Will setup just once for all tests"""
        os.mkdir('/tmp/test_pacha')
        new_file = open('/tmp/test_pacha/foo', 'w')
        new_file.close()

    def tearDown(self):
        """Will run last at the end of all tests"""
        shutil.rmtree('/tmp/test_pacha')
        try:
            shutil.rmtree('/tmp/remote_pacha')
        except OSError:
            pass # nevermind if you could not delte this guy

    def test_commit(self):
        """Builds a mercurial repo and commits"""
        hg = Hg(port=22, host='localhost', user=self.username, path='/tmp/test_pacha', test=True)
        hg.initialize()
        hg.hg_add()
        hg.commit()
        # we need to run hg st to verify we have actually commited stuff
        out = Popen('hg st /tmp/test_pacha', shell=True, stdout=PIPE)
        expected = ''
        actual = out.stdout.readline()
        self.assertEqual(expected, actual)

    def test_hg_add(self):
        """We create a file and then we add it"""
        hg = Hg(port=22, host='localhost', user=self.username, path='/tmp/test_pacha', test=True)
        hg.initialize()
        hg.hg_add()
        out = Popen('hg st /tmp/test_pacha', shell=True, stdout=PIPE)
        expected = 'A foo\n'
        actual = out.stdout.readline()
        self.assertEqual(expected, actual)

    def test_hgrc(self):
        """Add a line for automated push inside .hg"""
        config = open('/tmp/test_pacha/pacha.conf', 'w')
        config.write('user = %s\n' % self.username)
        config.write('host = localhost\n')
        config.write('path = /opt/pacha/hosts\n')
        config.close()
        hg = Hg(port=22, host='localhost', user=self.username, path='/tmp/test_pacha', 
                test=True, conf='/tmp/test_pacha/pacha.conf')
        hg.hgrc()
        actual = open('/tmp/test_pacha/.hg/hgrc').readlines()[1]
        expected = 'default = ssh://%s@localhost//opt/pacha/hosts/%s/test_pacha' % (
                self.username, host.hostname())
        self.assertEqual(expected, actual)

    def test_initialize(self):
        """Initializes a directory with Mercurial"""
        hg = Hg(port=22, host='localhost', user=self.username, 
                path='/tmp/test_pacha', test=True)
        hg.initialize()
        expected = os.path.isdir('/tmp/test_pacha/.hg')
        self.assertTrue(expected) 

#    def test_push(self):
#        """Push local changes to remote server"""
#        hg = Hg(port=22, host='localhost', user=self.username,
#                path='/tmp/pacha', test=True)
#        hg.initialize()
#        hg.hg_add()
#        hg.commit()
#        hg.push()
#        expected = os.path.isdir('/tmp/remote_pacha')
#        self.assertTrue(True)


    def test_validate_true(self):
        """Validate a working hg repository by returning True"""
        hg = Hg(port=22, host='localhost', user=self.username,
                path='/tmp/test_pacha', test=True)
        hg.initialize()
        expected = hg.validate()
        self.assertTrue(expected)

    def test_validate_false(self):
        """Return False to a non existent hg repository"""
        hg = Hg(port=22, host='localhost', user=self.username,
                path='/tmp/test_pacha', test=True)
        expected = hg.validate()
        self.assertFalse(expected)

    def test_update(self):
        """Update a working hg repository"""
        os.mkdir('/tmp/test_pacha/hosts')
        os.mkdir('/tmp/test_pacha/hosts/foo')
        os.mkdir('/tmp/test_pacha/hosts/foo/one')
        hg = Hg(port=22, host='localhost', user=self.username,
                path='/tmp/test_pacha/hosts/foo/one', test=True)
        empty = open('/tmp/test_pacha/hosts/foo/one/empty', 'w')
        hg.initialize()
        hg.hg_add()
        hg.commit()
        #out = "0 files updated, 0 files merged, 0 files removed, 0 files unresolved"
        expected = update(hosts_path='/tmp/test_pacha/hosts')
        self.assertFalse(expected)

if __name__ == '__main__':
    unittest.main()
