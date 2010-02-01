import sys
sys.path.append('../')
import os
import shutil
import unittest
import host

class TestHost(unittest.TestCase):
    
    def setUp(self):
        """init the host class"""
        self.foo_host = host.Host(host='foo')
    
    def test_create(self):
        """Create a host folder"""
        host_dir = '/opt/pacha/hosts/foo'
        self.foo_host.create()
        self.assertTrue(host_dir)

    def tearDown(self):
        """Remove the created folder"""
        shutil.rmtree('/opt/pacha/hosts/foo')

class TestHostname(unittest.TestCase):
    def test_hostname(self):
        """Get the right hostname"""
        uname = os.uname()[1]
        self.assertEquals(uname, host.hostname())

if __name__ == '__main__':
    unittest.main()
