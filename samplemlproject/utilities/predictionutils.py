from dataclasses import dataclass
from os.path import join
from typing import Optional, List, Dict, Any, Tuple

import fastparquet
import numpy as np
import pandas as pd
import yaml

from samplemlproject.utilities.factoryutils import subs_path_and_create_folder


@dataclass
class PredictionContainer(object):
    filename: str
    class_idx: int
    class_name: Optional[str]
    prediction: np.ndarray

    def get_pred_list(self):
        return [float(x) for x in self.prediction.tolist()]

    def get_pred_dict(self) -> dict:
        out_dict = dict()
        for idx, value in enumerate(self.prediction):
            out_dict[f"pred_{idx:04d}"] = value

        return out_dict

    def get_default_dict(self) -> dict:
        out_dict = dict(filename=self.filename, class_idx=int(self.class_idx))
        out_dict["prediction"] = self.get_pred_list()
        return out_dict

    def get_df_dict(self) -> dict:
        out_dict = dict(filename=self.filename, class_idx=self.class_idx, class_name=self.class_name)
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

    def get_class_and_pred_idxs(self) -> Tuple[np.ndarray, np.ndarray]:
        cur_df = self.get_df_data()
        target_idxs = np.round(cur_df["class_idx"])
        pred_cols = sorted([c for c in cur_df.columns if c.startswith("pred_")])

        if len(pred_cols) == 1:
            pred_idxs = np.round(cur_df["pred_0000"])
        elif len(pred_cols) > 1:
            pred_idxs = cur_df[pred_cols].idxmax(axis=1)
            pred_idxs = pred_idxs.apply(lambda x: int(x[5:]))
        else:
            raise Exception("No prediction column available!")
        return target_idxs, pred_idxs

    def save_df(self, filepath: str):
        fastparquet.write(filepath, self.get_df_data())

    def save_yaml(self, filepath: str):
        out_dict = dict(class_idxs=self.class_idxs, predictions=self.get_list_data())
        with open(filepath, "w") as fp:
            yaml.dump(out_dict, fp)


def prediction_factory(preds: List[Any],
                       filenames: List[str],
                       classes: List[int],
                       class_indices: Dict[str, int]) -> Predictions:
    pred_list = list()
    rev_class_idxs = {v: k for k, v in class_indices.items()}
    for pred, filename, cl in zip(preds, filenames, classes):
        pred_list.append(PredictionContainer(filename=filename,
                                             class_idx=cl,
                                             prediction=pred,
                                             class_name=rev_class_idxs[cl]))

    return Predictions(pred_list, class_indices)


def save_predictions(predictions: Predictions,
                     store_path: str,
                     parq_filename: str = None,
                     yml_filename: str = None):
    if parq_filename is not None:
        predictions.save_df(join(store_path, parq_filename))

    if yml_filename is not None:
        predictions.save_yaml(join(store_path, yml_filename))


def save_predictions_node(predictions: Predictions,
                          store_path: str,
                          parq_filename: str = None,
                          yml_filename: str = None):
    store_path = subs_path_and_create_folder(store_path)
    save_predictions(predictions,
                     store_path,
                     parq_filename,
                     yml_filename)
    return dict()
