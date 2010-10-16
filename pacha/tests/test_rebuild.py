import unittest
import os
import shutil
import getpass
import sys

import pacha

from time           import strftime

from guachi         import ConfigMapper
from mock           import MockSys
from pacha          import rebuild, host 
from pacha.hg       import hg_push_update


class TestRebuild(unittest.TestCase):
    username = getpass.getuser()

    def setUp(self):
        """Will setup just once for all tests"""
        if os.path.isdir('/tmp/remote_pacha'):
            shutil.rmtree('/tmp/remote_pacha')
        if os.path.isdir('/tmp/localhost'):
            shutil.rmtree('/tmp/localhost')
        if os.path.isdir('/tmp/test_pacha'):
            shutil.rmtree('/tmp/test_pacha')
        if os.path.isdir('/tmp/%s' % host.hostname()):
            shutil.rmtree('/tmp/%s' % host.hostname())
        if os.path.isdir('/tmp/pacha_test'):
            shutil.rmtree('/tmp/pacha_test')
        os.mkdir('/tmp/test_pacha')
        config = open('/tmp/test_pacha/pacha.conf', 'w')
        config.write('[DEFAULT]\n')
        config.write('pacha.ssh.user = %s\n' % self.username)
        config.write('pacha.host = %s\n' % host.hostname())
        config.write('pacha.hosts.path = /tmp/remote_pacha/hosts\n')
        config.close()
        # static mappings for file locations 
        pacha.DB_DIR = '/tmp/pacha_test'
        pacha.DB_FILE ='/tmp/pacha_test/pacha_test.db' 
        pacha.permissions.DB_FILE ='/tmp/pacha_test/pacha_test.db' 
        pacha.hg.DB_FILE ='/tmp/pacha_test/pacha_test.db' 
        pacha.database.DB_FILE = '/tmp/pacha_test/pacha_test.db'
        pacha.database.DB_DIR = '/tmp/pacha_test'
        pacha.daemon.PID_DIR = '/tmp/pacha_test'

        # write a config file 
        os.makedirs('/tmp/pacha_test')
        conf = open('/tmp/pacha_test/pacha.conf', 'w')
        conf.write('[DEFAULT]\n')
        conf.write('pacha.ssh.user = %s\n' % self.username)
        conf.write('pacha.host = %s\n' % host.hostname())
        conf.write('pacha.hosts.path = /tmp/remote_pacha/hosts\n')
        conf.close()
        



    def tearDown(self):
        """Will run last at the end of all tests"""
        if os.path.isdir('/tmp/remote_pacha'):
            shutil.rmtree('/tmp/remote_pacha')
        if os.path.isdir('/tmp/localhost'):
            shutil.rmtree('/tmp/localhost')
        if os.path.isdir('/tmp/test_pacha'):
            shutil.rmtree('/tmp/test_pacha')
        if os.path.isdir('/tmp/pacha_test'):
            shutil.rmtree('/tmp/pacha_test')

        try:
            shutil.rmtree('/tmp/test_pacha')
            shutil.rmtree('/tmp/remote_pacha')
            shutil.rmtree('/tmp/localhost')
            shutil.rmtree('/tmp/single_dir')
        except OSError:
            pass # nevermind if you could not delete this guy


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


    def test_retrieve_files_error_message(self):
        """If you can't retrieve files let me know"""
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
                        source='/tmpp/remote_pacha')
        sys.stdout = MockSys()
        sys.exit = MockSys()
        run.retrieve_files()
        actual = sys.stdout.captured()
        expected = """
Pacha was not able to retrieve the files from the SSH server provided.
Check your configuration file settings and try again.
"""
        self.assertEqual(actual, expected) 


    def test_retrieve_files_move_existing_file(self):
        """if there is an exisiting file when retrieving - move it"""
        os.makedirs('/tmp/remote_pacha/localhost/etc')
        os.mkdir('/tmp/remote_pacha/localhost/home')
        remote_file = open('/tmp/remote_pacha/localhost/etc/etc.conf', 'w')
        remote_file.write("remote second file")
        remote_file.close()
        remote_file = open('/tmp/remote_pacha/localhost/home/home.conf', 'w')
        remote_file.write("remote file")
        remote_file.close()
        server = "%s@%s" % (self.username, host.hostname()) 
        os.mkdir('/tmp/localhost')

        run = rebuild.Rebuild(server=server,
                        hostname='localhost', 
                        source='/tmp/remote_pacha')
        run.retrieve_files()
        result_1 = os.path.isfile('/tmp/localhost/etc/etc.conf')
        result_2 = os.path.isfile('/tmp/localhost/home/home.conf')
        result_3 = os.path.isdir('/tmp/localhost.%s' % strftime('%H%M%s'))
        line = open('/tmp/localhost/etc/etc.conf')
        remote_line = line.readline()
        self.assertEqual(remote_line, "remote second file")
        self.assertTrue(result_3)
        self.assertTrue(result_2)
        self.assertTrue(result_1)


    def test_pre_hooks(self):
        """Execute pre hook script"""
        os.makedirs('/tmp/localhost/pacha_pre')
        touch_script = open('/tmp/localhost/pacha_pre/foo.sh', 'w')
        touch_script.write('''touch /tmp/localhost/pre_got_executed.txt''')
        touch_script.close()
        run = rebuild.Rebuild(hostname='localhost') 
        run.pre_hooks()
        self.assertTrue(os.path.isfile('/tmp/localhost/pre_got_executed.txt'))


    def test_post_hooks(self):
        """Execute post hook script"""
        os.makedirs('/tmp/localhost/pacha_post')
        touch_script = open('/tmp/localhost/pacha_post/bar.sh', 'w')
        touch_script.write('''touch /tmp/localhost/post_got_executed.txt''')
        touch_script.close()
        run = rebuild.Rebuild(hostname='localhost') 
        run.post_hooks()
        self.assertTrue(os.path.isfile('/tmp/localhost/post_got_executed.txt'))


    def test_pre_post_hooks(self):
        """Execute both pre and post hooks"""
        os.makedirs('/tmp/localhost/pacha_pre')
        os.makedirs('/tmp/localhost/pacha_post')
        pre_script = open('/tmp/localhost/pacha_pre/foo.sh', 'w')
        pre_script.write('''touch /tmp/localhost/pre_got_executed.txt''')
        pre_script.close()
        post_script = open('/tmp/localhost/pacha_post/bar.sh', 'w')
        post_script.write('''touch /tmp/localhost/post_got_executed.txt''')
        post_script.close()
        run = rebuild.Rebuild(hostname='localhost') 
        run.pre_hooks()
        run.post_hooks()
        self.assertTrue(os.path.isfile('/tmp/localhost/post_got_executed.txt'))
        self.assertTrue(os.path.isfile('/tmp/localhost/pre_got_executed.txt'))


    def test_retrieve_files_with_pre_hook(self):
        """Retrieve files and execute the pre_hook if found"""
        os.makedirs('/tmp/remote_pacha/localhost/etc')
        os.mkdir('/tmp/remote_pacha/localhost/home')
        remote_file = open('/tmp/remote_pacha/localhost/etc/etc.conf', 'w')
        remote_file.write("remote second file")
        remote_file.close()
        remote_file = open('/tmp/remote_pacha/localhost/home/home.conf', 'w')
        remote_file.write("remote file")
        remote_file.close()
        os.makedirs('/tmp/remote_pacha/localhost/pacha_pre')
        touch_script = open('/tmp/remote_pacha/localhost/pacha_pre/foo.sh', 'w')
        touch_script.write('''touch /tmp/remote_pacha/localhost/pre_got_executed.txt''')
        touch_script.close()
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
        self.assertTrue(os.path.isfile('/tmp/remote_pacha/localhost/pre_got_executed.txt'))


    def test_rebuild_no_db(self):
        """Run a full rebuild and fail because no db was found"""
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
        sys.stdout = MockSys()
        sys.exit = MockSys()
        run.retrieve_files()
        run.replace_manager()
        actual = sys.stdout.captured()
        expected = """Could not find DB at /tmp/localhost/db/pacha.db\n"""
        self.assertEqual(actual, expected) 


    def test_rebuild(self):
        """Test a simple rebuild with some files in the pacha.db"""
        pacha.DB_DIR = '/tmp/pacha_test/db'
        pacha.DB_FILE ='/tmp/pacha_test/db/pacha_test.db' 
        pacha.permissions.DB_FILE ='/tmp/pacha_test/db/pacha_test.db' 
        pacha.hg.DB_FILE ='/tmp/pacha_test/db/pacha_test.db' 
        pacha.database.DB_FILE = '/tmp/pacha_test/db/pacha_test.db'
        pacha.database.DB_DIR = '/tmp/pacha_test/db'
        pacha.daemon.PID_DIR = '/tmp/pacha_test'

        os.makedirs('/tmp/pacha_test/db')
        os.makedirs('/tmp/remote_pacha/hosts/%s' % host.hostname())
        cmd = pacha.PachaCommands(test=True, parse=False, db=ConfigMapper('/tmp/pacha_test/db/pacha_test.db'),
            db_file='/tmp/pacha_test/db/pacha_test.db')
        cmd.add_config('/tmp/pacha_test/pacha.conf')
        cmd.check_config()
        os.makedirs('/tmp/pacha_test/foo/bar')
        test_file = open('/tmp/pacha_test/foo/bar/test.txt', 'w')
        test_file.write('file should be rebuilt')
        test_file.close()
        

        cmd.watch('/tmp/pacha_test/foo/bar')
        # do hg update on the newly cloned files: 
        hg_push_update('/tmp/remote_pacha/hosts/mbp.local/bar')
        

        # fake getting the db to the expected location 
        shutil.copy('/tmp/pacha_test/db/pacha_test.db' , '/tmp/remote_pacha/hosts/%s/db/pacha.db' % host.hostname())
        shutil.rmtree('/tmp/pacha_test')

        server = "%s@%s" % (self.username, host.hostname()) 
        run = rebuild.Rebuild(server=server,
                        hostname=host.hostname(), 
                        source='/tmp/remote_pacha/hosts')
        run.retrieve_files()
        self.assertFalse(os.path.exists('/tmp/pacha_test'))
        run.replace_manager()
        self.assertTrue(os.path.exists('/tmp/pacha_test/foo/bar'))
        self.assertEqual(open('/tmp/pacha_test/foo/bar/test.txt').readline(), 'file should be rebuilt')


if __name__ == '__main__':
    unittest.main()
