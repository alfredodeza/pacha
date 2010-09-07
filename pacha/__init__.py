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

import logging
import os
import sys
from optparse import OptionParser, OptionGroup
from pacha.config import options
from pacha import daemon, hg, rebuild, permissions


from pacha.database import Worker, is_tracked
from pacha.host import Host

CONFIG_GONE = """
    +-----------------------------------------------------+
    |                   ** WARNING **                     |
    |                                                     |
    |  The config file supplied does not exist. Try       |
    |  adding a new valid path by running:                |
    |                                                     |      
    |    pacha --add-config /path/to/config               |
    |                                                     | 
    +-----------------------------------------------------+
"""


WARNING = """ 
     +----------------------------------------------------+
     |                 ** WARNING **                      |
     |                                                    |
     |  You have not set a configuration file for Pacha.  |
     |  To add a configuration file, run:                 |
     |                                                    |
     |    pacha --add-config /path/to/config              |
     |                                                    |
     +----------------------------------------------------+
"""
 
class PachaCommands(object):
    """A lot of complicated options can happen with Pacha, so 
    it is easier if everything lives under a class rather than
    the widely used main()"""

    def __init__(self, argv=None, test=False, parse=True, db=Worker()):
        self.db = db
        if argv is None:
            argv = sys.argv

        self.test = test
        if parse:
            self.parseArgs(argv)
        self.config = {}


    def msg(self, msg, std="out"):
        if std == "out":
            sys.stdout.write(msg)
        else:
            sys.stderr.write(msg)
        if not self.test:
            sys.exit(1)


    def check_config(self):
        # if any commands are run, check for a MASTER config file Location
        config_db = self.db.get_config_path()
        config_file = None
        try:
            config_list = [i for i in self.db.get_config_path()]
            config_file = config_list[0][0]
            config = options(config_file)
            return config
        except IndexError:
            self.msg(msg=WARNING, std="err")
 

    def add_config(self, path):
        db = Worker()
        abspath = os.path.abspath(path)
        db.add_config(abspath)
        self.msg("Configuration file added: %s" % abspath)


    def config_values(self):
        try:
            db = Worker()
            config_list = [i for i in db.get_config_path()]
            config_file = config_list[0][0]
            if os.path.isfile(config_file):
                config = options(config_file)
                print "\nConfiguration file: %s\n" % config_file
                for i in config.items():
                    print "%-15s= %-4s" % (i[0], i[1])
            else:
                print "\nConfiguration file: %s\n" % config_file
                print CONFIG_GONE 
        except Exception, error:
            print "Could not complete command: %s" % error 


    def set_logging(self):
        enabled = self.config['log_enable']
        log_path = self.config['log_path']

        levels = {
                'debug': logging.DEBUG,
               'info': logging.INFO
                }
        
        level = levels.get(self.config['log_level'].lower())
        log_format = self.config['log_format']
        datefmt = self.config['log_datefmt']

        logging.basicConfig(level=level,
                format=log_format,
                datefmt=datefmt)

        if not enabled and log_path is None:
            logging.disable(logging.CRITICAL)

    def add_host(self, host):
        try:
            new = Host(host=host, 
                    host_path=self.config['hosts_path'])
            new.create()
            print "Added host %s" % host
        except Exception, error:
            print "Could not complete command: %s" % error 


    def watch(self, path):                
        """
        3 things need to happen:
        *  track whatever we initially were asked for
        *  check if this is the first time we are run (db not tracked)
        *  track the db if it is not tracked or push it with the new dir
        """
        try:
            mercurial = hg.Hg(path=path, conf=self.config)
            mercurial.hgrc()
            # we do a first time clone:
            mercurial.clone()
            # add the path to repos table in database
            db = Worker()
            db.insert(path=path, type='dir')
            # now make sure we record permissions metadata
            meta = permissions.Tracker(path=path)
            meta.walker()
        except Exception, error:
            print "Could not complete command: %s" % error 

        # db tracking
        if not is_tracked():
            pacha_file = os.path.abspath(__file__)
            pacha_dir = os.path.dirname(pacha_file)
            db_dir = pacha_dir+'/db'

            try:
                mercurial = hg.Hg(path=db_dir, conf=self.config)
                mercurial.hgrc()
                # we do a first time clone:
                mercurial.clone()
                # add the path to repos table in database
                db = Worker()
                db.insert(path=path, type='dir')
                # now make sure we record permissions metadata
                meta = permissions.Tracker(path=path)
                meta.walker()
            except Exception, error:
                print "Could not complete command: %s" % error 


    def watch_single(self, s_file):
        if os.path.isfile(s_file):

            # can't pass a single file to hg.Hg so 
            # convert it to file path without the file here
            # whatever we receive (either a full path or a single
            # file name 
            abspath = os.path.abspath(s_file)

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
                mercurial = hg.Hg(path=dirname, conf=self.config)
                mercurial.hg_add(abspath)
                mercurial.commit()

            # if it does not exist then this should be the first 
            # time this is being run here 
            else:
                mercurial = hg.Hg(path=dirname, conf=self.config)
                # then ignore everything within the path
                mercurial.hgignore()
                mercurial.initialize()
                mercurial.hg_add(single=abspath)
                mercurial.commit()
                mercurial.clone()
                # at the end of everything we put the hgrc method in
                mercurial.hgrc()

            # now insert the whole path into the database to 
            # check for it here. DB can figure out if
            # it is a duplicate so no double checking
            # before inserting
            db = Worker()
            db.insert(path=abspath, type='single')

        else:
            self.msg("You have provided a wrong or non-existent path\
to a file", std="err")


    def rebuild(self, server=None, hostname=None, dryrun=False, 
            directories=False, source_path=None):
        """
        server  = user@server
        host    = host to rebuild from (must exist in Master Pacha Server) 
        hostname    = Host to be rebuilt 
        """

        if not directories:
            print "SSH Connection: %-15s" % server
            print "Host to rebuild: %-15s" % hostname
            
            try:
                confirm = raw_input("Hit Enter to confirm or Ctrl-C to cancel")
                run = rebuild.Rebuild(server=server,
                        hostname=hostname, source=source_path)
                run.retrieve_files()
                run.replace_manager()

            except KeyboardInterrupt:
                print "\nExiting nicely from Pacha"
                sys.exit(0)

        if directories:
            try:
                run = rebuild.Rebuild(server=server,
                        source=source_path)
                run.show_directories()
            except Exception, error:
                self.msg(str(error), std="err")

    def parseArgs(self, argv):
        parser = OptionParser(description="""
A systems configuration management engine
    """
        ,version='0.2.4')

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

        # Daemon Group
        daemon_group = OptionGroup(parser, "Daemon Options", "Pacha is able to\
    run in the background, these options will help you manage the daemon")

        daemon_group.add_option('--daemon-start', action='store_true',
                help="Starts the Pacha daemon")

        daemon_group.add_option('--daemon-stop', action='store_true',
                help="Stops the Pacha daemon")

        daemon_group.add_option('--daemon-status', action='store_true',
                help="Checks the status of the Pacha daemon")

        daemon_group.add_option('--daemon-foreground', action='store_true',
                help="Checks the status of the Pacha daemon")

        parser.add_option_group(daemon_group)

        # Rebuilding Group
        group = OptionGroup(parser, "Rebuilding Options", "When rebuilding\
     a host, you will need to pass a few required options to Pacha so it can\
     connect to a remote host via SSH and copy the needed files.")

        group.add_option('--rebuild',
                help="""Receives user and host as arguments [user@host]""")

        group.add_option('--host',
                help="""The host to rebuild from""")


        group.add_option('--source-path',
                help="""Specify the absolute path where Pacha should retrieve\
 file from""")

        group.add_option('--port',
                help="""Overrides default port 22 for SSH""")

        group.add_option('--destination-path',
                help="""Overrides the default destination of the files to a
 different absolute path""")

        group.add_option('--directory',
                help="""Specifies a single directory to retrieve from a remote
 host instance of a Pacha server""")

        group.add_option('--show-directories', action="store_true",
                help="""Shows the available directories to retrieve from a
 given host.""")

        group.add_option('--dryrun', action="store_true",
                help="""Doesn't *actually* do anything, just prints the 
commands as they would happen""")

        parser.add_option_group(group)

        options, arguments = parser.parse_args(argv)

        if options.add_config:
            self.add_config(options.add_config)

        if options.config_values:
            self.config_values()

        if options.remove_config:
            db = Worker()
            db.remove_config()
            self.msg("Configuration file(s) removed")
            sys.exit(0)

        # important: only config options are allowed before 
        # actually checking for valid conf files stored 
        self.config = self.check_config()       

        # Cleanest way to show the help menu if no options are given
        if len(argv) == 1:
            parser.print_help()
  
        # set logging 
        self.set_logging()

        # Deamon Stuff
        if options.daemon_start:
            daemon.start(self.config)

        if options.daemon_stop:
            daemon.stop()

        if options.daemon_foreground:
            daemon.start(config=self.config, foreground=True)

        if options.daemon_status:
            daemon.status()

        if options.add_host:
            self.add_host(options.add_host)

        if options.watch:
            # a hack to have ambiguous optparse behavior 
            if len(sys.argv) is 2: #no path
                path = os.getcwd()
            if len(sys.argv) >=3: #with path
                path = sys.argv[2]
            self.watch(path)

        if options.watch_single:
            self.watch_single(options.watch_single)

        # Rebuilding Stuff
        if options.rebuild and options.host and options.source_path:
            if options.dryrun:
                self.rebuild(server = options.rebuild, 
                        hostname = options.host,
                        source_path = options.source_path)
            else:
                self.rebuild(server = options.rebuild, 
                        hostname = options.host,
                        source_path = options.source_path)

        if options.rebuild and options.source_path and options.show_directories:
            self.rebuild(server = options.rebuild, 
                    directories = True,
                    source_path = options.source_path)
            
    

main = PachaCommands

def main_():
    main()

