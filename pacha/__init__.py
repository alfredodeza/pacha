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


import os
import sys
from optparse import OptionParser, OptionGroup
import hg, host, rebuild,database, permissions
from pacha.config_options import config_options


def main():
    """All command line options happen here"""
    parser = OptionParser(description="""
A systems configuration management engine
"""
    ,version='0.2.0')

    parser.add_option('--config-values', action="store_true",
            help="""Displays the current configuration values used""")

    parser.add_option('--add-config',
            help="""Adds a path to a configuration file""")

    parser.add_option('--remove-config', action="store_true",
            help="""Removes the stored configuration file""")

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

    daemon_group = OptionGroup(parser, "Daemon Options", "Pacha is able to\
run in the background, these options will help you manage the daemon")

    daemon_group.add_option('--daemon-start', action='store_true',
            help="Starts the Pacha daemon")

    daemon_group.add_option('--daemon-stop', action='store_true',
            help="Stops the Pacha daemon")

    daemon_group.add_option('--daemon-status', action='store_true',
            help="Checks the status of the Pacha daemon")

    parser.add_option_group(daemon_group)


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

    options, arguments = parser.parse_args()

    # Cleanest way to show the help menu if no options are given
    if len(sys.argv) == 1:
        parser.print_help()


    if options.add_config:
        db = database.Worker()
        abspath = os.path.abspath(options.add_config)
        db.add_config(abspath)
        print "Configuration file added: %s" % abspath

    if options.config_values:
        try:
            db = database.Worker()
            config_list = [i for i in db.get_config_path()]
            config_file = config_list[0][0]
            config = config_options(config_file)
            print "Current config values are:\n%s" % config
        except Exception, error:
            print "Could not complete command: %s" % error 


    if options.remove_config:
        db = database.Worker()
        db.remove_config()
        print "Configuration file(s) removed"
        sys.exit(0)

    # if any commands are run, check for a MASTER config file Location
    db = database.Worker()
    config_db = db.get_config_path()
    config_file = None
    try:
        config_list = [i for i in db.get_config_path()]
        config_file = config_list[0][0]
        config = config_options(config_file)
    except IndexError:
        print """
        
*********************************************************

Warning! You have not set a configuration file for Pacha.
To add a configuration file, run:
    pacha --add-config /path/to/config 
"""
        sys.exit(1)

    if options.add_host:
        try:
            new = host.Host(host=options.add_host, 
                    host_path=config['hosts_path'])
            new.create()
            print "Added host %s" % options.add_host
        except Exception, error:
            print "Could not complete command: %s" % error 

    if options.watch:
        try:
            # a hack to have ambiguous optparse behavior 
            if len(sys.argv) is 2: #no path
                path = os.getcwd()
            if len(sys.argv) >=3: #with path
                path = sys.argv[2]
            mercurial = hg.Hg(path=path, conf=config_options(config_file))
            mercurial.hgrc()
            # we do a first time clone:
            mercurial.clone()
            # add the path to repos table in database
            db = database.Worker()
            db.insert(path=path, type='dir')
            # now make sure we record permissions metadata
            meta = permissions.Tracker(path=path)
            meta.walker()
        except Exception, error:
            print "Could not complete command: %s" % error 


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

