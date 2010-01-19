import sys
sys.path.append('../')
import os
import shutil
import unittest
import getpass
from hg import Hg

def setup():
    """Will setup just once for all tests"""
    os.mkdir('/tmp/pacha')
    open('/tmp/pacha/foo', 'w')

def teardown():
    """Will run last at the end of all tests"""
    shutil.rmtree('/tmp/pacha')

class TestHg(unittest.TestCase):

    def test_clone(self):
        """Clones the test repo to localhost"""
        username = getpass.getuser()
        hg = Hg(port=22, host='localhost', user=username, path='/tmp/pacha', test=True)
        hg.initialize()
        hg.hg_add()
        hg.commit()
        # self.assertEqual(expected, hg.clone())
        assert True # TODO: implement your test here

    def test_commit(self):
        """test commit 2"""
        # hg = Hg(port, host, user, path)
        # self.assertEqual(expected, hg.commit())
        assert True # TODO: implement your test here

    def test_hg_add(self):
        """test hg_add 3"""
        # hg = Hg(port, host, user, path)
        # self.assertEqual(expected, hg.hg_add())
        assert True # TODO: implement your test here

    def test_hgrc(self):
        """test hgrc 4"""
        # hg = Hg(port, host, user, path)
        # self.assertEqual(expected, hg.hgrc())
        assert True # TODO: implement your test here

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
