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

from optparse       import OptionParser, OptionGroup
from guachi         import ConfigMapper
from pacha.config   import set_mappings
from pacha          import daemon, rebuild, permissions
from pacha.database import Worker
from pacha.host     import Host
from pacha.util     import WARNING, CONFIG_GONE, get_db_file, get_db_dir
from pacha.sync     import Sync

DB_FILE = get_db_file()
DB_DIR = get_db_dir()
 
class PachaCommands(object):
    """A lot of complicated options can happen with Pacha, so 
    it is easier if everything lives under a class rather than
    the widely used main()"""

    def __init__(self, 
            argv=None, 
            test=False, 
            parse=True, 
            db=ConfigMapper(DB_FILE),
            db_file=DB_FILE):
        self.db = db 
        self.db_file = db_file
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
        """if any commands are run, check for a MASTER config file Location"""
        conf = self.db.stored_config()
        try:
            config_file = conf['path']
        except KeyError:
            return self.msg(msg=WARNING, std="err")
        if config_file == '':
            return self.msg(msg=WARNING, std="err")
        elif os.path.isfile(config_file):
            self.db.set_config(config_file)
            return self.db.stored_config()
        elif not os.path.isfile(config_file) and len(conf.items()) > 3: # Meaning already parsed
            print CONFIG_GONE 
            return self.db.stored_config()
        elif len(conf.items()) <= 1: # config might not be set 
            self.db.set_config(config_file)
            return self.db.stored_config()
        else:
            return self.db.stored_config()


    def add_config(self, path):
        conf = self.db.stored_config()
        abspath = os.path.abspath(path)
        conf['path'] = abspath
        set_mappings(self.db_file)
        self.msg("Configuration file added: %s" % abspath)


    def config_values(self):
        conf = self.db.stored_config()
        try:
            config_file = conf['path']
            print "\nConfiguration file: %s\n" % config_file
            for i in conf.items():
                print "%-15s= %-4s" % (i[0], i[1])
            print ''
        except Exception, error:
            # sometimes we can't catch the error
            print "Could not complete command %s" % error

    def set_logging(self, verbose=False):
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

        if not enabled or log_path is None:
            logging.disable(logging.CRITICAL)

        if not verbose:
            logging.disable(logging.CRITICAL)

    def add_host(self, host):
        try:
            new = Host(host=host, 
                    host_path=self.config['hosts_path'])
            created = new.create()
            if created:
                print "Added host %s" % host
            else:
                print "Host %s has been already created" % host
        except Exception, error:
            print "Could not complete command: %s" % error 


    def restore_db(self, hostname):
        """
        server  = user@server
        host    = host to rebuild the database from (must exist in Master Pacha Server) 
        hostname    = Host to be rebuilt 
        """
        server = "%s@%s" % (self.config['ssh_user'], self.config['host'])
        port = self.config['ssh_port']
        source = self.config['hosts_path']
 

        print "SSH Connection: %-15s" % server
        print "SSH Port:       %-15s" % port
        print "Host to rebuild DB: %-15s" % hostname
        
        try:
            confirm = raw_input("Hit Enter to confirm or Ctrl-C to cancel")
            run = rebuild.Rebuild(
                    server=server,
                    hostname=hostname, 
                    source=source,
                    directory='db',
                    port=port)
            run.retrieve_files()
            run.upgrade_database()

        except KeyboardInterrupt:
            print "\nExiting nicely from Pacha"
            sys.exit(0)

    def watch(self, path):                
        """
        3 things need to happen:
        *  track whatever we initially were asked for
        *  check if this is the first time we are run (db not tracked)
        *  track the db if it is not tracked or push it with the new dir
        """
        if os.path.exists(path):
            db = Worker(DB_FILE)
            sync = Sync(path=path)
            sync.sync()
            # add the path to repos table in database
            db.insert(path=path, type='dir')
            # now make sure we record permissions metadata
            meta = permissions.Tracker(path=path)
            meta.walker()

            # we always make sure the DB gets in sync:
            sync_db = Sync(path=DB_DIR)
            sync_db.sync()
        else:
            self.msg("You have provided a wrong or non-existent path\
to a file", std="err")

    def watch_single(self, s_file):
        if os.path.isfile(s_file):
            sync = Sync(path=s_file)
            sync.single_file()
            
            # permissions metadata
            meta = permissions.Tracker(path=s_file)
            meta.single_file()

            db = Worker(DB_FILE)
            db.insert(path=s_file, type='single')

            # track db
            sync_db = Sync(path=DB_DIR)
            sync_db.sync()

        else:
            self.msg("You have provided a wrong or non-existent path\
to a file", std="err")


    def rebuild(self, hostname, directory=None):
        """
        server  = user@server
        host    = host to rebuild from (must exist in Master Pacha Server) 
        hostname    = Host to be rebuilt 
        """
        server = "%s@%s" % (self.config['ssh_user'], self.config['host'])
        port = self.config['ssh_port']
        source = self.config['hosts_path']
 

        print "SSH Connection: %-15s" % server
        print "SSH Port:       %-15s" % port
        print "Host to rebuild: %-15s" % hostname
        
        try:
            confirm = raw_input("Hit Enter to confirm or Ctrl-C to cancel")
            run = rebuild.Rebuild(
                    server=server,
                    hostname=hostname, 
                    source=source,
                    directory=directory,
                    port=port)
            run.retrieve_files()
            run.replace_manager()

        except KeyboardInterrupt:
            print "\nExiting nicely from Pacha"
            sys.exit(0)


    def parseArgs(self, argv):
        parser = OptionParser(description="""
A systems configuration management engine
    """
        ,version='0.2.4')

        parser.add_option('--config-values', action="store_true",
                help="""Displays the current configuration values used""")

        parser.add_option('--add-config',
                help="""Adds a path to a configuration file""")

        parser.add_option('--add-host',
                help="""Creates structure for saving host configs\
 only meant for Pacha server""")

        parser.add_option('--watch', action="store_true",
               help="Provide a path for Pacha to watch and keep track of")  

        parser.add_option('--watch-single',
               help="Provide a single file for Pacha to watch in a given\
 directory. Everything else in the directory will be ignored.\
 Also used to add more individual files to track within the same\
 directory (e.g. like tracking .vimrc in $HOME)") 

        parser.add_option('--verbose', '-v', action='store_true',
                help="Enables verbosity in terminal")

        parser.add_option('--restore-db',
                help="Restores Pacha's internal DB from a previous version.\
You need to provide the hostname of the server where Pacha was running.")

        # Daemon Group
        daemon_group = OptionGroup(parser, "Daemon Options", "Pacha is able to\
    run in the background, these options will help you manage the daemon")

        daemon_group.add_option('--daemon-start', action='store_true',
                help="Starts the Pacha daemon")

        daemon_group.add_option('--daemon-stop', action='store_true',
                help="Stops the Pacha daemon")

        daemon_group.add_option('--daemon-status', action='store_true',
                help="Checks the status of the Pacha daemon")

        daemon_group.add_option('--daemon-run-once', action='store_true',
                help="Runs all daemon tasks once and then exits.")

        daemon_group.add_option('--daemon-foreground', action='store_true',
                help="Runs on the foreground until it receives a Ctrl-C")

        parser.add_option_group(daemon_group)

        # Rebuilding Group
        group = OptionGroup(parser, "Rebuilding Options", "When rebuilding\
 a host, you will need to pass a few required options to Pacha so it can\
 connect to a remote host via SSH and copy the needed files.")

        group.add_option('--rebuild',
                help="""Pass the hostname of the host you want to rebuild.""")

        group.add_option('--directory',
                help="""Specifies a single directory to retrieve from a remote
 host instance of a Pacha server""")

        parser.add_option_group(group)

        options, arguments = parser.parse_args(argv)

        if options.add_config:
            self.add_config(options.add_config)

        # important: only config options are allowed before 
        # actually checking for valid conf files stored 
        self.config = self.check_config()       

        if options.config_values:
            self.config_values()

        # Cleanest way to show the help menu if no options are given
        if len(argv) == 1:
            parser.print_help()
  

        # Deamon Stuff
        if options.daemon_start:
            self.set_logging(verbose=True)
            daemon.start(self.config)

        if options.daemon_stop:
            daemon.stop()

        if options.daemon_run_once:
            self.set_logging(verbose=True)
            daemon.start(foreground=True, run_once=True)

        if options.daemon_foreground:
            self.set_logging(verbose=True)
            daemon.start(config=self.config, foreground=True)

        if options.verbose:
            self.set_logging(verbose=True)

        if not options.verbose:
            self.set_logging()

        if options.daemon_status:
            daemon.status()

        if options.add_host:
            self.add_host(options.add_host)

        # Upgrade
        if options.restore_db:
            self.restore_db(options.restore_db)

        if options.watch:
            # a hack to have ambiguous optparse behavior 
            if len(argv) is 2: #no path
                path = os.getcwd()
            if len(argv) >=3: #with path
                path = argv[2]
            self.watch(os.path.abspath(path))

        if options.watch_single:
            abspath = os.path.abspath(options.watch_single) 
            self.watch_single(abspath)

        # Rebuilding Stuff
        if options.rebuild:
            directory = None
            if options.directory:
                directory = options.directory
            self.rebuild(hostname=options.rebuild, directory=directory)

main = PachaCommands

def main_():
    main()

