from kedro.pipeline import Pipeline, node

from ccmlutils.procedures.defaulttest import defaulttest_node
from ccmlutils.utilities.experimentmanager import get_exp_data_node
from ccmlutils.utilities.metricutils import cal_pred_metrics_node, save_metrics_node
from ccmlutils.utilities.predictionutils import save_predictions_node


def get_test_nodes(set_to_test: str, exp_id_var: str = None, connection_arg: str = None):
    exp_node = node(
        get_exp_data_node,
        inputs=dict(
            exp_output_folder="params:experiment_path",
            exp_id=exp_id_var,
            connection_arg=connection_arg,
        ),
        outputs=dict(experiment="experiment" + set_to_test, exp_path="exp_path" + set_to_test),
    )

    test_node = node(
        defaulttest_node,
        inputs=dict(experiment="experiment" + set_to_test, test_set=set_to_test),
        outputs=dict(predictions="predictions" + set_to_test),
    )

    set_name_node = \
        node(lambda:dict(set_name=set_to_test[5:]), inputs=None, outputs=dict(set_name="set_name" + set_to_test))


    save_node = node(
        save_predictions_node,
        inputs=dict(
            predictions="predictions" + set_to_test,
            store_path="exp_path" + set_to_test,
            filename="params:pred_filename",
            set_name="set_name" + set_to_test,
        ),
        outputs=dict(),
    )

    metric_node = node(
        cal_pred_metrics_node,
        inputs=dict(predictions="predictions" + set_to_test),
        outputs=dict(metrics="metrics" + set_to_test),
    )

    metric_save_node = node(
        save_metrics_node,
        inputs=dict(
            metric="metrics" + set_to_test,
            store_path="exp_path" + set_to_test,
            yaml_filename="params:metric_yaml_file",
            set_name="set_name" + set_to_test
        ),
        outputs=dict(),
    )

    test_node_list = [
        exp_node,
        test_node,
        save_node,
        metric_node,
        metric_save_node,
        set_name_node
    ]

    return test_node_list


def create_pipeline():

    test_node_list = get_test_nodes(
        exp_id_var="params:test_exp", connection_arg="params:dummy_arg", set_to_test="data_test"
    )
    validation_node_list = get_test_nodes(
        exp_id_var="params:test_exp", connection_arg="params:dummy_arg", set_to_test="data_validation"
    )
    train_node_list = get_test_nodes(
        exp_id_var="params:test_exp", connection_arg="params:dummy_arg", set_to_test="data_train_eval"
    )
    return Pipeline(test_node_list + validation_node_list + train_node_list)