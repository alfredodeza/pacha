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

The Master was holding a bunch of other servers configuration files in ``/
