#!/usr/bin/env python
#
# Copyright 2009 Alfredo Deza
#

# Layout to be
# Default use as standalone or client mode only (no server/client mode)
# Possibly read config file for Pacha
# Create controller for package installation
# Create controller for Bash/SH commands
# Create validation class for proper structure
# Create input values for command line options

import sys
from optparse import OptionParser
from subprocess import call
from lib import install, uninstall

# Do we need a class or a simple function?
#class InstallPackage(object):
#    """Calls the package manager to correctly install packages"""
    
#    def __init__(self, package):
#        self.package = package
    
# we are better off creating a class that reads the config
# files and then decides what needs to be done

#class Pacha(object):
#    """Reads the config file(s) and instantiates the values to controll
#    the deployment"""

#    def __init__(self,
#                conf_file='../apache2/main.conf'):
#        self.conf_file = conf_file
#        try:
#            get = confparser.Parse(conf_file)
#            get.options()
#            
#            self.package = get.package
#            print self.package
#            self.modules = get.modules # temporary hack, we need Pacha to be able
                                       # to tell what package is dealing with
#        except IOError:
#            print "Maybe you got the wrong path?"

#    def install(self):
#        """Installs the package"""
#        install = "apt-get install %s" % self.package
#        if len(self.modules) > 0:
#            for module in self.modules:
#                a2enmod = "a2enmod %s" % module
#                call(a2enmod, shell=True)
#        call(install, shell=True)
    
    
def main():
    """All command line options happen here"""
    parser = OptionParser()
    parser.add_option('--install', action="store_true",
        help="Installs pacha to /opt/ and creates the symlinks")

    parser.add_option('--uninstall', action="store_true",
            help="Destroys the symlinks and all pacha installed files")

    parser.add_option('--add-host',
            help="Creates structure for saving a host configs")

    options, arguments = parser.parse_args()

    # Cleanest way to show the help menu if no options are given
    if len(sys.argv) == 1:
        parser.print_help()

    if options.install:
        install.main()

    if options.uninstall:
        uninstall.main()

if __name__ == '__main__':
    main()
     
