"""
Reporting system for deployment. Hosts will be asking themselves:

 * Block *everything* until you get directory structure built
 * Sends a 1 when it has a file. Tracker will be incharge of keeping "DONT HAVEs" as 0
 * Update list of HAVE (update the tracker)
 * DO NOT Update list of DONT HAVE
 * Let tracker know when you are done
    
"""
