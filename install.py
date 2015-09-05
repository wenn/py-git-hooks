import os
import sys
import helper


class BaseHooks(object):

    HOOK_DIR = None
    HOOKS = [
        "pre-commit"
    ]

    @classmethod
    def install(cls):
        """Creates hook symlinks from HOOK_DIR to .git/hooks"""

        if cls.HOOK_DIR is None:
            raise Exception("HOOK_DIR can not be None")

        paths = cls.get_paths()

        for (source, destination) in paths:
            if (os.path.isfile(source)):
                helper.make_exe(source)
                sys.exit(helper.ln(source, destination))

    @classmethod
    def get_paths(cls):
        """Builds absolute paths for hook symlink source and destination

        Returns:
            list of tuples: [(source, destination)]

            source (str): absolute path of the hook's source
            destination (str): absolute path of the hook's destination
        """

        join = os.path.join
        hook_path = join(helper.top_dir(), cls.HOOK_DIR)
        git_path = helper.git_dir() + "/hooks"
        git_path = join(helper.top_dir(), git_path)

        return [(join(hook_path, hook), join(git_path, hook)) for hook in cls.HOOKS]


class PythonHooks(BaseHooks):

    HOOK_DIR = "git_hooks/hooks"


if __name__ == '__main__':
    PythonHooks.install()
