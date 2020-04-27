from pathlib import Path

from keras.callbacks.callbacks import ModelCheckpoint, CSVLogger

from samplemlproject.config.envconfig import replace_id_keys


def model_callback_factory(filepath: str, *args, **kwargs):
    filepath = replace_id_keys(filepath)
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    return ModelCheckpoint(filepath=filepath, *args, **kwargs)


def logging_callback_output(filename: str, *args, **kwargs):
    filename = replace_id_keys(filename)
    p = Path(filename)
    p.parent.mkdir(parents=True, exist_ok=True)
    return CSVLogger(filename=filename, *args, **kwargs)
