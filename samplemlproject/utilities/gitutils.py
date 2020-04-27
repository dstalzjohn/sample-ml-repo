import os
import subprocess
from importlib import import_module


class NoGitHashAvailable(Exception):
    pass


def get_git_revision_hash(path: str = "."):
    try:
        git_commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=path)
    except:
        raise NoGitHashAvailable(f"Folder seems to be no git repo: {path}")

    return str(git_commit_hash)


def get_module_dir(module_name: str):
    mod = import_module(module_name)
    mod_dir = os.path.dirname(mod.__file__)
    return mod_dir


def get_git_revision_of_module(module_name: str):
    mod_dir = get_module_dir(module_name)
    git_commit_hash = get_git_revision_hash(mod_dir)
    return git_commit_hash
