from os.path import join
from typing import Dict, Any, Optional, Tuple, List

from click import Path
from kedro.io import AbstractDataSet

from samplemlproject.datasets.imagedata import get_image_flow_directory_generator


class ImageFlowDataset(AbstractDataSet):

    def __init__(self, filepath: str,
                       batch_size: int,
                       sub_dir: Optional[str] = None,
                       target_size: Optional[Tuple[int, int]] = None,
                       rescale: Optional[float] = None,
                       classes: Optional[List[str]] = None,):
        super().__init__()
        self.file_path = filepath
        self.batch_size = batch_size
        self.sub_dir = sub_dir
        self.target_size = target_size
        self.rescale = rescale
        self.classes = classes

    def _load(self) -> Any:
        return get_image_flow_directory_generator(
            self.file_path,
            self.batch_size,
            self.sub_dir,
            self.target_size,
            self.rescale,
            self.classes
        )

    def _save(self, data: Any) -> None:
        pass

    def _describe(self) -> Dict[str, Any]:
        return dict(
            file_path=self.file_path,
            batch_size=self.batch_size,
            sub_dir=self.sub_dir,
            target_size=self.target_size,
            rescale=self.rescale,
            classes=self.classes,
        )

    def _exists(self) -> bool:
        target_folder = self.file_path if self.sub_dir is None else join(self.file_path, self.sub_dir)
        return Path(target_folder).exists()
