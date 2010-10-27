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

snc_log = logging.getLogger('pacha.rsync')

DB_FILE = get_db_file()

class Sync(object):
    """Synchronize the files in our repo to a remote Pacha instance"""

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
            snc_log.debug('verified path exists: %s' % path)
            self.path = os.path.normpath(path)
            self.dir = os.path.basename(path)
        else:
            snc_log.error('%s does not exist' % path)
        try:
            self.dest_path = '%s/%s' % (self.conf['hosts_path'], hostname())
        except AttributeError, error:
            snc_log.error('error trying to use config options: %s' % error)
            sys.stderr.write('error trying to use config options: %s' % error)
            sys.exit(1)

    def sync(self):
        """rsyncs the given path to the remote pacha instance"""
        source = self.path
        dest = '%s@%s:%s' % (self.conf['ssh_user'], self.conf['host'],
            self.dest_path)
        command = "rsync -av %s %s" % (source, dest)
        snc_log.debug('destination command for clone: %s' % command)
        run_command(std="stdout", cmd=command)


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
        snc_log.debug('doing commit at %s' % self.path)
        snc_log.debug(u.popbuffer())

    def hg_add(self, single=None):
        """Adds all files to Mercurial when the --watch options is passed
        This only happens one time. All consequent files are not auto added
        to the watch list."""
        repo = hg.repository(ui.ui(), self.path)
        if single is None:
            commands.add(ui.ui(), repo=repo)
            snc_log.debug('added files to repo %s' % self.path)

        else:
            commands.add(ui.ui(), repo, single) 
            snc_log.debug('added files to repo %s' % self.path)

    def push(self):
        """Pushes the repository to the centralized Pacha Master server
        The Mercurial API is broken here, it does not recognize 'default'
        or 'default-push' in .hg/hgrc so we need to call it via 
        subprocess.call"""
        command = "hg push"
        call(command, shell=True, stdout=PIPE, stderr=PIPE)
        snc_log.debug('push %s to central pacha' % self.path)

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
                snc_log.debug("wrote hgrc in %s" % self.path)
                snc_log.debug("default is %s" % ssh_line)

            except Exception, error:
                snc_log.error(error)
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
            snc_log.debug('verifying hgrc username')
            hgrc = open(self.path+'/.hg/hgrc')
            for line in hgrc.readlines():
                if 'default' and 'ssh:' in line:
                    try:
                        user = line.split('@')[0].split('//')[1]
                        snc_log.debug('found username in hgrc: %s' % user)
                    except IndexError:
                        pass # we can use None later 
                else:
                    pass 

        except Exception, error:
            snc_log.error(error)

        if user != self.conf['ssh_user']:
            snc_log.critical('.hgrc ssh user (%s) does not match config user: %s at %s' % (user, 
                self.conf['ssh_user'], 
                self.path))  
            if self.conf['hg_autocorrect'] == u'True':
                self.hgrc() # rewrites the hgrc 
            else:
                snc_log.critical('hg_autocorrect is set to False so not rewriting hgrc')

