
#!/usr/bin/env python
#
# Copyright (c) 2009-2010 Alfredo Deza <alfredodeza [at] gmail [dot] com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import getpass
import os
import sys
from optparse import OptionParser, OptionGroup
import hg, host, rebuild,database, permissions

def main():
    """All command line options happen here"""
    parser = OptionParser(description="""For more detailed option 
descriptions please visit:
http://code.google.com/p/pacha/wiki/Options"""
    ,version='0.2.0')

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
 connect to a remote host via SSH and copy the needed files.")

    group.add_option('--rebuild', action="store_true",
            help="""Combined with other options it rebuilds the
 given host with all tracked files. Doesn't take any arguments.""")

    group.add_option('--host',
            help="""Indicates the name of the host you want to rebuild""")

    group.add_option('--ssh-server', 
            help="""The server to connect to pull the files from""")

    group.add_option('--ssh-user',
            help="""User that authenticates to the Pacha server when 
 rebuilding""")

    parser.add_option_group(group)

    # Check for sudo privileges before annything else:
    #if getpass.getuser() != 'root':
    #    sys.stderr.write(" * Pacha needs sudo privileges to run *\n")
    #    sys.exit(1)

    # now check for mercurial:
    #if os.path.isfile('/usr/bin/hg') == False:
    #    sys.stderr.write(" * Pacha needs Mercurial installed to run *\n")

#    else:
    options, arguments = parser.parse_args()

    # Cleanest way to show the help menu if no options are given
    if len(sys.argv) == 1:
        parser.print_help()

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
        db.insert(path=path, type='dir')
        # now make sure we record permissions metadata
        meta = permissions.Tracker(path=path)
        meta.walker()

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
            # permissions metadata
            meta = permissions.Tracker(path=abspath)
            meta.single_file()
            if os.path.isfile(hgignore): # make sure we arent overwriting
                # we are already watching unique files here
                # so let's add the new guy and commit it
                mercurial = hg.Hg(path=dirname)
                mercurial.hg_add(abspath)
                mercurial.commit()

            # if it does not exist then this should be the first 
            # time this is being run here 
            else:
                mercurial = hg.Hg(path=dirname)
                # then ignore everything within the path
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
            db.insert(path=abspath, type='single')

        else:
            print "You have provided a wrong or non-existent path\
to a file"

    if options.rebuild and options.ssh_server and options.ssh_user\
            and options.host:
        print "SSH Server: \t\t%s" % options.ssh_server
        print "SSH User: \t\t%s" % options.ssh_user
        print "Host to rebuild: \t%s" % options.host
        
        try:
            confirm = raw_input("Hit Enter to confirm or Ctrl-C to cancel")

            run = rebuild.Rebuild(options.ssh_server,
                    options.ssh_user,
                    options.host)
            run.retrieve_files()
            run.install()
            run.replace_manager()

        except KeyboardInterrupt:
            print "\nExiting nicely from Pacha"
            sys.exit(1)

if __name__ == '__main__':
    main()

