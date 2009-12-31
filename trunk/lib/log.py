# Author: Alfredo Deza
# Email: alfredodeza [at] gmail dot com
# License: MIT
# Copyright 2009-2010 Alfredo Deza
#
"""Handles all logging for Pacha. Not using Python's logging module
knowlingly."""
import os
import shutil
from time import strftime
from subprocess import call


class Log(object):
    """Main class of the log module"""

    def __init__(self,
            log_file = '/var/log/pacha.log',
            type = 'INFO',
            timestamp = strftime('%b %d %H:%M:%S'),
            module = 'pacha'):
        self.log_file = log_file
        self.type = type
        self.timestamp = timestamp
        self.module = module
        



