from kedro.pipeline import Pipeline, node

from samplemlproject.datasets.imagedata import get_image_flow_directory_generator
from samplemlproject.models.simplemodel import get_simple_model, compile_model
from samplemlproject.procedures.defaulttrain import fit_generator
from samplemlproject.utilities.factoryutils import class_or_func_creation_node


def create_pipeline(**kwargs):

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

    train_node = node(
        fit_generator,
        inputs=dict(model="compiled_model",
                    train_set="fruit_data_train",
                    validation_set="fruit_data_test"),
        outputs=dict(history="history", model="final_model")
    )

    return Pipeline(
        [
            model_node,
            optimizer_node,
            compile_node,
            train_node
        ]
    )
