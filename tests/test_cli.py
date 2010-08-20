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


class TestCommandLine(unittest.TestCase):

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

    


if __name__ == '__main__':
    unittest.main()
