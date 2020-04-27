from typing import List

from keras.callbacks import Callback

from samplemlproject.utilities.gitutils import get_git_revision_hash, get_git_revision_of_module, NoGitHashAvailable
import yaml


class GitVersionCallback(Callback):

    def __init__(self, filepath, git_dirs: List[str] = [], git_modules: List[str] = []):
        super().__init__()
        self.filepath = filepath
        self.git_dirs: List[str] = [git_dirs] if type(git_dirs) is str else git_dirs
        self.git_modules: List[str] = [git_modules] if type(git_modules) is str else git_modules

    def on_train_begin(self, logs=None):
        output_versions = dict()

        for cur_dir in self.git_dirs:
            try:
                output_versions[cur_dir] = get_git_revision_hash(cur_dir)
            except NoGitHashAvailable:
                output_versions[cur_dir] = "NoVersionAvailable"

        for mod in self.git_modules:
            try:
                output_versions[mod] = get_git_revision_of_module(mod)
            except NoGitHashAvailable:
                output_versions[mod] = "NoVersionAvailable"

        with open(self.filepath, 'w') as outfile:
            yaml.dump(output_versions, outfile, default_flow_style=False)

