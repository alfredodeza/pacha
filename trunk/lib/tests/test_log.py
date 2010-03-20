import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
import tarfile
import shutil
import unittest
import log

class TestAppend(unittest.TestCase):

    def setUp(self):
        """call the append function before testing"""
        log.append(module='test', type='INFO', line='running a test',
                log_file = '/tmp/test.log')

    def test_log_exists(self):
        """Check if the log file was created"""
        log = os.path.isfile('/tmp/test.log')
        self.assertTrue(log)

    def test_append(self):
        """Opens the previously created log file and checks the line"""
        log_line = open('/tmp/test.log').readline()
        info = "INFO test running a test"
        if info in log_line:
            assert True
        else:
            assert False

    def tearDown(self):
        """Delete the log file that was created for the test"""
        os.remove('/tmp/test.log')

class TestRotate(unittest.TestCase):

    def setUp(self):
        """call the append function before testing to add some lines"""
        os.mkdir('/tmp/testlog')
        log.append(module='test', type='INFO', line='running a test',
                log_file = '/tmp/testlog/test.log')
        
    def test_location_verify(self):
        """Verify the location verifier"""
        rotate = log.Rotate(location='/tmp/testlog',
                max_size=1,
                max_items=3,
                log_name='test.log')
        self.assertTrue(rotate.location_verify())

    def test_item_count(self):
        """Return the total number of files"""
        rotate = log.Rotate(location='/tmp/testlog',
                max_size=1,
                max_items=3,
                log_name='test.log')
        expected = 1
        actual = rotate.item_count()
        self.assertEqual(actual, expected)

    def test_get_size(self):
        """Verify the correct size of a file"""
        rotate = log.Rotate(location='/tmp/testlog',
                max_size=1,
                max_items=3,
                log_name='test.log')
        expected = 41
        actual = rotate.get_size('/tmp/testlog/test.log')
        self.assertEqual(actual, expected)

    def test_compress(self):
        """Compress a given file"""
        rotate = log.Rotate(location='/tmp/testlog',
                max_size=1,
                max_items=3,
                log_name='test.log')
        rotate.compress('/tmp/testlog/log.tar.gz',
                '/tmp/testlog/test.log')
        try:
            tarfile.open('/tmp/testlog/log.tar.gz', 'r:gz')
            gz = True
        except ReadError:
            gz = False
        self.assertTrue(gz)


    def tearDown(self):
        """Delete the log file that was created for the test"""
        shutil.rmtree('/tmp/testlog')


if __name__ == '__main__':
    unittest.main()
