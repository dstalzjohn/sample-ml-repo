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
        return self.log_data[metric_name]


