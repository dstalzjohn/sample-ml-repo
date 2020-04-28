from os.path import join
from typing import Tuple, List

import yaml
import pandas as pd

from samplemlproject.config.envconfig import RUN_ID_KEY, SHORT_ID_KEY


def load_exp_info(exp_info_file) -> Tuple[str, str]:
    with open(exp_info_file, "r") as f:
        data = yaml.load(f)

    return data[RUN_ID_KEY], data[SHORT_ID_KEY]


def load_loggings(logging_file: str) -> pd.DataFrame:
    return pd.read_csv(logging_file)


class ExperimentData(object):

    def __init__(self, filepath: str, project_info_file="project_info.yml", train_log_file="train_logs.csv"):
        self.filepath = filepath
        self.project_info_file = project_info_file
        self.train_log_file = train_log_file
        self.run_id, self.short_id = load_exp_info(join(self.filepath, self.project_info_file))
        self.log_data: pd.DataFrame = load_loggings(join(self.filepath, self.train_log_file))

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


if __name__ == '__main__':
    p = "/Users/djohn/Projects/01_general/01_repos/sample-ml-project/experiment_outputs/2020-04-28T12.43.31.264Z-id_njs3"
    exp = ExperimentData(p)
    df = exp.get_log_for_metric("val_accuracy")


