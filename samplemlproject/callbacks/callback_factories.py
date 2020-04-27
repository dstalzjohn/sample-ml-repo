from pathlib import Path

from keras.callbacks.callbacks import ModelCheckpoint

from samplemlproject.config.envconfig import get_run_id, RUN_ID_KEY


def model_callback_factory(filepath: str, *args, **kwargs):
    filepath = filepath.replace("$" + RUN_ID_KEY, get_run_id())
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    return ModelCheckpoint(filepath=filepath, *args, **kwargs)
