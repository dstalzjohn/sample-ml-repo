from kedro.pipeline import Pipeline, node

from samplemlproject.procedures.defaulttest import defaulttest_node
from samplemlproject.utilities.experimentmanager import get_exp_data_node


def create_pipeline():

    exp_node = node(
        get_exp_data_node,
        inputs=dict(exp_output_folder="params:exp_output_folder", exp_id="params:test_exp"),
        outputs=dict(experiment="experiment"),
    )

    test_node = node(
        defaulttest_node,
        inputs=dict(experiment="experiment", test_set="data_test"),
        outputs=dict(results="results"),
    )

    return Pipeline(
        [
            exp_node,
            test_node
        ]
    )
