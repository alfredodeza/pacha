"""Manages storing a host config file, like locations and creating directory 
structures."""

import os
import log

class Host(object):
    """Main class for managing host config file structure"""

    def __init__(self,
            host = None,
            host_path = None,
            package = None
            ):
        self.host = host
        self.host_path = os.path.abspath(host_path)
        self.package = package
        self.host_dir = self.host_path+'/'+self.host

    def create(self):
        """Builds the initial structure for a host"""
        if os.path.isdir(self.host_dir) is not True:
            os.mkdir(self.host_dir)
            info = 'created host directory %s' % self.host_dir
            log.host.debug(info)
        else:
            info = '%s already present' % self.host
            print info
            log.host.debug(info)
            return False

def hostname():
    """Return the hostname of this machine"""
    name = os.uname()[1]
    return name
