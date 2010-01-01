#!/usr/bin/env python
#
# Copyright 2009 Alfredo Deza
#

# Create controller for package installation
# Create controller for Bash/SH commands

import sys
from optparse import OptionParser
from subprocess import call
from lib import install, uninstall, hg, host
    
def main():
    """All command line options happen here"""
    parser = OptionParser()
    parser.add_option('--install', action="store_true",
        help="Installs pacha to /opt/ and creates the symlinks")

    parser.add_option('--uninstall', action="store_true",
            help="Destroys the symlinks and all pacha installed files")

    parser.add_option('--add-host',
            help="Creates structure for saving a host configs")

    parser.add_option('--watch',
           help="Provide a path for Pacha to watch")


    options, arguments = parser.parse_args()

    # Cleanest way to show the help menu if no options are given
    if len(sys.argv) == 1:
        parser.print_help()

    if options.install:
        install.main()

    if options.uninstall:
        uninstall.main()

    if options.add_host:
        new = host.Host()
        new.create()

    if options.watch:
        mercurial = hg.Hg()
        mercurial.hgrc(options.watch)

if __name__ == '__main__':
    main()

# TODO
# Pacha WATCH needs to create the hostname directory in the remote PAChA Server
# Pacha WATCH needs to clone the current repo to PACHA SERVER
# the parameter for WATCH needs to be automatic from `pwd` (e.g. you need to be in
# the same directory to watch.
