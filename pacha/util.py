from subprocess import Popen, PIPE


# Easy way to implement colors in the terminal
# for actual use, you need to always end with ENDC
# For red text: 
# print RED+"a red string"+ENDS

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDS = '\033[0m'


def run_command(std, cmd):
    """Runs a command via Popen"""
    if std == "stderr":
        run = Popen(cmd, shell=True, stderr=PIPE)
        out = run.stderr.readlines()
    if std == "stdout":
        run = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out = run.stdout.readlines()
    return out

