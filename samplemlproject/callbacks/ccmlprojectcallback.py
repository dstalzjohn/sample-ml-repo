from os.path import join
from typing import List, Optional

import yaml
from keras.callbacks import Callback, CSVLogger

from samplemlproject.callbacks.gitversioncallback import produce_git_version_yaml
from samplemlproject.config.envconfig import get_run_id, get_short_id, RUN_ID_KEY, SHORT_ID_KEY


def produce_project_info(filepath: str):
    out_dict = {RUN_ID_KEY: get_run_id(), SHORT_ID_KEY: get_short_id()}
    with open(filepath, 'w') as outfile:
        yaml.dump(out_dict, outfile, default_flow_style=False)


class CCMLProjectCallback(Callback):

    def __init__(self, log_path: str, git_dirs: List[str] = [], git_modules: List[str] = [],
                 git_version_filename: str = "git_versions.yml",
                 project_info_filename: str = "project_info.yml",
                 enable_train_logging: bool = True,
                 train_log_file: str = "train_logs.csv"):
        super().__init__()
        self.git_dirs: List[str] = [git_dirs] if type(git_dirs) is str else git_dirs
        self.git_modules: List[str] = [git_modules] if type(git_modules) is str else git_modules
        self.log_path = log_path
        self.git_version_filename: str = git_version_filename
        self.project_info_filename: str = project_info_filename
        self.log_callback: Optional[Callback] = None
        if enable_train_logging:
            self.log_callback = CSVLogger(filename=join(log_path, train_log_file))

    def set_model(self, model):
        super().set_model(model)
        if self.log_callback is not None:
            self.log_callback.set_model(model)

    def on_train_begin(self, logs=None):
        produce_git_version_yaml(join(self.log_path, self.git_version_filename), self.git_dirs, self.git_modules)
        produce_project_info(join(self.log_path, self.project_info_filename))
        if self.log_callback is not None:
            self.log_callback.on_train_begin(logs=logs)

    def on_epoch_end(self, epoch, logs=None):
        if self.log_callback is not None:
            self.log_callback.on_epoch_end(epoch, logs=logs)

    def on_train_end(self, logs=None):
        if self.log_callback is not None:
            self.log_callback.on_train_end(logs=logs)
