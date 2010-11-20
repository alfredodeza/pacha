.. _changelog:

Changelog
==========

0.3.0
-----
 * Major release that breaks some backward compatibility.
 * Removes HG as sole backend for Pacha. Rsync takes over and DVCS is optional
   at Master instances

0.2.5
-------
 * Minor release
 * Adds a few more tests that bumps coverage to close to 75%
 * Minor changes in how we check for modified files. Before we used 'hg st' with Popen but
   we check for os.lstat and modified timestamps. Much faster and less code.

0.2.4
-------
 * Added "--daemon-run-once" that allows the daemon to run on the foreground one time and then exit.
 * Added "--restore-db" that will pull the database from a master server 
 * Included a lot more tests for stuff that was missing like watch and watch single.
 * Changed some attributes in __init__ that allows better argv handling and testing. 
 * Fixes a bug where the database was not tracked at all 
 * Adds a way to "auto-correct" certain things when there is a mismatch in hgrc on where/what username to use to push 
 * Pacha doesn't need to parse the config file every single time it is run. We now have persistent configurations.
 * Warning messages are now color coded (mostly yellowish.
 * Pacha can now "take over" an exisiting repo. Useful when you have used pacha before or when wanting to push somewhere else.
 * Fixes issue where --watch path was not absolute
 * adds an except block to catch possible permission denied issues when updating
 * Added PRE and POST hooks that get executed when rebuilding (FINALLY!)
 * Simplified the way we ask input for rebuilding a host. Now you only need to pass in the hostname (since everything should be in the config file)
 * Fixes unicode issue with Mercurial that would make it crash.
 * Cleans up commented out code and unused imports.
 * Removes Row factory, that was causing issues with Sqlite3 
 * Added Guachi for persistent configurations and mappings.
 * Logging will now be OFF in the command line unless you pass the -v or --verbose flag.
 * Removes the '--remove-config' option. If you want to override a config just add a new one.


0.2.3
------

 * Better warning messsages that don't allow you to make changes unless you add a config.
 * Configuration defaults that fill in missing values 
 * "--daemon-foreground" allows anyone to run the daemon in the foreground (e.g. it doesn't daemonize at all)
 * All ConfigParse options are now within a class instead of a huge function.

0.2.0
------

 *  Changed installation type to work as a Python package via setup.py

0.1.0
-------

 *  Users coming from versions 0.0.4 and older cannot upgrade to 0.1.0 with pacha --upgrade
 *  Added Sqlite3 that will effectively break on Python versions older than 2.5

0.0.4
------

 *  --upgrade has been rebuilt to grab the latest .tar.gz from the homepage instead of pulling changes via Mercurial. 
    Some info about what is going on when you upgrade is now displayed.
 *  master = True If you are a Pacha user from any previous version, you will need to add the following line to pacha 
    for your master server: master = True
    This will tell the daemon to run: hg update on your host repositories so you can always see the latests changes 
    (when a server pushes changes, files do not get updated via mercurial).
 *  More tests have been added to Pacha which have triggered some re-coding at some of the libraries. It is always 
    great to be able to test specific functionality of Pacha to make sure we have the right results.
 *  Faster Pacha! On most of the Mercurial calls Pacha was making on the backend, we were actually forking a 
    subprocess to run hg. Speed has increased a lot since we are now calling and import modules straight from Mercurial.
