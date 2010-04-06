"""Handles all logging for Pacha. Not using Python's logging module
knowlingly. Because it is absolutely HORRIBLE."""

import os
import sys
import tarfile
from time import strftime

def append(module='pacha', 
        type='INFO', 
        line='',
        log_file = '/opt/pacha/log/pacha.log'):
    """Simple function to write to a log file"""

    # every time we are called, check the size
    # and attempt log rotation
    rotate = Rotate()
    rotate.manager()
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
            max_size=10485760, # 10 megabytes in kilobytes
            max_items=5,
            log_name='pacha.log'):
 
        self.location = location
        self.max_size = max_size
        self.max_items = max_items  
        self.log_name = log_name
        self.log_path = os.path.join(location, log_name)

    def manager(self):
        """Handles all the logic from init to perform
        the actual rotation"""
        if self.get_size(self.log_path) > self.max_size:
            if self.location_verify():
                if self.item_count() == 1: # nothing compressed yet
                    newest = '%s.1.tar.gz' % self.log_path
                    self.compress(newest, self.log_path)
                    self.remove(self.log_path)
                else:
                    # start with the oldest file possible
                    oldest = '%s.%s.tar.gz' % (self.log_path, self.max_items)
                    if os.path.isfile(oldest):
                        self.remove(oldest) # we get rid of it
                    for number in reversed(range(self.item_count())):
                        norm_num = number + 1 # do not start numbering at cero
                        log_file = '%s.%d.tar.gz' % (self.log_path, norm_num)
                        if os.path.isfile(log_file):
                            new_number = norm_num + 1 
                            new_name = '%s.%d.tar.gz' % (self.log_path, 
                                    new_number)
                            os.rename(log_file, new_name)
                    # above rotates everything except the uncompressed log:
                    gz_name = '%s.1.tar.gz' % self.log_path
                    self.compress(gz_name, self.log_path)
                    # finally remove the log file
                    self.remove(self.log_path)
        else:
            pass # no log rotate needed

    def location_verify(self):
        """Make sure a log file is there, otherwise we end up
        with errors"""
        if os.path.isfile(self.log_path):
            return True
        else:
            return False

    def item_count(self):
        """Return how many items do we have here"""
        count = 0
        for item in os.listdir(self.location):
            count += 1
        return count

    def get_size(self, item):
        """Get the total size of an item"""
        size = os.path.getsize(item)
        return size

    def compress(self, gz_name, item):
        """Compresses a single item"""
        tar = tarfile.open(gz_name, 'w:gz')
        tar.add(item)
        tar.close()

    def remove(self, item):
        """After rotation a file needs to get deleted"""
        if os.path.exists(item):
            os.remove(item)

