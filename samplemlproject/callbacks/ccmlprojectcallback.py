from os.path import join
from typing import List

import yaml
from keras.callbacks import Callback

from samplemlproject.callbacks.gitversioncallback import produce_git_version_yaml
from samplemlproject.config.envconfig import get_run_id, get_short_id


def produce_project_info(filepath: str):
    out_dict = dict(run_id=get_run_id(), short_id=get_short_id())
    with open(filepath, 'w') as outfile:
        yaml.dump(out_dict, outfile, default_flow_style=False)


class CCMLProjectCallback(Callback):

    def __init__(self, log_path: str, git_dirs: List[str] = [], git_modules: List[str] = [],
                 git_version_filename: str = "git_versions.yml",
                 project_info_filename: str = "project_info.yml"):
        super().__init__()
        self.git_dirs: List[str] = [git_dirs] if type(git_dirs) is str else git_dirs
        self.git_modules: List[str] = [git_modules] if type(git_modules) is str else git_modules
        self.log_path = log_path
        self.git_version_filename: str = git_version_filename
        self.project_info_filename: str = project_info_filename

    def on_train_begin(self, logs=None):
        produce_git_version_yaml(join(self.log_path, self.git_version_filename), self.git_dirs, self.git_modules)
        produce_project_info(join(self.log_path, self.project_info_filename))
