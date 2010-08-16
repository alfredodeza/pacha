from logging import getLogger, basicConfig, DEBUG, INFO

#from pacha.config_options import config_defaults

#def setlogging(config=None):
#    if config == None:

def defaults(config=None):
    """From the config dictionary it checks missing values and
    adds the defaul ones for them if any"""
    if config == None:
        config = {}
    defaults = {
            'frequency': 60,
            'master': False,
            'host': 'localhost',
            'ssh_user': 'root',
            'ssh_port': 22,
            'hosts_path': '/opt/pacha',
            'log_level': 'DEBUG',
            'log_format': '%(asctime)s %(levelname) %(name)s %(message)s',
            'log_datefmt' : '%H:%M:%S'
            }

    for key in defaults:
        try:
            config[key]
        except KeyError:
            config[key] = defaults[key]
    return config




config = defaults()
levels = {
        'debug': DEBUG,
       'info': INFO
        }

level = levels.get(config['log_level'])
log_format = config['log_format']
datefmt = config['log_datefmt']

basicConfig(
        level   = level,
        format  = log_format,
       datefmt = datefmt)


#setlogging()
## Set logger objects for all modules
daemon          = getLogger('pacha.daemon')
database        = getLogger('pacha.database')
hg              = getLogger('pacha.hg')
host            = getLogger('pacha.host')
permissions     = getLogger('pacha.permissions')
config          = getLogger('pacha.config_options')
host            = getLogger('pacha.host')
