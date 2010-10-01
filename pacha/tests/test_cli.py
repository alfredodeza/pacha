import unittest
import sys
import os

from mock import MockSys
from guachi import ConfigMapper
from pacha import config
import pacha 



CONFIG_GONE = """
    +-----------------------------------------------------+
    |                   ** WARNING **                     |
    |                                                     |
    |  The config file supplied does not exist. Try       |
    |  adding a new valid path by running:                |
    |                                                     |      
    |    pacha --add-config /path/to/config               |
    |                                                     | 
    +-----------------------------------------------------+


"""



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


class MockDatabase(object):
    """Avoids writing to an existing Database"""
    def __init__(self, config_path):
        self.value = ""
        self.config_path = [(config_path,)]

    def get_config_path(self):
        return self.config_path

class TestCommandLine(unittest.TestCase):

    def setUp(self):
        # make sure we do not have db file 
        test_db = '/tmp/pacha_test.db'
        if os.path.isfile(test_db):
            os.remove(test_db)

    def test_init(self):
        actual = pacha.PachaCommands(parse=False)
        """argv=None, test=False, parse=True, db=Worker())"""
        self.assertEqual(actual.test, False)
        self.assertEqual(actual.db.__module__, 'guachi' )

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
        actual = sys.stdout.captured() 
        self.assertEqual(actual, "foo") 

    def test_display_message_err(self):
        # For this test, turn off stdout:
        sys.stdout = MockSys()
        sys.stderr = MockSys()
        cmds = pacha.PachaCommands(test=True, parse=False)
        cmds.msg("snap", std="err")
        actual = sys.stderr.captured() 
        self.assertEqual(actual, "snap")

    def test_check_config(self):
        pacha.DB_FILE = '/tmp/pacha_test.db'
        commands = pacha.PachaCommands(test=True, parse=False, db=ConfigMapper('/tmp/pacha_test.db')) 
        commands.add_config('/tmp')
        conf = commands.check_config() 
        actual = len(conf.keys())
        config.DEFAULT_MAPPINGS['path'] = '/tmp'
        expected = len(config.DEFAULT_MAPPINGS.keys())
        self.assertEqual(actual, expected) 

    def test_check_config_error(self):
        """Don't set a path and get an error message"""
        sys.stderr = MockSys()
        pacha.DB_FILE = '/tmp/pacha_test.db'
        commands = pacha.PachaCommands(test=True, parse=False, db=ConfigMapper('/tmp/pacha_test.db')) 
        commands.check_config() 
        actual  = sys.stderr.captured()
        expected = WARNING
        self.assertEqual(actual, expected) 

    def test_check_config_gone(self):
        """Set a path that is not reachablei and get an error message"""
        pacha.DB_FILE = '/tmp/pacha_test.db'
        commands = pacha.PachaCommands(test=True, parse=False, db=ConfigMapper('/tmp/pacha_test.db')) 
        commands.add_config('/non/existent/path')
        conf = ConfigMapper('/tmp/pacha_test.db')
        db_conf = conf.stored_config()
        # force a config push/parse:
        for k,v in config.DEFAULT_MAPPINGS.items():
            db_conf[k] = v
        self.assertEqual(len(conf.stored_config().items()), 13) 
        sys.stdout = MockSys()
        commands.check_config() 
        actual  = sys.stdout.captured()
        expected = CONFIG_GONE
        self.assertEqual(actual, expected) 

    def test_add_config(self):
        """Add a configuration file to the config db"""
        pacha.DB_FILE = '/tmp/pacha_test.db'
        commands = pacha.PachaCommands(test=True, parse=False, db=ConfigMapper('/tmp/pacha_test.db')) 
        sys.stdout = MockSys()
        commands.add_config('/non/existent/path')
        conf = ConfigMapper('/tmp/pacha_test.db')
        db_conf = conf.stored_config()
        
        self.assertEqual(db_conf['path'], '/non/existent/path')
        self.assertEqual(sys.stdout.captured(), 'Configuration file added: /non/existent/path')


if __name__ == '__main__':
    unittest.main()
