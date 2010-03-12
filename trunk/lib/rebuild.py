# Copyright 2009-2010 Alfredo Deza
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
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

    def update(self):
        """Do a simple update to apt so it won't complain about unreachable
        repositories"""
        cmd = "sudo apt-get update"
        call(cmd, shell=True)
        log.append(module='rebuild', 
                line="updated repositories via apt-get update")

    def install(self):
        """Reads the config and install via apt-get any packages that have to 
        be in form of a list"""
        conf = '/tmp/%s/conf/pacha.conf' % self.hostname
        parse = confparser.Parse(conf)
        parse.options()
        # do an update before everything:
        self.update()
        try:
            packages = parse.packages
            for package in packages:
                log.append(module='rebuild', line="installing %s" % package)
                command = "sudo apt-get -y install %s" % package
                call(command, shell=True)
        except AttributeError, error:
            log.append(module='rebuild', type='ERROR', line="%s" % error)
            sys.stderr.write("""No packages specified for installation 
in config\n""")

    def replace_manager(self):
        """Depending on the database information for each path, you may or may not have
        specific files you want to override. This manager method dispatches correctly
        after verifying if you were tracking a single file or a directory"""
        
        db_location = '/tmp/%s/db/pacha.db' % self.hostname
        if os.path.exists(db_location):
            # connect to the DB:
            db = database.Worker(db=db_location)
            for path in db.get_repos():
                for dirname in self.tracked():
                    if path[3] == 'dir': # if this is a dir then do default replace
                        log.append(module='rebuild.replace_manager', 
                                line = "dirname in self.tracked: %s" % dirname)
                        self.default_replace(dirname)
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
        repos_path = self.repos()
        log.append(module='rebuild.single_tracking',
                line='single repos path: %s' % repos_path)
        tmp_dir = '/tmp/%s/' % self.hostname
        log.append(module='rebuild.single_tracking', 
                line='tmp_dir: /tmp/%s' % self.hostname)
        # get list of directories in tmp and do a double loop
        for path in repos_path:
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
                        shutil.move(path,'/tmp/%s.%s' % (base, strftime('%H%M%S'))) # get it out of the way
                        log.append(module='rebuild.single_tracking', 
                                line='moving %s to /tmp' % path)
                    shutil.move(tmp_subdir+'/'+file, path)
                    log.append(module='rebuild.single_tracking',
                        line='moving %s to %s' % (tmp_subdir+'/'+dirname, path))

    def default_replace(self, dirname):
        """Usually you will replace the configs you were backing up. Here
        all directories get pushed if not specified in the DB"""
        repos_path = self.repos()
        log.append(module='rebuild', line='repos path: %s' % repos_path)
        tmp_dir = '/tmp/%s/' % self.hostname
        log.append(module='rebuild', line='tmp_dir: %s' % tmp_dir)
        # get list of directories in tmp and do a double loop
        for path in repos_path:
            base = os.path.basename(path)
            log.append(module='rebuild', line= 'DR base dir: %s' % base)
            for dirname in self.tracked():
                if dirname == base: # we have a winner
                    log.append(module='rebuild',
                    line='DR found path with matching dir: %s %s' % (dirname, 
                        base))
                    if os.path.exists(path):
                        shutil.move(path,'/tmp/%s.%s' % (base, strftime('%H%M%S'))) # get it out of the way
                        log.append(module='rebuild', line='moving %s' % path)
                    shutil.move(tmp_dir+dirname, path)
                    log.append(module='rebuild',
                        line='moving %s to %s' % (tmp_dir+dirname, path))

    def tracked(self):
        """There needs to be a comparison between the copied files and the
        files that are in the config file. If they are being tracked but
        nothing is specified in the config the whole directory is moved."""
        list_files = os.listdir('/tmp/%s' % self.hostname)
        return list_files

    def repos(self):
        """Returns a list of all repo paths Pacha has been tracking"""
        db = database.Worker(db='/tmp/%s/db/pacha.db' % self.hostname)
        repos_list = []
        for repo in db.get_repos():
            repos_list.append(repo[1])
        return repos_list
