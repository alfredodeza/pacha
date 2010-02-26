import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
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

if __name__ == '__main__':
    unittest.main()
