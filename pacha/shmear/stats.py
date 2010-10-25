"""
Keeping records
---------------------

Initially no one has anything except the Master, so it needs to build a "table"
with the list of files for *each* node in the seeding list and prefill them with
0's (e.g. DONT HAVEs).

This is the core of the tracker, keeping records.

Weigh System
-----------------
It also needs to have a weighing system that compares HAVES with DONT HAVEs in hosts.

The weighing system should balance the network usage for hosts to avoid having single
bottlenecks when other hosts aren't being used at all.

Initial Seeding
------------------
As soon as the master "seeds" it should only push one time for every file it has.
This will force the master to avoid being hit and create a bottleneck as it seeds 
the data.

Eventually the master "depleets" its one-time-file-serve and the hosts will start
pulling the files between them.

Unless
==========
Unless of course we are not sharing files with more than one host so we avoid all this
splitting and we just send the files.

"""
