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

class Rotate(object):
    """A simple approach to rotating a log file by compressing and
    deleting old files"""

    def __init__(self,
            location='/opt/pacha/log',
            max_size=10,
            compress=True,
            max_items=5):
 
        self.location = location
        self.max_size = max_size
        self.compress = compress
        self.max_items = max_items  

    def manager(self):
        """Handles all the logic fromo init to perform
        the actual rotation"""
    # get size of pacha.log
    # set max size of pacha.log
    # if size > max_size then compress
    # compress to tar.gz
    # check how many tar.gz are there
    # if more than 5, then delete the oldest one
    # rename all the log files pacha.log.+1.tar.gz
    # be done


    def location_verify(self):
        """Make sure a log file is there, otherwise we end up
        with errors"""

    def item_count(self):
        """Return how many items do we have here"""

    def get_size(self):
        """Get the total size of an item"""

    def compress(self, item):
        """Compresses a single item"""

    def rename(self, item):
        """For rotation we need to rename the file"""

    def delete(self, item):
        """After rotation a file need to get deleted"""

