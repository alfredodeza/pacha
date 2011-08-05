import logging
import os
import sys
from subprocess     import call, PIPE
from getpass        import getuser
from time           import strftime
from mercurial      import commands, ui, hg
from ConfigParser   import ConfigParser, NoOptionError
from guachi         import ConfigMapper

from pacha.host     import hostname
from pacha.util     import run_command, YELLOW, ENDS, get_db_file

hg_log = logging.getLogger('pacha.hg')

HGRC_ERROR =  YELLOW+"""
Pacha searched for a Mercurial username in the $HOME directory
and /etc/mercurial/hgrc but could not find one.
Mercurial needs a username provided:
But no username was supplied (see "hg help config")
      [ui]
      username = Firstname Lastname <firstname.lastname@example.net>
      verbose = True
"""+ENDS

DB_FILE = get_db_file()

class Hg(object):
    """Does local commits and pushes to a central Pacha Master location"""

    def __init__(self,
            port = 22,
            host = None,
            user = None,
            path = None,
            log = True,
            conf = None,
            test = False
            ):
        self.port = port
        self.host = host
        self.user = user
        self.log = log
        if conf == None:
            self.conf = ConfigMapper(DB_FILE).stored_config()
        else:
            self.conf = conf 
        if os.path.exists(path):
            hg_log.debug('verified path exists: %s' % path)
            self.path = os.path.normpath(path)
            self.dir = os.path.basename(path)
            self.hg_dir = self.path+'/.hg'
            os.chdir(self.path)
        else:
            hg_log.error('%s does not exist' % path)
        try:
            self.dest_path = '/%s/%s/%s' % (self.conf['hosts_path'],
                    hostname(), self.dir)
        except AttributeError, error:
            hg_log.error('error trying to use config options: %s' % error)
            sys.stderr.write('error trying to use config options: %s' % error)
            sys.exit(1)
        if not test:
            if hg_user() is False:
                print HGRC_ERROR 
                hg_log.error('No hgrc found with username')
                sys.exit(1)

    def commit(self):
        """hg commit action, adding a message with the correct timestamp
        and information from pacha."""
        timestamp = strftime('%b %d %H:%M:%S')
        message = "pacha auto-commit: %s" % timestamp
        u = ui.ui()
        u.pushbuffer()
        repo = hg.repository(u, self.path)
        commands.commit(u, repo=repo, message=message,
                logfile=None, addremove=None, user=None, date=None)
        hg_log.debug('doing commit at %s' % self.path)
        hg_log.debug(u.popbuffer())

    def hg_add(self, single=None):
        """Adds all files to Mercurial when the --watch options is passed
        This only happens one time. All consequent files are not auto added
        to the watch list."""
        repo = hg.repository(ui.ui(), self.path)
        if single is None:
            commands.add(ui.ui(), repo=repo)
            hg_log.debug('added files to repo %s' % self.path)

        else:
            commands.add(ui.ui(), repo, single) 
            hg_log.debug('added files to repo %s' % self.path)

    def push(self):
        """Pushes the repository to the centralized Pacha Master server
        The Mercurial API is broken here, it does not recognize 'default'
        or 'default-push' in .hg/hgrc so we need to call it via 
        subprocess.call"""
        command = "hg push"
        call(command, shell=True, stdout=PIPE, stderr=PIPE)
        hg_log.debug('push %s to central pacha' % self.path)

    def hgrc(self):
        """An option to write the default path in hgrc for pushing
        via hg"""
        if self.validate():
            machine = hostname()
            try:
                hgrc = open(self.path+'/.hg/hgrc', 'w')
                hgrc.write('[paths]\n')
                ssh_line = "default = ssh://%s@%s:%s%s" % (self.conf['ssh_user'],
                                    self.conf['host'],
                                    self.conf.get('ssh_port', 22),
                                    self.dest_path)
                hgrc.write(ssh_line)
                hgrc.close()
                hg_log.debug("wrote hgrc in %s" % self.path)
                hg_log.debug("default is %s" % ssh_line)

            except Exception, error:
                hg_log.error(error)
                return False

        else:
            self.initialize()
            self.hg_add()
            self.commit()
            self.hgrc()

    def hgrc_user(self):
        """Verifies the hgrc default user against what we expect"""
        user = None
        try:
            hg_log.debug('verifying hgrc username')
            hgrc = open(self.path+'/.hg/hgrc')
            for line in hgrc.readlines():
                if 'default' and 'ssh:' in line:
                    try:
                        user = line.split('@')[0].split('//')[1]
                        hg_log.debug('found username in hgrc: %s' % user)
                    except IndexError:
                        pass # we can use None later 
                else:
                    pass 

        except Exception, error:
            hg_log.error(error)

        if user != self.conf['ssh_user']:
            hg_log.critical('.hgrc ssh user (%s) does not match config user: %s at %s' % (user, 
                self.conf['ssh_user'], 
                self.path))  
            if self.conf['hg_autocorrect'] == u'True':
                self.hgrc() # rewrites the hgrc 
            else:
                hg_log.critical('hg_autocorrect is set to False so not rewriting hgrc')

    def clone(self):
        """Clones a given repository to the remote Pacha server
        needs to be ouralled when --watch is passed, runs just one time
        """
        source = self.path
        dest = 'ssh://%s@%s:%s%s' % (self.conf['ssh_user'],
                self.conf['host'],
                self.conf.get('ssh_port', 22),
                self.dest_path)
        hg_log.debug('destination command for clone: %s' % dest)
        try:
            commands.clone(ui.ui(), source, str(dest), pull=False, uncompressed=False, rev=False,
                 noupdate=False)
            hg_log.debug('cloning %s' % dest )
        except Exception, error:
            hg_log.error('could not clone repo: %s' % error)
            return False
        
    def hgrc_validate(self):
        """Returns False if it can't find an hgrc and returns 
        the full ssh path if found"""
        hg_log.debug("validating hgrc file at %s" % self.path)
        hgrc = "%s/.hg/hgrc" % self.path
        if os.path.exists(hgrc):
            hg_log.debug("hgrc found at %s" % self.path)
            parser = ConfigParser()
            parser.read(hgrc)
            try:
                default_path = parser.get('paths', 'default')
                return default_path
            except NoOptionError:
                return False
        else:
            hg_log.debug("hgrc not found at %s" % self.path)
            return False

    def validate(self):
        """Validates a working HG path"""
        hg_log.debug("validating repository at %s" % self.path)
        if os.path.exists(self.hg_dir):
            hg_log.debug("hg repository found at %s" % self.path)
            return True
        else:
            hg_log.debug("hg repository not found at %s" % self.path)
            return False

    def initialize(self):
        """Creates a mercurial repository"""
        commands.init(ui.ui(), dest=self.path)
        hg_log.debug('created hg repo at %s' % self.path)

    def hgignore(self):
        """Writes an hgignore to ignore all files"""
        ignore = open(self.path+'/.hgignore', 'w')
        ignore.write("syntax: glob\n*\n")
        ignore.close


    def revision(self):
        """Gets the revision ID from the path"""
        changeset = run_command(std="stdout", cmd="hg head")[0]
        return changeset[-13:].split('\n')


def update(hosts_path, rebuild=False):
    for dirs in os.listdir(hosts_path):
        sub_dir = os.path.join(hosts_path, dirs)
        if os.path.isdir(sub_dir):
            if rebuild:
                hg_push_update(os.path.join(hosts_path, dirs))
            else:
                for dir in os.listdir(os.path.join(hosts_path, dirs)):
                    directory = os.path.join(sub_dir, dir)
                    try:
                        if os.path.isdir(directory):
                            hg_push_update(directory)
                        else:
                            hg_log.error('%s is not a directory' % directory)
                    except OSError, error:
                        # avoid permission denied
                        hg_log.error("couldn't update %s. Error: %s" % (sub_dir, error)) 

def hg_push_update(repo):
    u = ui.ui()
    repo = hg.repository(u, repo)
    repo.ui.pushbuffer()
    commands.update(ui.ui(), repo)
    hg_log.debug("updating repo: %s" % repo)
    hg_log.debug(repo.ui.popbuffer().split('\n')[0])


def hg_user():
    """In charge of checking if you have a username set in either 
    $HOME/.hgrc or in /etc/mercurial/hgrc"""
    if 'root' == getuser():
        user_hgrc = '/root/.hgrc'
    else:
        home_dir = os.environ.get('HOME')
        user_hgrc = home_dir+'/.hgrc'
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


