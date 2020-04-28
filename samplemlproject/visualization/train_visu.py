import os
from typing import Dict, Any
import altair

import streamlit as st
import pandas as pd
from samplemlproject.utilities.experimentdata import ExperimentData

# the default metrics are shown as true
default_metrics = ["val_accuracy"]

st.title("Monitor your trainings!")
folder = "experiment_outputs"
subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]
experiments = []
metric_set = set()
for sf in subfolders:
    cur_exp = ExperimentData(sf)
    metric_set.update(cur_exp.get_metrics())
    experiments.append(cur_exp)

st.sidebar.markdown("Visualized Metrics")
visualized_metrics = list()
for met in metric_set:
    if st.sidebar.checkbox(met, value=bool(met in default_metrics)):
        visualized_metrics.append(met)

st.sidebar.markdown("Found Experiments")
checked_experiments = []
for exp in experiments:
    if st.sidebar.checkbox(f"ID: {exp.short_id} - TS: {exp.run_id}", value=True):
        checked_experiments.append(exp)
exp: ExperimentData
chart_log_dict: Dict[str, Any] = dict()
for met in visualized_metrics:
    for exp in checked_experiments:
        if met not in chart_log_dict:
            chart_log_dict[met] = exp.get_log_for_metric(met)
        else:
            chart_log_dict[met] = pd.concat([chart_log_dict[met], exp.get_log_for_metric(met)])
    if met not in chart_log_dict:
        continue
    chart_data = altair.Chart(chart_log_dict[met]).mark_line().encode(
        x='epoch',
        y=met,
        color='name',
    )
    st.write(chart_data)




