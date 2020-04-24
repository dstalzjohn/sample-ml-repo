from os.path import join
from typing import Dict, Tuple, List, Optional

import keras.preprocessing.image as keras_image


def get_image_flow_directory_generator(filepath: str,
                                       batch_size: int,
                                       sub_dir: Optional[str] = None,
                                       target_size: Optional[Tuple[int, int]] = None,
                                       rescale: Optional[float] = None,
                                       classes: Optional[List[str]] = None,
                                       ) -> Dict:
    """
    Creates an image dataset for training or testing
    :param filepath: path where the images are located
    :param batch_size: batch size for the later application
    :param sub_dir: can be used to differentiate between `test` and `training` folders
    :param target_size: when given the images are scaled to the given size
    :param rescale: scale value for each pixel (e.g. 1/255.)
    :param classes: List of classes which should be used (folder names), if not given, everything is used
    :return:
    """
    image_generator = keras_image.ImageDataGenerator(rescale=rescale)
    # switch between categorical and binary if exactyl two classes are given
    # if no class list is given, categorical is used
    class_mode = 'categorical'
    if classes is not None and len(classes) == 2:
        class_mode = 'binary'

    target_dir = filepath if sub_dir is None else join(filepath, sub_dir)
    image_set = image_generator.flow_from_directory(target_dir,
                                                    target_size=target_size,
                                                    batch_size=batch_size,
                                                    class_mode=class_mode,
                                                    classes=classes)

    return image_set
