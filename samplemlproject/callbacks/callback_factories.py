from os.path import join
from pathlib import Path

from keras.callbacks.callbacks import ModelCheckpoint, CSVLogger

from samplemlproject.callbacks.ccmlprojectcallback import CCMLProjectCallback
from samplemlproject.callbacks.gitversioncallback import GitVersionCallback
from samplemlproject.config.envconfig import replace_id_keys


def subs_path_and_create_folder(filepath: str) -> str:
    filepath = replace_id_keys(filepath)
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    return filepath


def model_callback_factory(exp_path: str, model_subfolder: str, *args, **kwargs):
    filepath = join(exp_path, model_subfolder)
    filepath = subs_path_and_create_folder(filepath)
    return ModelCheckpoint(filepath=filepath, *args, **kwargs)


def logging_callback_output(filename: str, *args, **kwargs):
    filename = subs_path_and_create_folder(filename)
    return CSVLogger(filename=filename, *args, **kwargs)


def git_callback_factory(filepath: str, *args, **kwargs):
    filepath = subs_path_and_create_folder(filepath)
    return GitVersionCallback(filepath, *args, **kwargs)


def ccmlproject_callback_factory(filepath: str, *args, **kwargs):
    filepath = subs_path_and_create_folder(filepath)
    return CCMLProjectCallback(filepath, *args, **kwargs)
