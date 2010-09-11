from ConfigParser import ConfigParser
from os.path import isfile
from pacha.database import Worker

def options(config=None):
    """Instead of calling ConfigParser all over the place
    we gather, read, parse and return valid configuration
    values for any pacha log.utility here, config should
    always be a file object or None and config_options
    always returns a dictionary with values"""
    
    # If all fails we will always have default values
    configuration = defaults()

    # Options comming from the config file have
    # longer names, hence the need to map them correctly
    opt_mapper = {
            'pacha.frequency':'frequency',
            'pacha.master':'master',
            'pacha.host':'host',
            'pacha.ssh.user':'ssh_user',
            'pacha.ssh.port':'ssh_port',
            'pacha.hosts.path': 'hosts_path',
            'pacha.hg.autocorrect': 'hg_autocorrect',
            'pacha.log.enable': 'log_enable',
            'pacha.log.path' : 'log_path',
            'pacha.log.level':'log_level',
            'pacha.log.format':'log_format',
            'pacha.log.datefmt':'log_datefmt'
            }

    try:
        if config == None or isfile(config) == False:
            configuration = defaults()
            return configuration

    except TypeError:
        if type(config) is dict:
            configuration = defaults(config)
    
    else:
        try:
            converted_opts = {}
            parser = ConfigParser()
            parser.read(config)
            file_options = parser.defaults()

            # we are not sure about the section so we 
            # read the whole thing and loop through the items
            for key, value in opt_mapper.items():
                try:
                    file_value = file_options[key]
                    converted_opts[value] = file_value

                except KeyError:
                    pass # we will fill any empty values later with config_defaults
            try:
                configuration = defaults(converted_opts)
            except Exception, e:
                print "Couldn't map configuration: %s" % e

        except Exception, e:
            pass
            print "Couldn't map configuration: %s" % e

    return configuration

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
            'hg_autocorrect': True,
            'log_enable': False,
            'log_path': None,
            'log_level': 'DEBUG',
            'log_format': '%(asctime)s %(levelname)s %(name)s %(message)s',
            'log_datefmt' : '%H:%M:%S'
            }

    for key in defaults:
        try:
            config[key]
        except KeyError:
            config[key] = defaults[key]
    return config

def stored_conf():
    db = Worker()
    db_config = db.get_full_config() 
    return defaults(db_config)
