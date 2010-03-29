import os
import sys
import pwd
import grp
from subprocess import call
import shutil
from time import strftime
import confparser, log, database


class Rebuild(object):
    """Does all the rebuilding work when a host needs to be reconstructed 
    with Pacha. Minimal configurations come from pacha.conf and more complex
    executions come from the sh folder.
    All executions should be done with Super User powers.

    ### WORKFLOW ###
    1. Install Pacha on new machine
    2. run `pacha --rebuild` and answer the prompts:
        pacha server:
        pacha server user:
        machine to rebuild (hostname):
    3. This will scp all the files from the pacha server to /tmp/pacha
    4. Pacha will read the config and install packages
    replaced
    6. The config will say what files need to be replaced and copied from /tmp/
    to final location.
    7. A reboot is strongly suggested, and printed."""

    def __init__(self,
            server = None,
            server_user = None,
            hostname = None,
            ):
        self.server = server
        self.server_user = server_user
        self.hostname = hostname

    def retrieve_files(self):
        """scp all the files we need to /tmp/pacha"""
        # this could probably be much better with a Mercurial Clone command
        command = "scp -r %s@%s:/opt/pacha/hosts/%s /tmp/" % (self.server_user,
                self.server, self.hostname)
        call(command, shell=True)
        # if for some reason the above failed let me know:
        host_copy = '/tmp/%s' % self.hostname
        if os.path.isdir(host_copy):
            pass # we are good
        else:
            print """Pacha was not able to retrieve the files from the SSH server provided.
Check your settings and run --rebuild again."""
            sys.exit(1)

    def update(self):
        """Do a simple update to apt so it won't complain about unreachable
        repositories"""
        cmd = "sudo apt-get update"
        call(cmd, shell=True)
        log.append(module='rebuild.update', 
                line="updated repositories via apt-get update")

    def install(self):
        """Reads the config and install via apt-get any packages that have to 
        be in form of a list or a path"""
        conf = '/tmp/%s/conf/pacha.conf' % self.hostname
        parse = confparser.Parse(conf)
        parse.options()
        # do an update before everything:
        self.update()
        try:
            packages = parse.packages
            if type(packages) == type(list()): # we have a list 
                for package in packages:
                    log.append(module='rebuild.install', line="installing %s" % package)
                    command = "sudo apt-get -y install %s" % package
                    call(command, shell=True)
            else:
                # we have to be flexible and allow a path or a file name
                package_file = os.path.basename(package)
                package_file_path = '/tmp/%s/conf/%s' % (self.hostname, package_file)
                if os.path.isfile(package_file_path): # is it really there?
                    txt = open(package_file_path)
                    for line in txt.readlines():
                        package = line.split('\n')[0]
                        log.append(module='rebuild.install', line="installing %s" % package)
                        command = "sudo apt-get -y install %s" % package
                        call(command, shell=True)
                else:
                    sys.stderr.write("""Could not find a text file 
with packages in: %s\n""" % package_file_path)
        except AttributeError, error:
            log.append(module='rebuild.install', type='ERROR', line="%s" % error)
            sys.stderr.write("""No packages specified for installation 
in config\n""")

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
                    if path[3] == 'dir': # if this is a dir then do default replace
                        log.append(module='rebuild.replace_manager', 
                                line = "dirname in self.tracked: %s" % dirname)
                        self.default_replace(dirname, path[1])
                    if path[3] == 'single': # a single file tracking
                        log.append(module='rebuild.replace_manager',
                                line='single file in self.tracked: %s' % dirname)
                        self.single_tracking(path[1])
        else:
            print "Could not find DB at /tmp/%s/db/pacha.db" % self.hostname
            sys.exit(1)

    def single_tracking(self, path):
        """You can have specific files to be rebuilt to avoid replacing
        whole directories."""
        #repos_path = self.repos()
        log.append(module='rebuild.single_tracking',
                line='single repo path: %s' % path)
        tmp_dir = '/tmp/%s/' % self.hostname
        log.append(module='rebuild.single_tracking', 
                line='tmp_dir: /tmp/%s' % self.hostname)
        # get list of directories in tmp and do a double loop
        #for path in repos_path:
        base = os.path.basename(path) #gets us the file name
        dir_path = os.path.dirname(path)
        directory = os.path.basename(dir_path) # finally a dir name from the path
        tmp_subdir = tmp_dir+directory
        log.append(module='rebuild.single_tracking', line= 'base file: %s' % base)
        for file in os.listdir(tmp_subdir): 
            if file == base: # we have a winner
                log.append(module='rebuild.single_tracking',
                line='found path with matching file: %s %s' % (path, 
                    base))
                if os.path.exists(path):
                    shutil.move(path,'/tmp/%s.%s' % (base, strftime('%H%M%s'))) # get it out of the way
                    log.append(module='rebuild.single_tracking', 
                            line='moving %s to /tmp' % path)
                shutil.copyfile(tmp_subdir+'/'+file, path)
                log.append(module='rebuild.single_tracking',
                    line='moving %s to %s' % (tmp_subdir+'/'+file, path))
                # get permissions right without walking the tree
                self.chmod(path)
                self.chown(path)

    def default_replace(self, dirname, path):
        """Usually you will replace the configs you were backing up. Here
        the directory gets pushed if not specified in the database"""
        log.append(module='rebuild.default_replace', line='repos path: %s' % path)
        tmp_dir = '/tmp/%s/' % self.hostname
        log.append(module='rebuild', line='tmp_dir: %s' % tmp_dir)
        # get list of directories in tmp and do a double loop
        base = os.path.basename(path)
        log.append(module='rebuild.default_replace', line= 'base dir: %s' % base)
        if dirname == base: # we have a winner
            log.append(module='rebuild.default_replace',
            line='DR found path with matching dir: %s %s' % (dirname, 
                base))
            if os.path.exists(path):
                shutil.move(path,'/tmp/%s.%s' % (base, strftime('%H%M%s'))) # get it out of the way
                log.append(module='rebuild.default_replace', line='moving %s' % path)
            shutil.copytree(tmp_dir+dirname, path)
            log.append(module='rebuild.default_replace',
                line='moving %s to %s' % (tmp_dir+dirname, path))
            # get ownership and permissions right walking the tree
            self.walk(path)

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
            print "The Pacha database from host %s could not be found." % self.hostname
            print """Make sure that the db directory is being tracked at /opt/pacha/hosts/%s/
in the Pacha server"""  % self.hostname
            sys.exit(1)

    def chmod(self, path):
        """Set permissions right by checking what is on the database"""
        info = self.permission_lookup(path)
        try:
            permissions = int(info[4], 8) # convert back for correct mode
            os.chmod(path, permissions)
        except TypeError:
            print "Could not find matching permissions info for path:"
            print path

    def permission_lookup(self, path):
        """find the matching file in the database and return the
        metadata we need"""
        db_file = '/tmp/%s/db/pacha.db' % self.hostname
        if os.path.exists(db_file):
            db = database.Worker(db_file)
            for info in db.get_meta(path):
                return info

    def chown(self, path):
        """Change the group and owner of a single file or directory"""
        info = self.permission_lookup(path)
        try:
            owner = pwd.getpwnam(info[2])[3]
            group = grp.getgrnam(info[3])[2]
            os.chown(path, owner, group)
        except TypeError:
            print "Could not find matching ownership info for path:"
            print path


