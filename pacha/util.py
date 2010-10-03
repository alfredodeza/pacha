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

CONFIG_GONE = YELLOW+"""
    +-----------------------------------------------------+
    |                   ** WARNING **                     |
    |                                                     |
    |  The config file supplied does not exist. Try       |
    |  adding a new valid path by running:                |
    |                                                     |      
    |    pacha --add-config /path/to/config               |
    |                                                     | 
    +-----------------------------------------------------+

"""+ENDS


WARNING = YELLOW+""" 
     +----------------------------------------------------+
     |                 ** WARNING **                      |
     |                                                    |
     |  You have not set a configuration file for Pacha.  |
     |  To add a configuration file, run:                 |
     |                                                    |
     |    pacha --add-config /path/to/config              |
     |                                                    |
     +----------------------------------------------------+

"""+ENDS

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
    db_file = file_dir+'/db/pacha.db'
    return db_file 

def get_db_dir():
    """Returns the absolute path  of the db directory"""
    # Fixes Database Absolute Location
    file_cwd =  path.abspath(__file__)
    file_dir = path.dirname(file_cwd)
    db_dir = file_dir+'/db'
    return db_dir 


