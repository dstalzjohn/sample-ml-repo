import os
from typing import Dict, Any, List, Tuple
import altair

import streamlit as st
import pandas as pd
from samplemlproject.utilities.experimentdata import ExperimentData

# the default metrics are shown as true
default_metrics = ["val_accuracy"]


def get_best_experiments(exp_list: List[ExperimentData],
                         metric_name: str,
                         mode: str,
                         number_of_exps: int) -> List[Tuple[str, ExperimentData]]:
    number_of_exps = min(number_of_exps, len(exp_list))
    value_exps = [(exp, exp.get_best_metric_value(metric_name, mode)) for exp in exp_list]
    reversed = True if mode == "max" else False
    value_exps = sorted(value_exps, reverse=reversed, key=lambda x: x[1].value)
    value_exps = value_exps[:number_of_exps]

    return [(f"{exp.short_id} - {value.value:0.2f}", exp) for exp, value in value_exps]


def generate_chart(source, metric):
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = altair.selection(type='single', nearest=True, on='mouseover',
                            fields=['epoch'], empty='none')

    line = altair.Chart(source).mark_line().encode(
        x='epoch',
        y=met,
        color='name',
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = altair.Chart(source).mark_point().encode(
        x='epoch',
        opacity=altair.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=altair.condition(nearest, altair.value(1), altair.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=altair.condition(nearest, metric + ':Q', altair.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = altair.Chart(source).mark_rule(color='gray').encode(
        x='epoch:Q',
    ).transform_filter(
        nearest
    )

    final = altair.layer(
        line, selectors, points, rules, text
    ).properties(
        width=600, height=400
    )

    return final


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

st.sidebar.markdown("Best Experiments")
best_metric = st.sidebar.selectbox("Metric", options=list(metric_set))
mode = st.sidebar.selectbox("Mode", options=['min', 'max'])
best_exps = get_best_experiments(experiments, best_metric, mode, 3)
for text, exp in best_exps:
    st.sidebar.checkbox(text)

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
    chart_data = generate_chart(chart_log_dict[met], met)
    st.write(chart_data)




