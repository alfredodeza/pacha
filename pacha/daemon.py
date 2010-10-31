import os
import sys
import time
import supay
import logging

from guachi             import ConfigMapper
from pacha.database     import Worker
from pacha.util         import get_db_file, get_pid_dir
from pacha.sync         import Sync

daemon_log = logging.getLogger('pacha.daemon')
PID_DIR = get_pid_dir()
DB_FILE = get_db_file()


class SingleRepository(object):
    """ Compares the modified time of a file or directory via lstat 
    and the timestamp stored in the database """
 

    def __init__(self, path):
        self.dir_path = os.path.normpath(path)
        self.path = os.path.normpath(path) 
        if not os.path.isdir(path):
            self.dir_path = os.path.dirname(path)
        self.db = Worker(DB_FILE)


    def is_modified(self):
        """checks whether the directory or the file is modified """
        daemon_log.debug('looking for modified files in %s' % self.path)
        repo = self.db.get_repo(self.path)
        saved_tstamp = int([i[4] for i in repo][0])
        stat = os.lstat(self.path)
        modified = int(stat.st_mtime)
        if saved_tstamp < modified:
            return modified 
        return False


    def synchronize(self):
        timestamp = self.is_modified()
        if timestamp:
            daemon_log.info('found modified files in %s' % self.path)
            sync = Sync(path=self.path)
            sync.sync()
            # Since we got a modified file, update the DB: 
            self.store_timestamp(timestamp) 


    def store_timestamp(self, new_tstamp):
        """If we find a newly modified repository the database needs to be
        updated"""
        daemon_log.debug('adding new modified timestamp to path %s' % self.path)
        self.db.update_timestamp(self.path, new_tstamp) 



def frecuency(seconds):
    """Deal with frecuency and thresholds"""
    try:
        freq = int(seconds)
        if freq < 10:
            freq = 60
    except ValueError: # if we do not get a number
        freq = 60
    except Exception:  # we catch anything always
        freq = 60
    return freq 



def start(config=None, foreground=False, run_once=False):

    if config == None:
        config=ConfigMapper(get_db_file()).stored_config()

    if not foreground:
        log_path = config['log_path']
        log_enable = config['log_enable']
        if not log_enable or log_path is None:
            daemon = supay.Daemon(name='pacha', log=False, pid_dir=PID_DIR)
        if log_enable and log_enable:
            daemon = supay.Daemon(name='pacha', catch_all_log=log_path, pid_dir=PID_DIR)

        daemon.start()
        daemon_log.debug('Daemon started')

    while True:
        try:
            db = Worker()
            daemon_log.debug('reading repos from database')
            repos = [i for i in db.get_repos()]
            db.closedb()
            freq = frecuency(config['frequency'])
            #### *** DVCS Support HERE *** ###
#            try:
#                master = config['master']
#                if master == 'True':
#                # we need to inject DVCS support HERE
#                    
#                    hg.update(config['hosts_path'])
#                    daemon_log.debug('machine set to master')
#            except AttributeError, error:
#                # it is ok if this setting is not ON
#                # but annoying if you see this INFO all over
#                # your log files, so nothing to see here
#                pass
            for repo in repos:
                daemon_log.debug('looping over repos in db')
                repo_path = repo[1]
                if os.path.exists(repo_path): # catches a path no longer there
                    stat_check = SingleRepository(repo_path)
                    stat_check.synchronize()
                else:
                    pass
                    daemon_log.warning('path %s does not exist' % repo_path)
            if run_once:
                raise KeyboardInterrupt
            daemon_log.debug('daemon going to sleep for %s seconds' % freq)
            time.sleep(freq)

        except KeyboardInterrupt:
            print "Exiting from foreground daemon"
            sys.exit(0)

        except Exception, error:
            daemon_log.error('Fatal exception - daemon killed')
            daemon_log.error(error)
            sys.exit(1)


def stop():
    daemon = supay.Daemon(name='pacha', log=False, pid_dir=PID_DIR)
    daemon.stop()


def status():
    daemon = supay.Daemon(name='pacha', log=False, pid_dir=PID_DIR)
    daemon.status()

