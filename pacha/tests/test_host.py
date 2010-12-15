import os
import shutil
import unittest
from pacha import host

class TestHost(unittest.TestCase):
    
    def setUp(self):
        """init the host class"""
        self.foo_host = host.Host(host='foo', host_path='/tmp/test_pacha/hosts')
    
    def test_create(self):
        """Create a host folder"""
        os.mkdir('/tmp/test_pacha')
        os.mkdir('/tmp/test_pacha/hosts')
        host_dir = '/tmp/test_pacha/hosts/foo'
        self.foo_host.create()
        self.assertTrue(host_dir)

    def test_create_error(self):
        """Don't create a host folder if present"""
        os.mkdir('/tmp/test_pacha')
        os.mkdir('/tmp/test_pacha/hosts')
        host_dir = '/tmp/test_pacha/hosts/foo'
        self.foo_host.create()
        self.assertFalse(self.foo_host.create())


    def tearDown(self):
        """Remove the created folder"""
        shutil.rmtree('/tmp/test_pacha')

class TestHostname(unittest.TestCase):
    def test_hostname(self):
        """Get the right hostname"""
        uname = os.uname()[1]
        self.assertEquals(uname, host.hostname())

if __name__ == '__main__':
    unittest.main()
