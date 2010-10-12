.. _rebuilding:


Rebuilding
===============
The rebuild process is pretty straight forward. The scenario that we are going to discuss here 
involves a Master Pacha server that has been holding some files for a Slave that was pushing 
automatically those configurations.

We will assume that the Slave crashed, was unable to recover and you need to get everything 
up and running again.


Prepare the new server
------------------------
The host to be rebuilt need 2 things before anything else:

 * Have the SSH keys accepted in the Master Pacha server.
 * A Pacha configuration file.

The above could be avoided if you are hosting images in a cloud environment or if you have a  
fully virtualized environment where you can have "Base Server Images". These images could hold 
the SSH keys already and have the right Pacha configs already set.

In some of the environments where Pacha is used, the virtual environment was served by Xen Server
and a few base images where ready to be booted up with SSH keys and Pacha configs already set. 

At this point, you should be able to:

 * SSH into the Master Pacha Server with no password prompt.
 * Pacha should not give you a warning about configurations.


A crash story
----------------
To be able to understand the rebuild process and what is going where, lets know a bit more 
about the crash that took that server down.

The Master Pacha Server was receiving confiogurations from a server called Bar. Bar had 
a very important directory called ``foo`` and it was located in ``/opt/foo`` and contained 
a few configuration files that were needed in production.

The Master was holding a bunch of other servers configuration files in ``/pacha/hosts``.

This would make server Bar exist in ``/pacha/hosts/bar`` and the actual directory that it 
was watching in ``/pacha/hosts/bar/foo``.


Actual Rebuilding
--------------------
Now that you have a server with proper SSH keys up, lets see how the configuration for this scenario 
would look like::

    [DEFAULT]

    ###################################
    # Pacha Server Configuration
    ###################################

    pacha.frequency = 12

    # Pacha master server 
    pacha.host = master.example.com

    pacha.ssh.user = bar_user

    pacha.hosts.path = /pacha/hosts

That is **13** lines including comments! It can't get more simple than that simple config file.

To be rebuild this host, you would need to run the ``--rebuild`` flag::

    pacha --rebuild bar 

You get a confirmation message::

    SSH Connection: bar_user@master.example.com
    SSH Port:       22             
    Host to rebuild: bar      
    Hit Enter to confirm or Ctrl-C to cancel
        

Once you hit enter you should see output similar to this::

    .empty                                           100%    0     0.0KB/s   00:00    
    00changelog.i                                    100%   57     0.1KB/s   00:00    
    branch                                           100%    8     0.0KB/s   00:00    
    branchheads.cache                                100%   92     0.1KB/s   00:00    
    dirstate                                         100%   88     0.1KB/s   00:00    
    requires                                         100%   23     0.0KB/s   00:00    
    00changelog.i                                    100%  561     0.6KB/s   00:00    
    00manifest.i                                     100%  428     0.4KB/s   00:00    
    .empty.i                                         100%   64     0.1KB/s   00:00    
    pacha.db.i                                       100% 2979     2.9KB/s   00:00    
    fncache                                          100%   30     0.0KB/s   00:00    
    undo                                             100%   56     0.1KB/s   00:00    
    undo.branch                                      100%    7     0.0KB/s   00:00    
    undo.dirstate                                    100%   88     0.1KB/s   00:00    
    pacha.db                                         100%   18KB  18.0KB/s   00:00    
    00changelog.i                                    100%   57     0.1KB/s   00:00    
    branch                                           100%    8     0.0KB/s   00:00    
    branchheads.cache                                100%   92     0.1KB/s   00:00    
    dirstate                                         100%   61     0.1KB/s   00:00    
    requires                                         100%   23     0.0KB/s   00:00    
    00changelog.i                                    100%  186     0.2KB/s   00:00    
    00manifest.i                                     100%  111     0.1KB/s   00:00    
    blah.i                                           100%   64     0.1KB/s   00:00    
    fncache                                          100%   12     0.0KB/s   00:00    
    undo                                             100%   45     0.0KB/s   00:00    
    undo.branch                                      100%    7     0.0KB/s   00:00    
    undo.dirstate                                    100%    0     0.0KB/s   00:00  

All those files are being transferred from the master to the host to be rebuild into a temporary
location in ``/tmp`` and from there it is being pushed to the directories where they existed 
originally.

Once it is done copying all the files, it runs a permission check and sets the permissions that 
it had stored from before (e.g. owner, group ownership and rwx permissions).
