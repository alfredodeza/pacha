.. _changelog:

Changelog
============

0.2.4
-------

 Changes 
 *  Logs have to be turned on and be pointing to a file 
 *  Added a new warning message that alerts a config file that no longer exists
 *  The config file accepts logging options like: log_enable and log_path. If both are not set, logging is disabled.

 Bug Fixes
 *  Logging is no longer pushing to ouput to the terminal
 *  Daemon will no longer crash due to logging issues
