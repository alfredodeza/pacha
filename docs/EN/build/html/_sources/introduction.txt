.. _introduction:

Introduction
===============
A few things you should know about Pacha, like Operating Systems supported and a couple of our 
dependencies.


Dependencies
-----------------
We have 3 dependencies, make sure you have them installed and ready:

 *  SSH (versions 4.7p1 to 5.1p1)
 *  Mercurial (versions 0.9.5 to 1.3.1)
 *  Python (version 2.5 to 2.6)

About version differences
----------------------------
You should NOT use Pacha with different versions of Mercurial in different servers otherwise you will get undesired behavior when trying to rebuild a host. This would happen when functionality found in later versions of Mercurial will conflict with the older ones, hence the ability lack of being able to get the latest version of the files you need to rebuild.

Operating Systems
-------------------
Pacha should work with any system that has the above installed. If you experience any issues let us know!

Pacha has been used and tested in:

 * OpenSolaris 10
 * Ubuntu Linux 
 * Mac OS X Snow Leopard 

 Remember though, as long as you meet the dependencies you should be able to run Pacha.

 
 
