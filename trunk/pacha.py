#!/usr/bin/env python
#
# Copyright 2009 Alfredo Deza
#

# Create controller for package installation
# Create controller for Bash/SH commands
from subprocess import call
import os
import sys
from optparse import OptionParser
from lib import install, uninstall, hg, host, rebuild
    
def main():
    """All command line options happen here"""
    parser = OptionParser()
    parser.add_option('--install', action="store_true",
        help="Installs pacha to /opt/ and creates the symlinks")

    parser.add_option('--uninstall', action="store_true",
            help="Destroys the symlinks and all pacha installed files")

    parser.add_option('--add-host',
            help="Creates structure for saving a host configs")

    parser.add_option('--watch', action="store_true",
           help="Provide a path for Pacha to watch")

    parser.add_option('--rebuild', action="store_true",
            help="Rebuilds all tracked files")

    options, arguments = parser.parse_args()

    # Cleanest way to show the help menu if no options are given
    if len(sys.argv) == 1:
        parser.print_help()

    if options.install:
        install.main()
        print "Pacha finished installing."
        print "############################################################"
        print """Remember to edit pacha.conf and run:
pacha --watch /opt/pacha/conf
This will keep track of all host specific configurations that will be needed
when rebuilding."""

    if options.uninstall:
        uninstall.main()
        print "Pacha finished uninstalling."

    if options.add_host:
        new = host.Host(host=options.add_host)
        new.create()

    if options.watch:
        # a hack to have ambiguous optparse behavior 
        if len(sys.argv) is 2: #no path
            path = os.getcwd()
        if len(sys.argv) >=3: #with path
            path = sys.argv[2]
        mercurial = hg.Hg(path=path)
        mercurial.hgrc()
        # we do a first time clone:
        mercurial.clone()
        # add the path to .repos
        repos = open('/opt/pacha/conf/.repos', 'a')
        repos.write(path)
        repos.close()

    if options.rebuild:
        try:
            run = rebuild.Rebuild()
            run.retrieve_files()
            run.install()
            run.specific_tracking()

        except KeyboardInterrupt:
            sys.exit(1)

if __name__ == '__main__':
    main()

