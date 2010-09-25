import unittest
import sys

import pacha 

WARNING = """ 
     +----------------------------------------------------+
     |                 ** WARNING **                      |
     |                                                    |
     |  You have not set a configuration file for Pacha.  |
     |  To add a configuration file, run:                 |
     |                                                    |
     |    pacha --add-config /path/to/config              |
     |                                                    |
     +----------------------------------------------------+

"""

class MockSys(object):
    """Can grab messages sent to stdout or stderr"""
    def __init__(self):
        self.message = ""

    def write(self, string):
        self.message = string 
        pass

class MockDatabase(object):
    """Avoids writing to an existing Database"""
    def __init__(self, config_path):
        self.value = ""
        self.config_path = [(config_path,)]

    def get_config_path(self):
        return self.config_path

class TestCommandLine(unittest.TestCase):

    def test_init(self):
        actual = pacha.PachaCommands(parse=False)
        """argv=None, test=False, parse=True, db=Worker())"""
        self.assertEqual(actual.test, False)
        self.assertEqual(actual.db.__module__, 'pacha.database' )


    def test_warning_message(self):
        actual = pacha.WARNING
        expected = WARNING
        self.assertEqual(actual, expected) 


    def test_display_message_out(self):
        # For this test, turn off stderr:
        sys.stderr = MockSys()
        sys.stdout = MockSys()
        cmds = pacha.PachaCommands(test=True, parse=False)
        cmds.msg("foo")
        actual = sys.stdout.message 
        self.assertEqual(actual, "foo") 

    def test_display_message_err(self):
        # For this test, turn off stdout:
        sys.stdout = MockSys()
        sys.stderr = MockSys()
        cmds = pacha.PachaCommands(test=True, parse=False)
        cmds.msg("snap", std="err")
        actual = sys.stderr.message 
        self.assertEqual(actual, "snap")

#    def test_check_config(self):
#        Worker = MockDatabase(config_path="/pacha.conf") 
#        actual = pacha.PachaCommands(parse=False, db=Worker).check_config() 
#        expected = defaults()
#        self.assertEqual(actual, expected) 
#
if __name__ == '__main__':
    unittest.main()
