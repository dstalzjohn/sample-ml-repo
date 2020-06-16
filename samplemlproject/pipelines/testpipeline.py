from kedro.pipeline import Pipeline, node

from ccmlutils.procedures.defaulttest import defaulttest_node
from ccmlutils.utilities.experimentmanager import get_exp_data_node
from ccmlutils.utilities.metricutils import cal_pred_metrics_node, save_metrics_node
from ccmlutils.utilities.predictionutils import save_predictions_node


def get_test_nodes(exp_id_var: str = None, connection_arg: str = None):
    exp_node = node(
        get_exp_data_node,
        inputs=dict(
            exp_output_folder="params:experiment_path",
            exp_id=exp_id_var,
            connection_arg=connection_arg,
        ),
        outputs=dict(experiment="experiment", exp_path="exp_path"),
    )

    test_node = node(
        defaulttest_node,
        inputs=dict(experiment="experiment", test_set="data_test"),
        outputs=dict(predictions="predictions"),
    )

    set_name_node = node(
        lambda: dict(set_name="test"), inputs=dict(), outputs=dict(set_name="set_name")
    )

    save_node = node(
        save_predictions_node,
        inputs=dict(
            predictions="predictions",
            store_path="exp_path",
            filename="params:pred_filename",
            set_name="set_name",
        ),
        outputs=dict(),
    )

    metric_node = node(
        cal_pred_metrics_node,
        inputs=dict(predictions="predictions"),
        outputs=dict(metrics="metrics"),
    )

    metric_save_node = node(
        save_metrics_node,
        inputs=dict(
            metric="metrics",
            store_path="exp_path",
            yaml_filename="params:metric_yaml_file",
        ),
        outputs=dict(),
    )

    test_node_list = [
        exp_node,
        test_node,
        save_node,
        metric_node,
        metric_save_node,
        set_name_node,
    ]

    return test_node_list


def create_pipeline():

    test_node_list = get_test_nodes(
        exp_id_var="params:test_exp", connection_arg="params:dummy_arg"
    )
    return Pipeline(test_node_list)
