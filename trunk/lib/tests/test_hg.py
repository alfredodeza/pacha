import sys
sys.path.append('../')
import os
from time import sleep
import shutil
import unittest
import getpass
from subprocess import Popen, PIPE
from hg import Hg
import host


class TestHg(unittest.TestCase):

    def test_clone(self):
        """Clones the test repo to localhost"""
        username = getpass.getuser()
        hg = Hg(port=22, host='localhost', user=username, path='/tmp/pacha', test=True)
        hg.initialize()
        hg.hg_add()
        hg.commit()
        hg.clone()
        result = os.path.isdir('/tmp/remote_pacha')
        self.assertTrue(result)

    def setUp(self):
        """Will setup just once for all tests"""
        os.mkdir('/tmp/pacha')
        open('/tmp/pacha/foo', 'w')

    def tearDown(self):
        """Will run last at the end of all tests"""
        shutil.rmtree('/tmp/pacha')
        try:
            shutil.rmtree('/tmp/remote_pacha')
        except OSError:
            pass # nevermind if you could not delte this guy

    def test_commit(self):
        """Builds a mercurial repo and commits"""
        username = getpass.getuser()
        hg = Hg(port=22, host='localhost', user=username, path='/tmp/pacha', test=True)
        hg.initialize()
        hg.hg_add()
        hg.commit()
        # we need to run hg st to verify we have actually commited stuff
        out = Popen('hg st /tmp/pacha', shell=True, stdout=PIPE)
        expected = ''
        actual = out.stdout.readline()
        self.assertEqual(expected, actual)

    def test_hg_add(self):
        """We create a file and then we add it"""
        username = getpass.getuser()
        hg = Hg(port=22, host='localhost', user=username, path='/tmp/pacha', test=True)
        hg.initialize()
        hg.hg_add()
        out = Popen('hg st /tmp/pacha', shell=True, stdout=PIPE)
        expected = 'A foo\n'
        actual = out.stdout.readline()
        self.assertEqual(expected, actual)

    def test_hgrc(self):
        """Add a line for automated push inside .hg"""
        username = getpass.getuser()
        config = open('/tmp/pacha/pacha.conf', 'w')
        config.write('user = %s\n' % username)
        config.write('host = localhost\n')
        config.write('path = /opt/pacha/hosts\n')
        config.close()
        hg = Hg(port=22, host='localhost', user=username, path='/tmp/pacha', 
                test=True, conf='/tmp/pacha/pacha.conf')
        hg.hgrc()
        actual = open('/tmp/pacha/.hg/hgrc').readlines()[1]
        expected = 'default = ssh://%s@localhost//opt/pacha/hosts/%s/pacha' % (
                username, host.hostname())
        self.assertEqual(expected, actual)

    def test_initialize(self):
        """test initialize 5"""
        # hg = Hg(port, host, user, path)
        # self.assertEqual(expected, hg.initialize())
        assert True # TODO: implement your test here

    def test_push(self):
        """test push 6"""
        # hg = Hg(port, host, user, path)
        # self.assertEqual(expected, hg.push())
        assert True # TODO: implement your test here

    def test_validate(self):
        """test validate 7"""
        # hg = Hg(port, host, user, path)
        # self.assertEqual(expected, hg.validate())
        assert True # TODO: implement your test here


if __name__ == '__main__':
    unittest.main()
