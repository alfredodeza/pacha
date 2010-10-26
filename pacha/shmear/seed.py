
def broadcast():
    """given N number of hosts, we tell them there is a new build
    Broadcast should do this in batches of 50 hosts"""
    pass


# The seeding file should be named after the UUID and scp'd to /tmp
# that way pacha only needs to check /tmp/%s % UUID

# A seeindg file should be only pushed to a maximum of 5 hosts in a threaded
# way.
# 
# These 5 hosts will push the file again to a maximum of 5 hosts too. This 
# avoids the problem of having the master pushing data to hundreds of servers
# at the same time.
# 


class Builder(object):
    """
    Builds the information necessary to do a new deployment.

    Specifically, we need:

     * List of directories to create.
     * A unique UUID for the deployment
     * List of absolute paths for top level directories to replace
     * Should be able to push the seeding file to N hosts. (it should know abouut those hosts)
    """

    def __init__(self, hosts):
        self.hosts = hosts 

    def build_host_list():
        """Create the host list for the seeding file minus the hosts we are already
        pushing to."""
        pass

    def build_seed_file():
        """Build a seed file that provides a few parameters that we absolutely need:

        * UUID of the actual deployment
        * List of top directories to create
        * List of absolute paths to replace
        * List of hosts involved in the build
        """
        pass

    def dirs():
        pass

