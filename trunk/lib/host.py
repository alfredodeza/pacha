# Copyright 2009-2010 Alfredo Deza
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Manages storing a host config file, like locations and creating directory 
structures."""

import os
import sys
import log

class Host(object):
    """Main class for managing host config file structure"""

    def __init__(self,
            host = None,
            package = None
            ):
        self.host = host
        self.package = package
        self.host_dir = '/opt/pacha/hosts/'+self.host

    def create(self):
        """Builds the initial structure for a host"""
        if os.path.isdir(self.host_dir) is not True:
            os.mkdir(self.host_dir)
            info = 'created host directory %s' % self.host_dir
            log.append(module='host', line=info)
        else:
            info = '%s already present'
            log.append(module='host', type='WARNING', line=info)

def hostname():
    """Return the hostname of this machine"""
    name = os.uname()[1]
    return name
