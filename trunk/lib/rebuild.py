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
import confparser, log


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
        """Depending on the configuration file, you may or may not have
        specific files you want to override. This method does a cross
        check between what directories Pacha has kept track and if they
        have a corresponding match in the config file."""
        # we parse the conf file to get specific tracking:
        conf = '/tmp/%s/conf/pacha.conf' % self.hostname
        parse = confparser.Parse(conf)
        parse.options()
        log.append(module='rebuild', line="read config file and parsed options")
        #check if the config has dirs we have in tmp:
        for dirname in self.tracked():
            log.append(module='rebuild', line = "dirname in self.tracked: %s" % dirname)
            self.default_replace(dirname)


    def specific_tracking(self, dirname, item):
        """You can specify specific files to be rebuilt to avoid replacing
        whole directories. Mercurial can't keep track of single files."""
        ##
        # BUGGY / NOT YET IMPLEMENTED
        ##
        # now be build the paths and move stuff
        default_path = "/%s/%s" % (dirname, item)
        log.append(module='rebuild', line = 'default path: /%s/%s' % (dirname, item))
        shutil.move(default_path, '/tmp/%s.%s' % (item, strftime('%H%M%S')))
        log.append(module='rebuild', line="moving %s to %s" % (default_path, 
                default_path+'.old'))
        replacer = '/tmp/%s/%s/%s' % (self.hostname, dirname, item)
        shutil.move(replacer, default_path)
        log.append(module='rebuild', 
                line="ST moving %s to %s" % (replacer, default_path))

    def default_replace(self, dirname):
        """Usually you will replace the configs you were backing up. Here
        all directories get pushed if not specified in the config"""
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
        # THIS IS NO LONGER THE CASE !!! REMOVE THIS

    def repos(self):
        """Returns a list of all repo paths Pacha has been tracking"""
        db = database.Worker(db='/tmp/%s/db/pacha.db' % self.hostname)
        repos_list = []
        for repo in db.get_repos():
            repos_list.append(repo[1])
        return repos_list
