from kedro.pipeline import Pipeline, node

from samplemlproject.callbacks.createcallbacks import create_callbacks_node
from samplemlproject.models.simplemodel import get_simple_model, compile_model
from samplemlproject.procedures.defaulttrain import fit_generator
from samplemlproject.utilities.factoryutils import class_or_func_creation_node


def get_train_nodes():

    model_node = node(
        get_simple_model,
        inputs=dict(input_shape="params:input_shape", output_classes="params:n_classes"),
        outputs=dict(model="model"),
    )

    optimizer_node = node(
        class_or_func_creation_node,
        inputs=["params:optimizer"],
        outputs={"class": "optimizer"}
    )

    compile_node = node(
        compile_model,
        inputs=dict(model="model", output_classes_count="params:n_classes",
                    optimizer="optimizer"),
        outputs=dict(compiled_model="compiled_model"),
    )

    callback_node = node(
        create_callbacks_node,
        inputs=["params:callbacks"],
        outputs=dict(callbacks="init_callbacks")
    )

    train_node = node(
        fit_generator,
        inputs=dict(epochs="params:epochs",
                    model="compiled_model",
                    train_set="data_train",
                    validation_set="data_validation",
                    callbacks="init_callbacks"),
        outputs=dict(history="history", model="final_model")
    )

    return [
            model_node,
            optimizer_node,
            compile_node,
            callback_node,
            train_node
        ]


def create_pipeline():

    train_node_list = get_train_nodes()

    return Pipeline(
        train_node_list
    )
