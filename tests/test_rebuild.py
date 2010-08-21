import unittest
import sys
import os
import shutil
import getpass

from pacha import rebuild, host 

class MockSys(object):
    """Can grab messages sent to stdout or stderr"""
    def __init__(self):
        self.message = []

    def write(self, string):
        self.message.append(string)
        pass


class TestRebuild(unittest.TestCase):
    username = getpass.getuser()

    def setUp(self):
        """Will setup just once for all tests"""
        if os.path.isdir('/tmp/remote_pacha'):
            shutil.rmtree('/tmp/remote_pacha')
        if os.path.isdir('/tmp/test_pacha'):
            shutil.rmtree('/tmp/test_pacha')
        os.mkdir('/tmp/test_pacha')
        config = open('/tmp/test_pacha/pacha.conf', 'w')
        config.write('[DEFAULT]\n')
        config.write('pacha.ssh.user = %s\n' % self.username)
        config.write('pacha.host = %s\n' % host.hostname())
        config.write('pacha.hosts.path = /tmp/remote_pacha/hosts\n')
        config.close()


    def tearDown(self):
        """Will run last at the end of all tests"""
        try:
            shutil.rmtree('/tmp/test_pacha')
            shutil.rmtree('/tmp/remote_pacha')
            shutil.rmtree('/tmp/localhost')
            shutil.rmtree('/tmp/single_dir')
        except OSError:
            pass # nevermind if you could not delte this guy


    def test_retrieve_files_single(self):
        """Gets a single directory from a remote host"""
        os.makedirs('/tmp/remote_pacha/localhost/another_dir')
        os.makedirs('/tmp/remote_pacha/localhost/single_dir')
        remote_file = open('/tmp/remote_pacha/localhost/single_dir/remote.txt', 'w')
        remote_file.write("remote file")
        remote_file.close()
        self.assertTrue(os.path.isfile('/tmp/remote_pacha/localhost/single_dir/remote.txt'))
        server = "%s@%s" % (self.username, host.hostname()) 
        run = rebuild.Rebuild(server=server,
                        hostname='localhost', 
                        source='/tmp/remote_pacha',
                        directory='single_dir')
        run.retrieve_files()
        result = os.path.isfile('/tmp/localhost/single_dir/remote.txt')
        line = open('/tmp/localhost/single_dir/remote.txt')
        remote_line = line.readline()
        self.assertEqual(remote_line, "remote file")
        self.assertTrue(result)

    def test_retrieve_files_all(self):
        """Gets all files from a remote host"""
        os.makedirs('/tmp/remote_pacha/localhost/etc')
        os.mkdir('/tmp/remote_pacha/localhost/home')
        remote_file = open('/tmp/remote_pacha/localhost/etc/etc.conf', 'w')
        remote_file.write("remote second file")
        remote_file.close()
        remote_file = open('/tmp/remote_pacha/localhost/home/home.conf', 'w')
        remote_file.write("remote file")
        remote_file.close()
        server = "%s@%s" % (self.username, host.hostname()) 
        run = rebuild.Rebuild(server=server,
                        hostname='localhost', 
                        source='/tmp/remote_pacha')
        run.retrieve_files()
        result_1 = os.path.isfile('/tmp/localhost/etc/etc.conf')
        result_2 = os.path.isfile('/tmp/localhost/home/home.conf')
        line = open('/tmp/localhost/etc/etc.conf')
        remote_line = line.readline()
        self.assertEqual(remote_line, "remote second file")
        self.assertTrue(result_2)
        self.assertTrue(result_1)

    def test_show_directories(self):
        """Get a list of files in the remote server"""
        os.makedirs('/tmp/remote_pacha/localhost/etc')
        os.mkdir('/tmp/remote_pacha/localhost/home')
        remote_file = open('/tmp/remote_pacha/localhost/etc/etc.conf', 'w')
        remote_file.write("remote second file")
        remote_file.close()
        remote_file = open('/tmp/remote_pacha/localhost/home/home.conf', 'w')
        remote_file.write("remote file")
        remote_file.close()
        server = "%s@%s" % (self.username, host.hostname()) 
        sys.stdout = MockSys()
        run = rebuild.Rebuild(server=server,
                        source='/tmp/remote_pacha')
        run.show_directories()
        actual = sys.stdout.message
        expected = ['/tmp/remote_pacha', '\n', '/tmp/remote_pacha/localhost', 
                '\n', '/tmp/remote_pacha/localhost/etc', '\n', 
                '/tmp/remote_pacha/localhost/etc/etc.conf', '\n', 
                '/tmp/remote_pacha/localhost/home', '\n', 
                '/tmp/remote_pacha/localhost/home/home.conf', '\n']
        self.assertEqual(actual, expected) 

if __name__ == '__main__':
    unittest.main()
