import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
import pwd
import grp
import unittest
import permissions

class TestPermissions(unittest.TestCase):

    def test_owner(self):
        """Check correct ownership of a directory"""
        info = os.stat('/tmp').st_uid
        actual = pwd.getpwuid(info)[0]
        expected = 'root'
        self.assertEqual(actual, expected)

    def test_group(self):
        """Check the group ownership of a directory"""
        info = os.stat('/tmp').st_uid
        actual = grp.getgrgid(info)[0]
        expected = 'root'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
