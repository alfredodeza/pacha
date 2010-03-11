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
from optparse import OptionParser, OptionGroup
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

    parser.add_option('--watch-single',
           help="Provide a single file for Pacha to watch in a given\
 directory. Everything else in the directory will be ignored.\
 Also used to add more individual files to track within the same\
 directory (e.g. like tracking .vimrc in $HOME)") 

    group = OptionGroup(parser, "Rebuilding Options", "When rebuilding\
 a host, you will need to pass a few required options to Pacha so it can\
 connecto to a remote host via SSH and copy the needed files.")
    

    group.add_option('--rebuild', action="store_true",
            help="""Combined with other options it rebuilds the
 given host with all tracked files. Doesn't take any arguments.""")

    group.add_option('--host',
            help="""Prompts some questions and then rebuilds the
 given host with all tracked files""")

    group.add_option('--ssh-server', 
            help="""The server to connect to pull the files from""")

    group.add_option('--ssh-user',
            help="""User that authenticates to the Pacha server when 
 rebuilding""")

    parser.add_option_group(group)

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

        if options.watch_single:
            if os.path.isfile(options.watch_single):
                # can't pass a single file to hg.Hg so 
                # convert it to file path without the file here
                # whatever we receive (either a full path or a single
                # file name 
                abspath = os.path.abspath(options.watch_single)
                # now we need only the directory name:
                dirname = os.path.dirname(abspath)
                # get the abs_path and add '.hgignore' and make
                # sure it does not exist, 
                hgignore = dirname+'/.hgignore'
                if os.path.isfile(hgignore): # make sure we arent overwriting
                    # so this means we are already watching unique files here
                    # so let's add the new guy and commit it
                    mercurial = hg.Hg(path=dirname)
                    mercurial.hg_add(abspath)
                    mercurial.commit()

                #if it does not exist then this should be the first 
                # time this is being run here right?
                # pass it on to:
                else:
                    mercurial = hg.Hg(path=dirname)
                    # then ignore everythin withn the path
                    mercurial.hgignore()
                    mercurial.initialize()
                    mercurial.hg_add(single=abspath)
                    mercurial.commit()
                    mercurial.clone()
                    #at the end of everything we put the hgrc method in
                    mercurial.hgrc()
                # now insert the whole path into the database to 
                # check for it here. DB can figure out if
                # it is a duplicate so no double checking
                # before inserting
                db = database.Worker()
                db.insert(path=abspath)

            else:
                print "You have provided a wrong or non-existent path\
 to a file"

        if options.rebuild and options.ssh_server and options.ssh_user\
                and options.host:
            print "SSH Server: \t\t%s" % options.ssh_server
            print "SSH User: \t\t%s" % options.ssh_user
            print "Host to rebuild: \t%s" % options.host

# NEEDS VERIFICATION AFTER METHOD MOD
#            try:
#                run = rebuild.Rebuild()
#                run.retrieve_files()
#                run.install()
#                run.replace_manager()
#
#            except KeyboardInterrupt:
#                sys.exit(1)
#
        if options.upgrade:
            upgrade.main()

if __name__ == '__main__':
    main()

