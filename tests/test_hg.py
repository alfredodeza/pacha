import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
from time import sleep
import shutil
import unittest
import getpass
from subprocess import Popen, PIPE
from pacha import host, hg


class TestHg(unittest.TestCase):

    username = getpass.getuser()

    def setUp(self):
        """Will setup just once for all tests"""
        os.mkdir('/tmp/test_pacha')
        config = open('/tmp/test_pacha/pacha.conf', 'w')
        config.write('user = %s\n' % self.username)
        config.write('host = localhost\n')
        config.write('path = /tmp/remote_pacha/hosts\n')
        config.close()

    def tearDown(self):
        """Will run last at the end of all tests"""
        try:

            shutil.rmtree('/tmp/test_pacha')
            shutil.rmtree('/tmp/remote_pacha')
        except OSError:
            pass # nevermind if you could not delte this guy

    def test_clone(self):
        """Clones the test repo to localhost"""
        os.mkdir('/tmp/remote_pacha')
        os.mkdir('/tmp/remote_pacha/hosts/')
        os.mkdir('/tmp/remote_pacha/hosts/%s' % host.hostname())
        mercurial = hg.Hg(port=22, host='localhost', user=self.username, 
		path='/tmp/test_pacha', 
            	test=True, conf='/tmp/test_pacha/pacha.conf')
	
        mercurial.initialize()
        mercurial.hg_add()
        mercurial.commit()
        mercurial.clone()
        result = os.path.isdir('/tmp/remote_pacha/hosts/%s/test_pacha' % host.hostname())
        self.assertTrue(result)

    def test_commit(self):
        """Builds a mercurial repo and commits"""
        mercurial = hg.Hg(port=22, host='localhost', user=self.username, 
		path='/tmp/test_pacha', test=True,
		conf='/tmp/test_pacha/pacha.conf')
    	mercurial.initialize()
        mercurial.hg_add()
        mercurial.commit()
        # we need to run hg st to verify we have actually commited stuff
        out = Popen('hg st /tmp/test_pacha', shell=True, stdout=PIPE)
        expected = ''
        actual = out.stdout.readline()
        self.assertEqual(expected, actual)

    def test_hg_add(self):
        """We create a file and then we add it"""
        mercurial = hg.Hg(port=22, host='localhost', user=self.username, 
		path='/tmp/test_pacha', test=True,
		conf='/tmp/test_pacha/pacha.conf')
        mercurial.initialize()
        mercurial.hg_add()
        out = Popen('hg st /tmp/test_pacha', shell=True, stdout=PIPE)
        expected = 'A pacha.conf\n'
        actual = out.stdout.readline()
        self.assertEqual(expected, actual)

    def test_hgrc(self):
        """Add a line for automated push inside .hg"""
        mercurial = hg.Hg(port=22, host='localhost', user=self.username, 
		path='/tmp/test_pacha', 
                test=True, conf='/tmp/test_pacha/pacha.conf')
        mercurial.hgrc()
        actual = open('/tmp/test_pacha/.hg/hgrc').readlines()[1]
        expected = 'default = ssh://%s@localhost//tmp/remote_pacha/hosts/%s/test_pacha' % (self.username, host.hostname())
        self.assertEqual(expected, actual)

    def test_hgrc_except(self):
        """Return False for issues if hgrc cannot be written"""
        mercurial = hg.Hg(port=22, host='localhost', user=self.username, 
		        path='/tmp/test_pacha', 
                test=True, 
                conf='/tmp/test_pacha/pacha.conf')
        mercurial.hgrc()
        self.assertFalse(mercurial.hgrc())

    def test_initialize(self):
        """Initializes a directory with Mercurial"""
        mercurial = hg.Hg(port=22, host='localhost', user=self.username, 
                path='/tmp/test_pacha', test=True,
		conf='/tmp/test_pacha/pacha.conf')
        mercurial.initialize()
        expected = os.path.isdir('/tmp/test_pacha/.hg')
        self.assertTrue(expected) 

    def test_push(self):
        """Push local changes to remote server"""
        os.mkdir('/tmp/remote_pacha')
        os.mkdir('/tmp/remote_pacha/hosts/')
        os.mkdir('/tmp/remote_pacha/hosts/%s' % host.hostname())
        mercurial = hg.Hg(port=22, host='localhost', user=self.username,
                path='/tmp/test_pacha', 
		        test=True, conf='/tmp/test_pacha/pacha.conf')
        mercurial.hgrc()
        mercurial.hg_add()
        mercurial.commit()
        mercurial.clone()
        new_file = open('/tmp/test_pacha/foo', 'w')
        new_file.write('new line')
        new_file.close()
        mercurial.hg_add()
        mercurial.commit()
        mercurial.push()
        hg.update(hosts_path = '/tmp/remote_pacha/hosts')
        new_line = open('/tmp/remote_pacha/hosts/%s/test_pacha/foo' % host.hostname())
        actual = new_line.readlines()[0]
        expected = 'new line'
        self.assertEqual(actual, expected)

    def test_validate_true(self):
        """Validate a working hg repository by returning True"""
        mercurial = hg.Hg(port=22, host='localhost', user=self.username,
                path='/tmp/test_pacha', test=True,
		conf='/tmp/test_pacha/pacha.conf')
        mercurial.initialize()
        expected = mercurial.validate()
        self.assertTrue(expected)

    def test_validate_false(self):
        """Return False to a non existent hg repository"""
        mercurial = hg.Hg(port=22, host='localhost', user=self.username,
                path='/tmp/test_pacha', test=True,
		conf='/tmp/test_pacha/pacha.conf')
        expected = mercurial.validate()
        self.assertFalse(expected)

    def test_update(self):
        """Update a working hg repository"""
        os.mkdir('/tmp/remote_pacha')
        os.mkdir('/tmp/remote_pacha/hosts')
        os.mkdir('/tmp/remote_pacha/hosts/%s' % host.hostname())
        mercurial = hg.Hg(port=22, host='localhost', user=self.username,
                path='/tmp/test_pacha', test=True,
		conf='/tmp/test_pacha/pacha.conf')
        mercurial.hgrc()
        mercurial.hg_add()
        mercurial.commit()
        mercurial.clone()
        new_line = open('/tmp/test_pacha/foo', 'w')
        new_line.write('new line')
        new_line.close()
        mercurial.hg_add()
        mercurial.commit()
        mercurial.push()
        hg.update(hosts_path='/tmp/remote_pacha/hosts')
        get_line = open('/tmp/remote_pacha/hosts/%s/test_pacha/foo' % host.hostname())
        actual = get_line.readlines()[0]
        expected = 'new line'
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
