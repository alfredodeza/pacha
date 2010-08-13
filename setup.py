import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages

tests_require = ['nose']

setup(
    name = "pacha",
    version = "0.2.0",
    packages = find_packages(),
    scripts = ['pacha/sripts/pacha.py'],
    install_requires = ['bottle>=0.8', 'pymongo'],
    entry_points = {
        'console_scripts': [
            'pacha = pacha:main'
            ]
        },
    include_package_data=True,
    package_data = {
        '': ['distribute_setup.py'],
        },

    # metadata for upload to PyPI
    author = "Alfredo Deza",
    author_email = "alfredodeza [at] gmail [dot] com",
    description = "Stats Middleware for WSGI applications.",
    long_description = """\
 Provides statistics for any WSGI application:

  * Requests Per Second
  * Time to respond

 Data can be accessed via a web interface and eventually
 can be accomodated with plugins to output to any
 monitoring system.

 Full documentation can be found at http://code.google.com/p/waskr
 """,

    license = "MIT",
    py_modules = ['waskr'],
    keywords = "WSGI stats statistics request measure performance",
    url = "http://code.google.com/p/waskr",   

)

