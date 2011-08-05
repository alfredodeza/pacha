"""rebuilder that checks for permissions and locations in the datbase, 
moves files from one places to the other and installs packages if needed"""
import mercurial
import logging
import os
import sys
import pwd
import grp
import shutil

from subprocess     import call
from time           import strftime

from pacha          import database
from pacha.hg       import update
from pacha.util     import get_db_dir

rebuild_log = logging.getLogger('pacha.rebuild')
DB_DIR = get_db_dir()

class Rebuild(object):
    """Does all the rebuilding work when a host needs to be reconstructed 
    with Pacha. Minimal configurations come from pacha.conf and more complex
    executions come from the sh folder.
    All executions should be done with Super User powers.
    """

    def __init__(self,
            server = None,
            port = 22,
            destination = '/tmp',
            source = None,
            hostname = None,
            directory = None
            ):
        self.server = server
        self.port = int(port)
        self.destination = destination
        self.source = source
        self.directory = directory
        self.hostname = hostname

    def retrieve_files(self):
        """scp all the files we need to /tmp"""
        os.chdir('/') # avoids being in a dir that will no longer exist
        if os.path.exists('/tmp/%s' % self.hostname):
            shutil.move('/tmp/%s' % self.hostname, '/tmp/%s.%s' % (self.hostname, strftime('%H%M%s')))

        if not self.directory:
            rebuild_log.debug("Getting all files (not single dir)")
            command = "scp -r -P %d %s:%s/%s %s" % (self.port, self.server,
                    self.source, self.hostname, self.destination)
            rebuild_log.debug(command)
        else:
            if self.destination == '/tmp':
                os.makedirs('/tmp/%s' % (self.hostname))
                self.destination = '/tmp/%s/%s' % (self.hostname, self.directory) 
            rebuild_log.debug("Getting a single dir")
            command = "scp -r -P %d %s:%s/%s/%s %s" % (self.port, self.server,
                    self.source, self.hostname, self.directory, self.destination)
            rebuild_log.debug(command)
        call(command, shell=True)
        # if for some reason the above failed let me know:
        host_copy = '/tmp/%s' % self.hostname
        if os.path.isdir(host_copy):
            # update everything making sure we have the latest rev:
            try:
                update(host_copy)
            except mercurial.error.RepoError:
                pass

            # run pre-hooks
            self.pre_hooks()

        else:
            print """
Pacha was not able to retrieve the files from the SSH server provided.
Check your configuration file settings and try again."""
            sys.exit(1)

    def upgrade_database(self):
        db_location = '/tmp/%s/db/pacha.db' % self.hostname
        db_dir_location = os.path.dirname(db_location)
        db_to_replace = DB_DIR 
        if os.path.exists(db_location):
            # move initial db out
            shutil.move(db_to_replace, '/tmp/pacha.db.%s' % strftime('%H%M%s'))
            # get old db in 
            shutil.copytree(db_dir_location, db_to_replace)

    def replace_manager(self):
        """Depending on the database information for each path, you may or 
        may not have specific files you want to override. This manager method 
        dispatches correctly after verifying if you were tracking a single 
        file or a directory"""
        
        db_location = '/tmp/%s/db/pacha.db' % self.hostname
        if os.path.exists(db_location):
            # connect to the DB:
            db = database.Worker(db=db_location)
            for path in db.get_repos():
                for dirname in self.tracked():
                    if path[3] == 'dir': # dir so do default replace
                        rebuild_log.debug("dirname in self.tracked: %s" % dirname)
                        self.default_replace(dirname, path[1])
                    if path[3] == 'single': # a single file tracking
                        rebuild_log.debug('single file in self.tracked: %s' % dirname)
                        self.single_tracking(path[1])
            # run post hooks 
            self.post_hooks()
        else:
            print "Could not find DB at /tmp/%s/db/pacha.db" % self.hostname
            sys.exit(1)

    def single_tracking(self, path):
        """You can have specific files to be rebuilt to avoid replacing
        whole directories."""
        #repos_path = self.repos()
        rebuild_log.debug('single repo path: %s' % path)
        tmp_dir = '/tmp/%s/' % self.hostname
        rebuild_log.debug('tmp_dir: /tmp/%s' % self.hostname)
        # get list of directories in tmp and do a double loop
        #for path in repos_path:
        base = os.path.basename(path) #gets us the file name
        dir_path = os.path.dirname(path)
        # finally a dir name from the path
        directory = os.path.basename(dir_path)
        tmp_subdir = tmp_dir+directory
        rebuild_log.debug(module='rebuild.single_tracking', 
                line= 'base file: %s' % base)
        for filen in os.listdir(tmp_subdir): 
            if filen == base: # we have a winner
                rebuild_log.debug('found path with matching file: %s %s' % (path, 
                    base))
                if os.path.exists(path):
                    # get it out of the way
                    shutil.move(path,'/tmp/%s.%s' % (base, strftime('%H%M%s'))) 
                    rebuild_log.debug('moving %s to /tmp' % path)
                shutil.copyfile(tmp_subdir+'/'+filen, path)
                rebuild_log.debug('moving %s to %s' % (tmp_subdir+'/'+filen, path))
                # get permissions right without walking the tree
                self.chmod(path)
                self.chown(path)

    def default_replace(self, dirname, path):
        """Usually you will replace the configs you were backing up. Here
        the directory gets pushed if not specified in the database"""
        temp_bucket = '/tmp/pacha_bucket'
        if os.path.exists(temp_bucket):
            shutil.rmtree(temp_bucket)
        os.makedirs(temp_bucket)
        rebuild_log.debug('repos path: %s' % path)
        tmp_dir = '/tmp/%s/' % self.hostname
        rebuild_log.debug('tmp_dir: %s' % tmp_dir)
        # get list of directories in tmp and do a double loop
        base = os.path.basename(path)
        rebuild_log.debug('base dir: %s' % base)
        if dirname == base: # we have a winner
            rebuild_log.debug('found path with matching dir: %s %s' % (dirname, 
                base))
            if os.path.exists(path):
                shutil.move(path,'/tmp/pacha_bucket/%s.%s' % (base, 
                    strftime('%H%M%s'))) # get it out of the way
                rebuild_log.debug(
                        'moving %s to /tmp/pacha_bucket/%s.%s' % (
                            path, base, strftime('%H%M%s')))
            try:
                shutil.copytree(tmp_dir+dirname, path)
                rebuild_log.debug('moving %s to %s' % (tmp_dir+dirname, path))
                # get ownership and permissions right walking the tree
                self.walk(path)
                # we also need to set permissions for the directory
                self.chown(path)
                self.chmod(path)

            except OSError, error:
                rebuild_log.error(error)
                pass 

    def walk(self, path):
        """If we are replacing whole directories we need to make sure
        we get the permissions in each file within the tree"""
        for root, dirs, files in os.walk(path):
            for f in files:
                absolute = os.path.join(root, f)
                self.chown(absolute)
                self.chmod(absolute)

    def tracked(self):
        """There needs to be a comparison between the copied files and the
        files that are in the database.
        """
        list_files = os.listdir('/tmp/%s' % self.hostname)
        return list_files

    def repos(self):
        """Returns a list of all repo paths Pacha has been tracking"""
        db_file = '/tmp/%s/db/pacha.db' % self.hostname
        if os.path.exists(db_file):
            db = database.Worker(db_file)
            repos_list = []
            for repo in db.get_repos():
                repos_list.append(repo[1])
            return repos_list
        else:
            print "Aborting the --rebuild operation"
            print """The Pacha database from host %s could not be 
found.""" % self.hostname
            print """Make sure that the db directory is being tracked 
at /opt/pacha/hosts/%s/ in the Pacha server"""  % self.hostname
            sys.exit(1)

    def chmod(self, path):
        """Set permissions right by checking what is on the database"""
        info = self.permission_lookup(path)
        try:
            permissions = int(str(info[4]), 8) # convert back correct mode
            os.chmod(path, permissions)
        except TypeError, e:
            print """Could not find matching permissions info for 
path: %s""" % path

    def permission_lookup(self, path):
        """find the matching file in the database and return the
        metadata we need"""
        db_file = '/tmp/%s/db/pacha.db' % self.hostname
        if os.path.isfile(db_file):
            db = database.Worker(db_file)
            for info in db.get_meta(path):
                meta = list(info)
                return meta
        else:
            print "No permissions information was found in the database"

    def chown(self, path):
        """Change the group and owner of a single file or directory"""
        info = self.permission_lookup(path)
        try:
            owner = pwd.getpwnam(info[2])
            group = grp.getgrnam(info[3])
            os.chown(path, owner[3], group[2])
        except TypeError, e:
            print "Could not find matching ownership info for path: %s" % path

        except KeyError, e:
            print "Could not find matching ownership info for path: %s" % path


    def pre_hooks(self):
        """Anything that we find in the pacha_pre directory gets executed"""
        pre_dir = '/tmp/%s/pacha_pre' % self.hostname
        if os.path.exists(pre_dir):
            for hook in os.listdir(pre_dir):
                abspath = '%s/%s' % (pre_dir, hook)
                # make sure it is executable 
                rebuild_log.debug("chmod on %s" % abspath)
                os.chmod(abspath, 0755)
                # now execute it!
                call(abspath, shell=True)

    def post_hooks(self):
        """Anything in the pacha_post directory gets executed""" 
        post_dir = '/tmp/%s/pacha_post' % self.hostname
        if os.path.exists(post_dir):
            for hook in os.listdir(post_dir):
                abspath = '%s/%s' % (post_dir, hook)
                rebuild_log.debug("chmod on %s" % abspath)
                # make sure it is executable 
                os.chmod(abspath, 0755)
                # now execute it!
                call(abspath, shell=True)

