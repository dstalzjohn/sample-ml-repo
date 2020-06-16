from typing import List

import streamlit as st

from ccmlutils.utilities.chartutils import generate_chart
from ccmlutils.utilities.experimentdata import ExperimentData

# the default metrics are shown as true
from ccmlutils.utilities.experimentmanager import ExperimentManager

# Define your parameters
default_metrics = ["val_accuracy"]
folder: str = "experiment_outputs"
number_of_preselected_exps: int = 2
number_of_preselected_best_exps: int = 1
number_of_best_exps_shown: int = 3

exp: ExperimentData
exp_manager = ExperimentManager(folder)
metric_list: List[str] = exp_manager.get_metrics()

# Built Sidebar
st.sidebar.markdown("Visualized Metrics")
visualized_metrics = list()
for met in metric_list:
    if st.sidebar.checkbox(met, value=bool(met in default_metrics)):
        visualized_metrics.append(met)

st.sidebar.markdown("Best Experiments")
best_metric = st.sidebar.selectbox("Metric", options=list(metric_list))
mode = st.sidebar.selectbox("Mode", options=["min", "max"])
best_exps = exp_manager.get_best_experiments(
    best_metric, mode, number_of_best_exps_shown
)
checked_experiments = set()
for idx, (text, exp) in enumerate(best_exps):
    if st.sidebar.checkbox(text, value=idx < number_of_preselected_best_exps):
        checked_experiments.add(exp.short_id)

st.sidebar.markdown("Found Experiments")

for idx, exp in enumerate(exp_manager.get_experiments()):
    if st.sidebar.checkbox(
        f"ID: {exp.short_id} - TS: {exp.run_id}", value=idx < number_of_preselected_exps
    ):
        checked_experiments.add(exp.short_id)

# Visualize in the center
for met in visualized_metrics:
    cur_df = exp_manager.get_visu_df(met, list(checked_experiments))
    chart_data = generate_chart(cur_df, met)
    st.write(chart_data)
