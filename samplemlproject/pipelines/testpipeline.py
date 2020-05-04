from kedro.pipeline import Pipeline, node

from samplemlproject.procedures.defaulttest import defaulttest_node
from samplemlproject.utilities.experimentmanager import get_exp_data_node
from samplemlproject.utilities.metricutils import cal_pred_metrics, cal_pred_metrics_node, save_metrics_node
from samplemlproject.utilities.predictionutils import save_predictions_node


def get_test_nodes(exp_id_var: str = None, connection_arg: str = None):
    exp_node = node(
        get_exp_data_node,
        inputs=dict(exp_output_folder="params:experiment_path", exp_id=exp_id_var),
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

    test_node_list = [
        exp_node,
        test_node,
        save_node,
        metric_node,
        metric_save_node,
    ]

    return test_node_list

def create_pipeline():

    test_node_list = get_test_nodes(exp_id_var="params:test_exp")
    return Pipeline(
        test_node_list
    )
