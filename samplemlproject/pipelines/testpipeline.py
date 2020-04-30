from kedro.pipeline import Pipeline, node

from samplemlproject.procedures.defaulttest import defaulttest_node
from samplemlproject.utilities.experimentmanager import get_exp_data_node
from samplemlproject.utilities.metricutils import cal_pred_metrics, cal_pred_metrics_node, save_metrics_node
from samplemlproject.utilities.predictionutils import save_predictions_node


def create_pipeline():

    exp_node = node(
        get_exp_data_node,
        inputs=dict(exp_output_folder="params:experiment_path", exp_id="params:test_exp"),
        outputs=dict(experiment="experiment", exp_path="exp_path"),
    )

    test_node = node(
        defaulttest_node,
        inputs=dict(experiment="experiment", test_set="data_test"),
        outputs=dict(predictions="predictions"),
    )

    save_node = node(
        save_predictions_node,
        inputs=dict(predictions="predictions", store_path="exp_path",
                    parq_filename="params:parq_pred_filename", yml_filename="params:yaml_pred_filename"),
        outputs=dict(),
    )

    metric_node = node(
        cal_pred_metrics_node,
        inputs=dict(predictions="predictions"),
        outputs=dict(metrics="metrics"),
    )

    metric_save_node = node(
        save_metrics_node,
        inputs=dict(metric="metrics", store_path="exp_path", yaml_filename="params:metric_yaml_file"),
        outputs=dict(),
    )

    return Pipeline(
        [
            exp_node,
            test_node,
            save_node,
            metric_node,
            metric_save_node,
        ]
    )
