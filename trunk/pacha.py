#!/usr/bin/env python
#
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

import getpass
import os
import sys
from optparse import OptionParser
from lib import install, uninstall, hg, host, rebuild, upgrade, database
    
def main():
    """All command line options happen here"""
    parser = OptionParser(description="""For more detailed option 
descriptions please visit:
http://code.google.com/p/pacha/wiki/Options"""
    ,version='0.0.5')
    parser.add_option('--install', action="store_true",
        help="Installs pacha to /opt/ and creates the symlinks")

    parser.add_option('--uninstall', action="store_true",
            help="Destroys the symlinks and all pacha installed files")

    parser.add_option('--add-host',
            help="""Creates structure for saving host configs
 only meant for Pacha server""")

    parser.add_option('--watch', action="store_true",
           help="Provide a path for Pacha to watch and keep track of")  

    parser.add_option('--watch-single', action="store_true",
           help="Provide a single file for Pacha to watch in a given\
 directory. Everything else in the directory will be ignored.\
 Also used to add more individual files to track within the same\
 directory (e.g. like tracking .vimrc in $HOME)") 

    parser.add_option('--rebuild', action="store_true",
            help="""Prompts some questions and then rebuilds the
 given host with all tracked files""")

    parser.add_option('--upgrade', action="store_true",
            help="""Upgrades to a newer version by pulling the latest
 .tar.gz file.""")

    # Check for sudo privileges before annything else:
    if getpass.getuser() != 'root':
        sys.stderr.write(" * Pacha needs sudo privileges to run *\n")
        sys.exit(1)

    # now check for mercurial:
    if os.path.isfile('/usr/bin/hg') == False:
        sys.stderr.write(" * Pacha needs Mercurial installed to run *\n")

    else:
        options, arguments = parser.parse_args()

        # Cleanest way to show the help menu if no options are given
        if len(sys.argv) == 1:
            parser.print_help()
    
        if options.install:
            install.main()
            print " * Pacha finished installing."
            print """ * Remember to edit pacha.conf and run:
pacha --watch /opt/pacha/conf
 * This will keep track of all host specific configurations that will be needed
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
            # add the path to repos table in database
            db = database.Worker()
            db.insert(path=path)

        if options.rebuild:
            try:
                run = rebuild.Rebuild()
                run.retrieve_files()
                run.install()
                run.replace_manager()

            except KeyboardInterrupt:
                sys.exit(1)

        if options.upgrade:
            upgrade.main()

if __name__ == '__main__':
    main()

