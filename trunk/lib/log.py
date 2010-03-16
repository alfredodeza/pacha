"""Handles all logging for Pacha. Not using Python's logging module
knowlingly. Because it is absolutely HORRIBLE."""

import os
import sys
from time import strftime

def append(module='pacha', 
        type='INFO', 
        line='',
        log_file = '/opt/pacha/log/pacha.log'):
    """Simple function to write to a log file"""

    try:
        if os.path.isfile(log_file):
            open_log = open(log_file, 'a')
        else:
            open_log = open(log_file, 'w')

        timestamp = strftime('%b %d %H:%M:%S')
        log_line = "%s %s %s %s" % (timestamp, type, module, line)
        open_log.write(log_line+'\n')
        open_log.close()

    except IOError:
        sys.stderr.write("Permission denied to write log file ")
        sys.exit(1)

def rotate():
    """In charge of rotating the Pacha log, compressing 
    and deleting old log files"""
    # get size of pacha.log
    # set max size of pacha.log
    # if size > max_size then compress
    # compress to tar.gz
    # check how many tar.gz are there
    # if more than 5, then delete the oldest one
    # rename all the log files pacha.log.+1.tar.gz
    # be done


