#!/usr/bin/env python
#
# Copyright (c) 2009-2010 Alfredo Deza <alfredodeza [at] gmail [dot] com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import os

from guachi                             import ConfigMapper
from teja.util                          import WARNING, get_db_file, get_db_dir
from teja.runners                       import TestRunner


DB_FILE = get_db_file()
DB_DIR = get_db_dir()


 
class TejaCommands(object):

    def __init__(self, 
            argv=None, 
            test=False, 
            parse=True, 
            db=ConfigMapper(DB_FILE),
            db_file=DB_FILE):
        self.db = db 
        self.db_file = db_file
        if argv is None:
            argv = sys.argv

        self.test = test
        if parse:
            self.parseArgs(argv)
        self.config = {}


    def msg(self, msg, std="out"):
        if std == "out":
            sys.stdout.write(msg)
        else:
            sys.stderr.write(msg)
        if not self.test:
            sys.exit(1)


    def check_config(self):
        """if any commands are run, check for a MASTER config file Location"""
        conf = self.db.stored_config()

        #check for a first time run 
        if len(conf.get_all()) == 0:
            conf['runner'] = 'pytest'
        if len(conf.items()) <= 1: # config might not be set 
            self.msg(WARNING, std="err")
        else:
            return self.db.stored_config()


    def config_values(self):
        conf = self.db.stored_config()
        try:
            print "\nTestRunner Configuration : \n" 
            for i in conf.items():
                print "%-15s= %-4s" % (i[0], i[1])
            print ''
        except Exception, error:
            # sometimes we can't catch the error
            print "Could not complete command %s" % error


    def detect(self, string):
        """Make sure what runner are we talking about"""
        pytest = ['py.test', 'pytest', 'py', 'py_test']
        nose = ['nose', 'python-nose', 'nosetests']
        if string.lower() in pytest:
            return 'pytest'
        elif string.lower() in nose:
            return 'nose'
        else:
            return False


    def set_runner(self, runner):
        runner = self.detect(runner)
        if runner:
            conf = self.db.stored_config()
            conf['runner'] = runner
        else:
            self.msg("Couldn't set a valid TestRunner.")


    def set_config_path(self, path):
        if os.path.exists(path):
            absolute = os.path.abspath(path)
            if os.path.isfile(absolute):
                absolute = os.path.dirname(absolute)
            conf = self.db.stored_config()
            conf['config_path'] = absolute 
        
    
    def parseArgs(self, argv):

        options = ('runner', 'values', 'path')

        match = [i for i in argv if i in options]

        # if there is no match in teja options pass them 
        # on to py.test 
        if not match:
            tests = TestRunner(argv)
            tests.run()

        else:
            arg_count = {}
            count_arg = {}
            
            for count, argument in enumerate(sys.argv):
                arg_count[argument] = count 
                count_arg[count] = argument

            if arg_count.get('runner'):
                count = arg_count.get('runner')
                value = count_arg.get(count+1)
                if value:
                    self.set_runner(value)
                else:
                    self.msg("Please provide a value for 'runner'.")

            if arg_count.get('values'):
                self.config_values()

            if arg_count.get('path'):
                count = arg_count.get('path')
                value = count_arg.get(count+1)
                if value:
                    self.set_config_path(value)
                else:
                    self.msg("Please provide a value for 'path'.")


main = TejaCommands

def main_():
    main()

