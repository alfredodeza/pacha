import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup

tests_require = ['pytest']

setup(
    name = "pacha",
    version = "0.3.0",
    packages = ['pacha'],
    install_requires = [
        'supay==0.0.7', 
        'guachi==0.0.6',
        'coima==0.0.2'],
    entry_points = {
        'console_scripts': [
            'pacha = pacha:main_'
            ]
        },
    include_package_data=True,
    package_data = {
        '': ['distribute_setup.py'],
        },

    # metadata 
    author = "Alfredo Deza",
    author_email = "alfredodeza [at] gmail [dot] com",
    description = "Systems configuration/management engine",
    long_description = """\
Pacha was designed from the ground up to be a simple way to backup and 
manage software configuration files from single or multiple server 
instances across the network.

Pacha's approach is to easily deploy an instance and capture any changes 
via a version control, giving the System Administrator the ability 
to rollback and safe guard valid, working configurations and rebuild a 
host from those same configurations.

Don't learn another language
------------------------------
Other configuration frameworks tell you this, but are written in a language like Ruby and require you to extend,modify or adapt this writing Ruby. We don't! It doesn't matter that Pacha is written in Python. You do not need to know Python to make any changes to the software you want to deploy.

Easy learn curve
-----------------------
One main configuration file to manage the package to be installed and one directory where you can place any number of executable shell scripts to extend and modify your deployment according to your needs.

Versioned Configurations
----------------------------
Keep track of any changes done to a configuration file and rollback easily. We support Mercurial, GIT and SVN to version your configurations.

Light
---------
Deploy Pacha as a client, server, or standalone version. Either way, you get an extremely light, low memory tool that can communicate with your configuration files almost instantly.

Extend and Conquer
------------------------
Forget about the "but this tool doesn't do this". We provide a full hook environment to plug in directly into Pacha so you can extend whatever need you have for your deployment.

Security
-----------
Transferring system configuration files, even across a trusted private network is a security risk. Pacha tackles this problem using SSH as the transport protocol. Although this may add a slight complexity to the framework, we encourage security and think this is the best shot for dealing with critical data related to your systems.


""",
   classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],

    license = "MIT",
    keywords = "systems configuration management engine hg mercurial",
    url = "http://pacha.cafepais.com",   

)

