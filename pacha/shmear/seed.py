"""
Builds the information necessary to do a new deployment.

Specifically, we need:

 * List of directories to create.
 * A unique UUID for the deployment
 * List of absolute paths for top level directories to replace
 * Should be able to push the seeding file to N hosts. (it should know abouut those hosts)
"""

def broadcast():
    """given N number of hosts, we tell them there is a new build
    Broadcast should do this in batches of 50 hosts"""
    pass

def dirs():
    pass

def build_seed_file():
    """Build a seed file that provides a few parameters that we absolutely need:

    * UUID of the actual deployment
    * List of top directories to create
    * List of absolute paths to replace
    * List of hosts involved in the build
    """
    pass

# The seeding file should be named after the UUID and scp'd to /tmp
# that way pacha only needs to check /tmp/%s % UUID

# Compression
# This is probably the biggest bottleneck. Sending a file that is 20kb
# to 1,000 hosts increases this push to 20MB.
#
# with compression we could easily get that 20kb file to probably 1/4
# the original size.


