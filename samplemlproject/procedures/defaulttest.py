from dataclasses import dataclass
from typing import List, Dict, Any

from keras.models import load_model, Model

from samplemlproject.utilities.experimentdata import ExperimentData
import numpy as np
import pandas as pd


@dataclass
class PredictionContainer(object):
    filename: str
    class_idx: int
    prediction: np.ndarray

    def get_pred_list(self):
        return [float(x) for x in self.prediction.tolist()]

    def get_pred_dict(self) -> dict:
        out_dict = dict()
        for idx, value in enumerate(self.prediction):
            out_dict[f"pred_{idx:04d}"] = value

        return out_dict

    def get_default_dict(self) -> dict:
        out_dict = dict(filename=self.filename, class_idx=self.class_idx)
        out_dict["prediction"] = self.get_pred_list()
        return out_dict

    def get_df_dict(self) -> dict:
        out_dict = dict(filename=self.filename, class_idx=self.class_idx)
        out_dict.update(self.get_pred_dict())
        return out_dict


class Predictions(object):

    def __init__(self, preds: List[PredictionContainer], class_idxs: Dict[str, int]):
        self.preds = preds
        self.class_idxs = class_idxs

    def get_list_data(self) -> List[dict]:
        out_list: List[dict] = [x.get_default_dict() for x in self.preds]
        return out_list

    def get_df_data(self) -> pd.DataFrame:
        df_list: List[dict] = [x.get_df_dict() for x in self.preds]
        df = pd.DataFrame(df_list)
        return df


def prediction_factory(preds: List[Any],
                       filenames: List[str],
                       classes: List[int],
                       class_indices: Dict[str, int]) -> Predictions:
    pred_list = list()
    for pred, filename, cl in zip(preds, filenames, classes):
        pred_list.append(PredictionContainer(filename=filename, class_idx=cl, prediction=pred))

    return Predictions(pred_list, class_indices)


def defaulttest(test_set, experiment: ExperimentData) -> Predictions:
    model_path = experiment.get_model_path()
    model: Model = load_model(model_path)
    preds_output = model.predict_generator(test_set)
    filenames = test_set.filenames
    class_indices = test_set.class_indices
    classes = test_set.classes
    predictions: Predictions = prediction_factory(preds_output, filenames, classes, class_indices)

    pred_list = predictions.get_list_data()
    pred_df = predictions.get_df_data()

    return predictions


def defaulttest_node(test_set, experiment: ExperimentData) -> Dict[str, Predictions]:
    return dict(predictions=defaulttest(test_set, experiment))

