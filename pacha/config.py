from guachi import ConfigMapper

INI_MAPPINGS = {
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

DEFAULT_MAPPINGS = {
        'frequency': 60,
        'master': 'False',
        'host': 'localhost',
        'ssh_user': 'root',
        'ssh_port': 22,
        'hosts_path': '/opt/pacha',
        'hg_autocorrect': 'True',
        'log_enable': 'False',
        'log_path': 'False',
        'log_level': 'DEBUG',
        'log_format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        'log_datefmt' : '%H:%M:%S'
        }


def set_mappings(DB_FILE):
    """Sets the INI and default mappings in the database"""
    conf = ConfigMapper(DB_FILE)
    conf.set_default_options(DEFAULT_MAPPINGS)
    conf.set_ini_options(INI_MAPPINGS)

