import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup

tests_require = ['nose', 'unittest2']

setup(
    name = "pacha",
    version = "0.2.4",
    packages = ['pacha'],
    install_requires = ['supay>=0.0.7', 'mercurial==1.5.3', 'guachi==0.0.4'],
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
    url = "http://code.google.com/p/pacha",   

)

