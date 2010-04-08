import sys
if '../' not in sys.path:
    sys.path.append('../')
import unittest
import os

class TestDependencies(unittest.TestCase):

    def test_ssh_bin(self):
        """Is ssh in /usr/bin"""
        ssh = os.path.exists('/usr/bin/ssh')
        self.assertTrue(ssh)

    def test_hg_bin(self):
        """Is Mercurial in /usr/bin"""
        hg = os.path.exists('/usr/bin/hg')
        self.assertTrue(hg)

if __name__ == '__main__':
    unittest.main()
