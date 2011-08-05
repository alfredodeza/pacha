import logging
import os
import shutil
import sys
from time           import strftime
from guachi         import ConfigMapper

from pacha.host     import hostname
from pacha.util     import run_command, get_db_file

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
            test = False,
            single = False
            ):
        self.port = port
        self.host = host
        self.user = user
        self.log = log
        self.single = single
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

    def sync(self, source=None):
        """rsyncs the given path to the remote pacha instance"""
        if not source:
            source = self.path
        dest = '%s@%s:%s' % (self.conf['ssh_user'], self.conf['host'],
            self.dest_path)
        command = "rsync -av %s %s" % (source, dest)
        snc_log.debug('destination command for clone: %s' % command)
        run_command(std="stdout", cmd=command)

    def single_file(self):
        """Single files get in sync differently from directories
        we need to create a directory and move that single file and then 
        perform a synchronization"""
        tmp_path = '/tmp/pacha_%s/%s' % (strftime('%H%M%s'),
                os.path.basename(os.path.dirname(self.path)))
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
        os.makedirs(tmp_path)
        shutil.copy(self.path, tmp_path)
        
        # Now we call sync with our new path: 
        self.sync(source = tmp_path)
