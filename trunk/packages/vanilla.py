#!/usr/bin/env python
#
#
# Vanilla installation of packages
#
#

from subprocess import call

def install(package):
    """Main function to install a single package"""
    command = 'apt-get -y install %s' % package
    call(command, shell=True)
