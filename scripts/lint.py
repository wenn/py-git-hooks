#!/usr/bin/python
# Please be aware that this script will be ran in the context of the actual hook located in .git/hooks/


import os
import sys

import flake8.hooks

import git_hooks.helper as helper


def python_files():
    '''filter file absolute paths that have indexed changes

    Yields:
        str: file path
    '''
    _, cached_files, _ = helper.run("git diff-index --cached --name-only --diff-filter=ACMRTUXB HEAD")

    paths = [os.path.join(helper.top_dir(), f) for f in cached_files]
    files_modified = [path for path in paths if os.path.isfile(path)]

    python_files = []
    for path in files_modified:
        name, ext = os.path.splitext(path)
        if ext == '.py':
            python_files.append(path)

    return python_files


def has_python_files():
    return bool(python_files())


def lint():
    '''runs on the default settings for lint, will scan only indexed files

    Note:
        Uses config from ./setup.cfg

    Returns:
        int: total errors reported
    '''
    return flake8.hooks.git_hook(strict=True)


if __name__ == '__main__':

    if not has_python_files():
        sys.exit(0)

    errors_count = lint()

    if errors_count != 0:
        print "{0}{1} lint errors found, please correct them.{2}".format(
            helper.color.RED, errors_count, helper.color.NO_COLOR)
        sys.exit(1)
