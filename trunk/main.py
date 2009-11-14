# main.py
#
# Copyright 2009 Alfredo Deza
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Layout to be
# Default use as standalone or client mode only (no server/client mode)
# Possibly read config file for Pacha
# Create controller for package installation
# Create controller for Bash/SH commands
# Create validation class for proper structure
# Create input values for command line options

from optparse import OptionParser
from subprocess import call
from lib import confparser

# Do we need a class or a simple function?
class InstallPackage(object):
    """Calls the package manager to correctly install packages"""
    
    def __init__(self, package):
        self.package = package

# Maybe a function works better at handling a pacackage install:

#def install(package)
#    """Handles the package installation via the main.conf file ONLY"""
    
# we are better off creating a class that reads the config
# files and then decides what needs to be done

class Pacha(object):
    """Reads the config file(s) and instantiates the values to controll
    the deployment"""

    def __init__(self,
                conf_file='../apache2/main.conf'):
        self.conf_file = conf_file
        try:
            get = confparser.Parse(conf_file)
            get.options()
            
            self.package = get.package
            print self.package
            self.modules = get.modules # temporary hack, we need Pacha to be able
                                       # to tell what package is dealing with
        except IOError:
            print "Maybe you got the wrong path?"

    def install(self):
        """Installs the package"""
        install = "apt-get install %s" % self.package
        if len(self.modules) > 0:
            for module in self.modules:
                a2enmod = "a2enmod %s" % module
                call(a2enmod, shell=True)
        call(install, shell=True)
        
if __name__ == '__main__':
    n = Pacha()
    n.install()
     
