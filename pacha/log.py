from logging import getLogger

## Set logger objects for all modules
daemon          = getLogger('pacha.daemon')
database        = getLogger('pacha.database')
hg              = getLogger('pacha.hg')
host            = getLogger('pacha.host')
permissions     = getLogger('pacha.permissions')
