from kedro.pipeline import Pipeline, node

from ccmlutils.callbacks.createcallbacks import create_callbacks_node
from ccmlutils.procedures.defaulttrain import fit_generator

from samplemlproject.models.simplemodel import get_simple_model
from samplemlproject.pipelines.testpipeline import get_test_nodes
from ccmlutils.utilities.factoryutils import init_object


def get_train_nodes():

    model_node = node(
        get_simple_model,
        inputs=dict(
            input_shape="params:input_shape", output_classes="params:n_classes"
        ),
        outputs=dict(model="model"),
    )

    optimizer_node = node(
        init_object, inputs=["params:optimizer"], outputs="optimizer",
    )

    # compile_node = node(
    #     compile_model,
    #     inputs=dict(model="model", output_classes_count="params:n_classes",
    #                 optimizer="optimizer"),
    #     outputs=dict(compiled_model="compiled_model"),
    # )

    callback_node = node(
        create_callbacks_node,
        inputs=["params:callbacks"],
        outputs=dict(callbacks="init_callbacks"),
    )

    train_node = node(
        fit_generator,
        inputs=dict(
            epochs="params:epochs",
            model="model",
            optimizer="optimizer",
            train_set="data_train",
            validation_set="data_validation",
            callbacks="init_callbacks",
            loss="params:loss",
        ),
        outputs=dict(history="history"),
    )

    return [model_node, optimizer_node, callback_node, train_node]


def create_pipeline():

    train_node_list = get_train_nodes()
    # connection arg is only used to connect the test nodes after the train graph

    test_node_list = get_test_nodes(
        exp_id_var="params:test_exp", connection_arg="history", set_to_test="data_test"
    )
    validation_node_list = get_test_nodes(
        exp_id_var="params:test_exp", connection_arg="history", set_to_test="data_validation"
    )
    testtrain_node_list = get_test_nodes(
        exp_id_var="params:test_exp", connection_arg="history", set_to_test="data_train_eval"
    )


    return Pipeline(train_node_list + test_node_list + validation_node_list + testtrain_node_list)
