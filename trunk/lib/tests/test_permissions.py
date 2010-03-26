import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
import stat
import pwd
import grp
import unittest
import permissions

class TestPermissions(unittest.TestCase):

    def test_owner(self):
        """Check correct ownership of a directory"""
        info = os.stat('/tmp').st_uid
        expected = pwd.getpwuid(info)[0]
        owner = permissions.Permissions('/tmp')
        actual = owner.owner()
        self.assertEqual(actual, expected)

    def test_group(self):
        """Check the group ownership of a directory"""
        info = os.stat('/tmp').st_uid
        expected = grp.getgrgid(info)[0]
        group = permissions.Permissions('/tmp')
        actual = group.group()
        self.assertEqual(actual, expected)

    def test_rwx(self):
        """Return an octal representation of file permissions"""
        info = os.stat('/tmp')[stat.ST_MODE]
        expected = oct(info & 0777)
        mode = permissions.Permissions('/tmp')
        actual = mode.rwx()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
