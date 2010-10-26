"""
Not entirely sure about needing this file.

Initial intent is to fixate master related things here.
"""

# Message center: it should be the one that receives the messages 
# from other hosts. Things like:
#  
#  *  Done with building directory structure for current build 
#  *  Percent done [ if grabbing files from other hosts ] 
#
# It should provide a "private" command line option to allow
# remote hosts to call this message center and provide information 
# Something like::
#   pacha __message [hostname] [status]
#
# Hostname would be the qualifier (it could be the IP as well) and 
# status would be the current status of that host. By default this 
# falls back to ``wait``
#
# the *very* small API should be something like:
#
# ``in_progress``   : Grabbing Files
# ``grab_wait``     : Either building the dir structure or just trying to find files
# ``grab_done``     : Finished grabbing files with dir structure
# ``verifying``     : Verifying checksums 
# ``done``          : Finished all tasks
