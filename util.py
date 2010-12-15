from os             import path
from subprocess     import Popen, PIPE


# Easy way to implement colors in the terminal
# for actual use, you need to always end with ENDC
# For red text: 
# print RED+"a red string"+ENDS

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDS = '\033[0m'


WARNING = YELLOW+""" 
     +----------------------------------------------------+
     |                 ** NOTICE **                       |
     |                                                    |
     |  You have not set a config path for Teja.          |
     |  To add a path to load your configs with run:      |
     |                                                    |
     |    teja --config-path /path/to/config/dir          |
     |                                                    |
     +----------------------------------------------------+

"""+ENDS

def sanitize_argv(argv):
    """Make sure we have a clean argv for the test runners 
    """
    return argv[1:]
    

def run_command(std, cmd):
    """Runs a command via Popen"""
    if std == "stderr":
        run = Popen(cmd, shell=True, stderr=PIPE)
        out = run.stderr.readlines()
    if std == "stdout":
        run = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out = run.stdout.readlines()
    return out

def get_db_file():
    """Returns the absolute path of the database"""
    # Fixes Database Absolute Location
    file_cwd =  path.abspath(__file__)
    file_dir = path.dirname(file_cwd)
    db_file = file_dir+'/db/teja.db'
    return db_file 

def get_db_dir():
    """Returns the absolute path  of the db directory"""
    # Fixes Database Absolute Location
    file_cwd =  path.abspath(__file__)
    file_dir = path.dirname(file_cwd)
    db_dir = file_dir+'/db'
    return db_dir 

def get_pid_dir():
    """Returns the absolute dir path for the daemon"""
    file_cwd =  path.abspath(__file__)
    file_dir = path.dirname(file_cwd)
    return file_dir


