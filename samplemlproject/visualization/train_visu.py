import os
from collections import defaultdict
from typing import Dict, Any

import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from samplemlproject.utilities.experimentdata import ExperimentData

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
exp: ExperimentData
chart_log_dict: Dict[str, dict] = defaultdict(dict)
for exp in experiments:
    for met in visualized_metrics:
        if st.sidebar.checkbox(f"ID: {exp.short_id} - TS: {exp.run_id}", value=True):
            chart_log_dict[met][exp.short_id] = list(exp.get_log_for_metric(met))

st.write(chart_log_dict)

chart_data = pd.DataFrame(
   np.random.randn(20, 3),
   columns=['a', 'b', 'c'])

st.line_chart(chart_data)

