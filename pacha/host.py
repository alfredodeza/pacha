"""Manages storing a host config file, like locations and creating directory 
structures."""

import os

class Host(object):
    """Main class for managing host config file structure"""

    def __init__(self,
            host = None,
            host_path = None
            ):
        self.host = host
        self.host_path = os.path.abspath(host_path)
        self.host_dir = self.host_path+'/'+self.host

    def create(self):
        """Builds the initial structure for a host"""
        if os.path.isdir(self.host_dir):
            return False
        else:
            os.mkdir(self.host_dir)
            return True

def hostname():
    """Return the hostname of this machine"""
    name = os.uname()[1]
    return name
