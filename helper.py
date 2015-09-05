# helper file to include reuseable commands

from subprocess import Popen, PIPE
import os


def run(command, raw=False):
    """Runs command

    Args:
        command (str): A command string literal to be ran
        raw (bool): returns the raw standard error and output

    Returns:
        tuple: (returncode, stdout, stderr)

        returncode (int): the exit code
        stdout (list): the standard output of the process
        stderr (list): the standard error of the process
    """

    p = Popen(command.split(), stdout=PIPE, stdin=PIPE)
    (stdout, stderr) = p.communicate()

    if not raw:
        if stdout is not None:
            stdout = [line.strip() for line in stdout.splitlines()]

        if stderr is not None:
            stderr = [line.strip() for line in stderr.splitlines()]

    return (p.returncode, stdout, stderr)


def make_exe(path):
    "rxwr--r--"
    os.chmod(path, 0744)


def ln(source, destination):
    """Creates a soft link

    Args:
        source (str): the source of the symlink
        destination (str): the destination of the symlink

    Note:
        `f` forces the link the be create if one already exists
    """
    exit_code = run("ln -sf {0} {1}".format(source, destination))[0]
    return exit_code


def git_dir():
    stdout = run("git rev-parse --git-dir")[1]
    return stdout[0]


def top_dir():
    stdout = run("git rev-parse --show-toplevel")[1]
    return stdout[0]


class color(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NO_COLOR = '\033[0m'
