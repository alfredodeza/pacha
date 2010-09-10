from subprocess import Popen, PIPE

def run_command(std, cmd):
    """Runs a command via Popen"""
    if std == "stderr":
        run = Popen(cmd, shell=True, stderr=PIPE)
        out = run.stderr.readlines()
    if std == "stdout":
        run = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out = run.stdout.readlines()
    return out
