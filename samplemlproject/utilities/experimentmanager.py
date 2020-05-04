import os
from os.path import dirname
from typing import List, Tuple, Set, Dict
import pandas as pd

from samplemlproject.config.envconfig import get_short_id, get_pipeline_name, set_pipeline_name
from samplemlproject.utilities.experimentdata import ExperimentData


def get_exp_data_node(exp_output_folder: str, exp_id: str = None) -> Dict[str, ExperimentData]:
    exp_output_folder = dirname(exp_output_folder)
    if exp_id is None:
        exp_id = get_short_id()
    exp_data = get_exp_data(exp_output_folder, exp_id)
    return dict(experiment=exp_data,
                exp_path=exp_data.get_store_path())


def get_exp_data(exp_output_folder: str, exp_id: str):
    exp_manager = ExperimentManager(exp_output_folder)
    return exp_manager.get_exp_by_id(exp_id)


class ExperimentManager(object):

    def __init__(self, path):
        self.path = path
        self.experiments: List[ExperimentData] = \
            [ExperimentData(f.path) for f in os.scandir(path) if f.is_dir()]
        self.exp_dict = {exp.short_id: exp for exp in self.experiments}
        self.exp_dict.update({exp.run_id: exp for exp in self.experiments})

    def get_best_experiments(self,
                             metric_name: str,
                             mode: str,
                             number_of_exps: int) -> List[Tuple[str, ExperimentData]]:
        exp_list = self.experiments
        number_of_exps = min(number_of_exps, len(exp_list))
        value_exps = [(exp, exp.get_best_metric_value(metric_name, mode)) for exp in exp_list]
        reversed = True if mode == "max" else False
        value_exps = sorted(value_exps, reverse=reversed, key=lambda x: x[1].value)
        value_exps = value_exps[:number_of_exps]

        return [(f"{exp.short_id} - {value.value:0.2f}", exp) for exp, value in value_exps]

    def get_metrics(self) -> List[str]:
        metric_set: Set[str] = set()
        for cur_exp in self.experiments:
            metric_set.update(cur_exp.get_metrics())

        return sorted(list(metric_set))

    def get_experiments(self) -> List[ExperimentData]:
        return sorted(self.experiments, reverse=True, key=lambda x: x.run_id)

    def get_exp_by_id(self, exp_id: str) -> ExperimentData:
        if exp_id.lower() == "latest":
            ret_exp = sorted(self.experiments, reverse=True, key=lambda x: x.run_id)[0]
        else:
            ret_exp = self.exp_dict[exp_id]
        return ret_exp

    def get_visu_df(self, metric_name: str, exp_id_list: List[str]) -> pd.DataFrame:
        df = None
        for exp_id in exp_id_list:
            exp = self.get_exp_by_id(exp_id)
            if df is None:
                df = exp.get_log_for_metric(metric_name)
            else:
                df = pd.concat([df, exp.get_log_for_metric(metric_name)])

        return df
