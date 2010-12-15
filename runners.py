import sys
from guachi                             import ConfigMapper
from teja.util                          import get_db_file, get_db_dir


DB_FILE = get_db_file()
DB_DIR = get_db_dir()


 
class TestRunner(object):

    def __init__(self, 
            argv=None, 
            db=ConfigMapper(DB_FILE)):

        self.db = db 
        self.argv = argv
    
    def _environ_path(self):
        """Make sure the config path is added to the path"""
        conf = self.db.stored_config()
        config_path = conf['config_path']
        if config_path not in sys.path:
            sys.path.append(config_path)

    def run(self):
        self._environ_path()
        conf = self.db.stored_config()
        runner = conf['runner']
        if runner == 'pytest':
            self.pytest()
        elif runner == 'nose':
            print "Booo...  nose is not yet implemented"


    def pytest(self):
        import pytest

        # pytest freaks out with an empty argv
        if not self.argv:
            pytest.main()
        else:
            pytest.main()

        


