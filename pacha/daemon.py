import os
import sys
import time
from subprocess import Popen, PIPE
import supay
from pacha import hg, database
import logging

daemon_log = logging.getLogger('pacha.daemon')

class Watcher(object):
    """Handles all the Reports to display"""
 
    def __init__(self,
                 path=None):
        self.dir_path = os.path.normpath(path)
        self.path = os.path.normpath(path) 
        if not os.path.isdir(path):
            self.dir_path = os.path.dirname(path)

    def report(self):
        """Report if a file changed and the change has not been commited"""
        daemon_log.debug('watching for changes in %s' % self.path)
        run = Runners(location=self.dir_path)
        if run.modified() is True:
            mercurial = hg.Hg(path=self.dir_path)
            mercurial.commit()
            mercurial.push()

    def revision_compare(self, path, rev):
        """Conect to the database for revision comparison
        and insert a revision hash from Mercurial if it 
        does not exist"""
    
        run = Runners(location=self.dir_path)
        if rev == None:  #a path without a revision so insert one
            daemon_log.debug('No revision recorded in DB - so adding it')
            revision = run.hg_revision()[0]
            db = database.Worker()
            db.update_rev(self.path, revision)
            daemon_log.debug('added revision %s for path %s' % (revision, self.path))
        else: # we have a hash there so:
            revision = run.hg_revision()[0]
            if rev != revision:
                daemon_log.debug('found a new revision: %s at %s' % (rev,self.path))
                mercurial = hg.Hg(path=self.path)
                mercurial.push()
                db = database.Worker()
                db.update_rev(self.path, revision) 

class Runners(object):
    """Handles everything related to Mercurial calls"""

    # TODO This should belong in the HG Class, not here in the Daemon

    def __init__(self, location=None):
        self.location = location
        os.chdir(location) # change directory (HG bug)

    def hg_revision(self):
        """Gets the revision ID from the path"""
        changeset = run_command(std="stdout", cmd="hg head")[0]
        return changeset[-13:].split('\n')

    def modified(self):
        """Checks if a file has been modified and not commited"""
        out = run_command(std="stdout", cmd="hg st")
        for line in out:
            file_name = line[2:].split('\n')[0] # get a nice file name
            if line.startswith('M'):
                daemon_log.debug('found modified file: %s' % file_name)
                return True
            else:
                return False
                daemon_log.debug('no changes with: %s' % file_name)

def run_command(std, cmd):
    """Runs a command via Popen"""
    if std == "stderr":
        run = Popen(cmd, shell=True, stderr=PIPE)
        out = run.stderr.readlines()
    if std == "stdout":
        run = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out = run.stdout.readlines()
    return out


def start(config, foreground=False):
    if not foreground:
        daemon = supay.Daemon(name='pacha', log=False, pid_dir=os.path.dirname(__file__))
        daemon.start()
    daemon_log.debug('Daemon started')

    while True:
        try:
            daemon_log.debug('Starting while True')
            db = database.Worker()
            repos = []
            for i in db.get_repos():
                repos.append(i)
            db.closedb()
            daemon_log.debug('reading repos from database')
            try:
                freq = int(config['frequency'])
                if freq < 10:
                    freq = 60
            except ValueError: # if we do not get a number
                freq = 60
            except AttributeError:
                freq = 60
            try:
                master = config['master']
                if master == 'True':
                    hg.update(config['hosts_path'])
                    daemon_log.debug('machine set to master')
            except AttributeError, error:
                # it is ok if this setting is not ON
                # but annoying if you see this INFO all over
                # your log files, so nothing to see here
                pass
                daemon_log.debug('looping over repos in db')
            for repo in repos:
                # need to get an abspath from 'repo' and then pass it on
                # else the daemon will error out
                repo_path = repo[1]
                if os.path.exists(repo_path): # catches a path no longer there...
                    watch = Watcher(path=repo_path)
                    watch.report()
                    watch.revision_compare(path=repo_path, rev=repo[4])
                else:
                    pass
                    daemon_log.warning('path %s does not exist' % repo_path)
            daemon_log.debug('daemon going to sleep')
            time.sleep(freq)

        except KeyboardInterrupt:
            print "Exiting from foreground daemon"
            sys.exit(0)

        except Exception, error:
            daemon_log.error('Fatal exception - daemon killed')
            daemon_log.error(error)
            sys.exit(1)

def stop():
    daemon = supay.Daemon(name='pacha', log=False, pid_dir=os.path.dirname(__file__))
    daemon.stop()
    daemon_log.debug("daemon stopped")

