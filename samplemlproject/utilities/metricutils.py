from dataclasses import dataclass
from os.path import join
from typing import Dict

import numpy as np
import yaml

from sklearn.metrics import accuracy_score, confusion_matrix

from samplemlproject.callbacks.callback_factories import subs_path_and_create_folder
from samplemlproject.utilities.predictionutils import Predictions


@dataclass
class Metrics(object):
    accuracy: float
    confusion_mat: np.ndarray

    def save(self, filepath):
        d = dict(accuracy=self.accuracy, confusion_mat=self.confusion_mat.tolist())
        with open(filepath, "w") as f:
            yaml.dump(d, f)


def load_metrics(filepath: str) -> Metrics:
    with open(filepath, "r") as f:
        data = yaml.load(f)

    return Metrics(accuracy=data["accuracy"],
                   confusion_mat=np.array(data["confusion_mat"]))


def cal_pred_metrics(predictions: Predictions) -> Metrics:
    target_idxs, pred_idxs = predictions.get_class_and_pred_idxs()

    acc_score = float(accuracy_score(target_idxs, pred_idxs))
    conf_mat = confusion_matrix(target_idxs, pred_idxs)

    mets = Metrics(accuracy=acc_score, confusion_mat=conf_mat)

    return mets


def cal_pred_metrics_node(predictions: Predictions) -> Dict[str, Metrics]:
    return dict(metrics=cal_pred_metrics(predictions))


def save_metrics_node(metric: Metrics, store_path: str, yaml_filename: str):
    filepath = subs_path_and_create_folder(join(store_path, yaml_filename))
    metric.save(filepath)
    return dict()
