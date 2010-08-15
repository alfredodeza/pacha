"""Plugs into Mercurial and matches Pacha's need to commit, push, clone and
other commands. """

from subprocess import call, PIPE
from getpass import getuser
import os
import sys
from time import strftime
from mercurial import commands, ui, hg

from pacha import log
from pacha.config_options import config_defaults
from pacha.host import hostname


class Hg(object):
    """Does local commits and pushes to a central Pacha Master location"""

    def __init__(self,
            port = 22,
            host = None,
            user = None,
            path = None,
            conf = config_defaults(),
            test = False
            ):
        self.port = port
        self.host = host
        self.user = user
        
        if os.path.exists(path):
            log.hg.debug('verified path exists: %s' % path)
            self.path = os.path.normpath(path)
            self.dir = os.path.basename(path)
            self.hg_dir = self.path+'/.hg'
            os.chdir(self.path)
        else:
            log.hg.error('%s does not exist' % path)

        # read the config file once and make sure is edited:
        self.conf = conf
        print self.conf
#        self.parse = confparser.Parse(self.conf)
#        self.parse.options()
        try:
            self.dest_path = '/%s/%s/%s' % (self.conf['hosts_path'],
                    hostname(), self.dir)
        except AttributeError, error:
            log.hg.error('error trying to use config options: %s' % error)
            sys.stderr.write('error trying to use config options: %s' % error)
            sys.exit(1)
        if not test:
            if hg_user() is False:
                print """
Pacha searched for a Mercurial username in the $HOME directory
and /etc/mercurial/hgrc but could not find one.
Mercurial needs a username provided:
But no username was supplied (see "hg help config")
      [ui]
      username = Firstname Lastname <firstname.lastname@example.net>
      verbose = True"""
                log.hg.error(line='No hgrc found with username')
                sys.exit(1)
          #  else:
#
#                try:
#                    self.par.user
#                    self.parse.host
#                except AttributeError, error:
#                    log.hg.error('config file not edited - aborting')
#                    sys.stderr.write('config file not edited! or missing params- aborting\n')
#                    sys.exit(1)
        # testing functionality:
        #if test:
        #    self.parse.user = user
        #    self.parse.path = '/tmp/remote_pacha'
        #    self.parse.host = host

    def commit(self):
        """hg commit action, adding a message with the correct timestamp
        and information from pacha."""
        timestamp = strftime('%b %d %H:%M:%S')
        message = "pacha auto-commit: %s" % timestamp
        repo = hg.repository(ui.ui(), self.path)
        commands.commit(ui.ui(), repo=repo, message=message,
                logfile=None, addremove=None, user=None, date=None)
        log.hg.debug('doing commit at %s' % self.path)

    def hg_add(self, single=None):
        """Adds all files to Mercurial when the --watch options is passed
        This only happens one time. All consequent files are not auto added
        to the watch list."""
        repo = hg.repository(ui.ui(), self.path)
        if single is None:
            commands.add(ui.ui(), repo=repo)
            log.hg.debug('added files to repo %s' % self.path)

        else:
            commands.add(ui.ui(), repo, single) 
            log.hg.debug('added files to repo %s' % self.path)

    def push(self):
        """Pushes the repository to the centralized Pacha Master server
        The Mercurial API is broken here, it does not recognize 'default'
        or 'default-push' in .hg/hgrc so we need to call it via 
        subprocess.call"""
        command = "hg push"
        call(command, shell=True, stdout=PIPE, stderr=PIPE)
        log.hg.debug('push %s to central pacha' % self.path)

    def hgrc(self):
        """An option to write the default path in hgrc for pushing
        via hg"""
        if self.validate():
            machine = hostname()
            try:
                hgrc = open(self.path+'/.hg/hgrc', 'w')
                hgrc.write('[paths]\n')
                ssh_line = "default = ssh://%s@%s%s" % (self.conf['ssh_user'],
                        self.conf['host'], self.dest_path)
                hgrc.write(ssh_line)
                hgrc.close()
                log.hg.debug("wrote hgrc in %s" % self.path)
                log.hg.debug("default is %s" % ssh_line)

            except Exception, error:
                log.hg.error(error)
                return False

        else:
            self.initialize()
            self.hg_add()
            self.commit()
            self.hgrc()

    def clone(self):
        """Clones a given repository to the remote Pacha server
        needs to be ouralled when --watch is passed, runs just one time
        """
        source = self.path
        dest = 'ssh://%s@%s%s' % (self.conf['ssh_user'], 
                self.conf['host'],
            self.dest_path)
        log.hg.debug('destination command for clone: %s' % dest)
        try:
            commands.clone(ui.ui(), source, dest, pull=False, uncompressed=False, rev=False,
                 noupdate=False)
            log.hg.debug('cloning %s' % dest )
        except Exception, error:
            log.hg.error('could not clone repo: %s' % error)
            print "Could not clone this repository: %s" % error
            print """Have you added this host in the Pacha server?"""
        # TODO: need to add trusted USERS in the global .hgrc 
        
    def validate(self):
        """Validates a working HG path"""
        log.hg.debug("validating repository at %s" % self.path)
        if os.path.exists(self.hg_dir):
            log.hg.debug("hg repository found at %s" % self.path)
            return True
        else:
            log.hg.debug("hg repository not found at %s" % self.path)
            return False

    def initialize(self):
        """Creates a mercurial repository"""
        commands.init(ui.ui(), dest=self.path)
        log.hg.debug('created hg repo at %s' % self.path)

    def hgignore(self):
        """Writes an hgignore to ignore all files"""
        ignore = open(self.path+'/.hgignore', 'w')
        ignore.write("syntax: glob\n*\n")
        ignore.close

def update(hosts_path = '/opt/pacha/hosts'):
    """Updates a mercurial repository pluging in directly into Mercurial
    This update() function will be used as a trial to later plug
    all of Pacha into Mercurial, instead of doing subprocess calls"""
    
    for dirs in os.listdir(hosts_path):
        sub_dir = os.path.join(hosts_path, dirs)
        if os.path.isdir(sub_dir):
            for dir in os.listdir(os.path.join(hosts_path, dirs)):
                directory = os.path.join(sub_dir, dir)
                if os.path.isdir(directory):
                    u = ui.ui()
                    repo = hg.repository(u, directory)
                    repo.ui.pushbuffer()
                    commands.update(ui.ui(), repo)
                    log.hg.debug('updating host %s directory: %s' % (dirs, directory))
                    log.hg.debug(repo.ui.popbuffer().split('\n')[0])
                else:
                    log.hg.error('%s is not a directory' % directory)

def hg_user():
    """In charge of checking if you have a username set in either 
    $HOME/.hgrc or in /etc/mercurial/hgrc"""
    if 'root' == getuser():
        user_hgrc = '/root/.hgrc'
    else:
        user_hgrc = '/home/%s/.hgrc' % getuser()
    global_hgrc = '/etc/mercurial/hgrc'
    result = False
    if os.path.isfile(global_hgrc):
        for line in open(global_hgrc):
            if 'username' in line:
                result = True
    if result is False: # nothing found in global so look into home
        if os.path.isfile(user_hgrc):
            for line in open(user_hgrc):
                if 'username' in line:
                    result =True
    return result


