.. _testing:
   
Testing  
================
A few notes on how to setup and run your tests properly

Introduction
-----------------
We recommend you have Python Nose installed for running tests::

    pip install nose

You could also run the tests manually, but ``nosetests`` will be easier to use.

Dependencies
---------------
Other than ``nosetests`` you should already be setup with Mercurial and SSH.


Keys and SSH
----------------
Just like a fresh installation of Pacha, you need to have proper keys setup with the right user for SSH.
Once all your keys are correctly set you can run your tests.

A brief example on how to get started with SSH Keys (the tests will use the current user and localhost for SSH)::

    cd ~/.ssh
    ssh-keygen
    [...]
    cat id_rsa.pub >> authorized_keys


Install first, then test
-------------------------
There are some core settings that depend on Pacha being installed. Please make sure you have Pacha installed before running your tests. None of our tests are destructive, so even if you have your settings already in place, Pacha will not be removing or tinkering with files already being used.

Running your tests
------------------------
Within the Pacha directory run the following command::

    nosetests -v

The auto-discover tool from ``nose`` will find the tests (located in the tests directory) and run them one by one.

Ideally, you should see output (once Pacha is installed) like this::

    (vpacha)[alfredo@mbp ~/vpacha/pacha/tests]$ nosetests -v
    Add a configuration file path ... ok
    You can't add duplicates to the config table ... ok
    Add a config path and then query it ... ok
    Check if the db file was created ... ok
    test_insert_meta (test_database.TestWorker) ... ok
    Do a simple insert of a path into db ... ok
    Do a simple insert of a path and its type into db ... ok
    Remove a record from the db ... ok
    Add and then remove a configuration file path ... ok
    Updates the DB revision information ... ok
    test_hg (test_dependencies.TestDependencies) ... ok
    test_hg_commands (test_dependencies.TestDependencies) ... ok
    test_hg_hg (test_dependencies.TestDependencies) ... ok
    test_hg_ui (test_dependencies.TestDependencies) ... ok
    Clones the test repo to localhost ... ok
    Builds a mercurial repo and commits ... ok
    We create a file and then we add it ... ok
    Add a line for automated push inside .hg ... ok
    Return False for issues if hgrc cannot be written ... ok
    Initializes a directory with Mercurial ... ok
    Push local changes to remote server ... ok
    Update a working hg repository ... ok
    Return False to a non existent hg repository ... ok
    Validate a working hg repository by returning True ... ok
    Create a host folder ... ok
    Don't create a host folder if present ... ok
    Get the right hostname ... ok
    test_import_pacha (test_imports.TestImports) ... ok
    test_pacha_config_options (test_imports.TestImports) ... ok
    test_pacha_database (test_imports.TestImports) ... ok
    test_pacha_host (test_imports.TestImports) ... ok
    test_pacha_log (test_imports.TestImports) ... ok
    test_pacha_permissions (test_imports.TestImports) ... ok
    Check the group ownership of a directory ... ok
    Check correct ownership of a directory ... ok
    Return an octal representation of file permissions ... ok
    test_insert (test_permissions.TestTracker) ... ok
    A single file should be tracked ... ok
    Walker should insert the group for path ... ok
    Walker should insert the owner for path ... ok
    Walker should insert the dir path ... ok
    Walker should insert rwx for path ... ok
    Walker should be able to track single file ... ok

    ----------------------------------------------------------------------
    Ran 43 tests in 3.801s

    OK

