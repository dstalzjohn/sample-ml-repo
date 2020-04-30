import os
from dataclasses import dataclass
from os.path import join
from typing import Tuple, List

import yaml
import pandas as pd
import numpy as np

from samplemlproject.config.envconfig import RUN_ID_KEY, SHORT_ID_KEY


class ModelNotFound(Exception):
    pass

def load_exp_info(exp_info_file) -> Tuple[str, str]:
    with open(exp_info_file, "r") as f:
        data = yaml.load(f)

    return data[RUN_ID_KEY], data[SHORT_ID_KEY]


def load_loggings(logging_file: str) -> pd.DataFrame:
    return pd.read_csv(logging_file)


@dataclass
class MetricValue(object):
    metric_name: str
    value: float
    epoch: int


class ExperimentData(object):

    def __init__(self, filepath: str, project_info_file="project_info.yml", train_log_file="train_logs.csv",
                 model_subfolder: str="models", epoch_formatting: str = "ep{epoch:03d}"):
        self.filepath = filepath
        self.project_info_file = project_info_file
        self.train_log_file = train_log_file
        self.run_id, self.short_id = load_exp_info(join(self.filepath, self.project_info_file))
        self.log_data: pd.DataFrame = load_loggings(join(self.filepath, self.train_log_file))
        self.model_subfolder: str = model_subfolder
        self.epoch_formatting: str = epoch_formatting

    def get_store_path(self) -> str:
        return self.filepath

    def get_metrics(self) -> List[str]:
        metrics = list(self.log_data.columns)
        metrics.remove("epoch")
        return metrics

    def get_log_for_metric(self, metric_name: str):
        series_epoch = self.log_data["epoch"]
        series_metrics = self.log_data[metric_name]
        series_name = pd.Series(data=[self.short_id] * len(series_epoch))
        df = pd.DataFrame({"epoch": series_epoch, metric_name: series_metrics, "name": series_name})

        return df

    def get_best_metric_value(self, metric_name: str, mode) -> MetricValue:
        """
        Returns the best value of the given metric according to the mode.
        :param metric_name: name of the metric
        :param mode: either 'min' or 'max'
        :return: MetricValue
        """
        series_epoch = self.log_data["epoch"]
        series_metrics = self.log_data[metric_name]
        if mode == "max":
            idx = np.argmax(series_metrics)
        elif mode == "min":
            idx = np.argmin(series_metrics)
        else:
            raise Exception(f"Mode is neither 'max' nor 'min' but {mode}")

        val = series_metrics[idx]
        epoch = series_epoch[idx]
        return MetricValue(metric_name=metric_name, value=val, epoch=epoch)

    def get_model_path(self, epoch: int = None) -> str:
        """
        Get the model path for the desired model.
        :param epoch: epoch as int if not given the latest is returned
        """
        model_path = join(self.filepath, self.model_subfolder)
        model_files: List[str] = sorted([f.path for f in os.scandir(model_path) if f.is_file()])
        ret_model = None
        if len(model_files) == 0:
            raise ModelNotFound(f"No model found for this experiment: {self.short_id}")

        if epoch is None:
            ret_model = model_files[-1]
        else:
            ep_str = self.epoch_formatting.format(epoch)
            for mf in model_files:
                if ep_str in mf:
                    ret_model = mf

        if ret_model is None:
            raise ModelNotFound(f"Model from epoch: {epoch} not found in exp: {self.short_id}")

        return ret_model



if __name__ == '__main__':
    p = "/Users/djohn/Projects/01_general/01_repos/sample-ml-project/experiment_outputs/2020-04-28T12.43.31.264Z-id_njs3"
    exp = ExperimentData(p)
    df = exp.get_log_for_metric("val_accuracy")
    mv = exp.get_best_metric_value("loss", "min")


