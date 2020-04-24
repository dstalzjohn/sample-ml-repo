from pathlib import Path
from typing import Optional, Dict, Any

from keras import Model
from keras.models import load_model
from kedro.io import AbstractVersionedDataSet, Version, DataSetError
import tensorflow as tf


class KerasModelDataset(AbstractVersionedDataSet):

    def __init__(self,
                 filepath: str,
                 version: Optional[Version] = None):
        super().__init__(filepath=Path(filepath), version=version)

    def _load(self) -> Model:
        load_path = Path(self._get_load_path())
        with tf.device("/CPU:0"):
            model = load_model(str(load_path))

        return model

    def _save(self, model: Model) -> None:
        save_path = Path(self._get_save_path())
        save_path.parent.mkdir(parents=True, exist_ok=True)
        model.save(str(save_path))

    def _exists(self) -> bool:
        try:
            path = self._get_load_path()
        except DataSetError:
            return False
        return Path(path).exists()

    def _describe(self) -> Dict[str, Any]:
        return dict(
            filepath=self._filepath,
            version=self._version,
        )


