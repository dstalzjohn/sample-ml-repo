from kedro.pipeline import Pipeline, node

from samplemlproject.datasets.imagedata import get_image_flow_directory_generator
from samplemlproject.models.simplemodel import get_simple_model, compile_model
from samplemlproject.procedures.defaulttrain import fit_generator


def create_pipeline(**kwargs):

    model_node = node(
        get_simple_model,
        inputs=dict(input_shape="params:input_shape"),
        outputs=dict(model="model"),
    )

    compile_node = node(
        compile_model,
        inputs=dict(model="model"),
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
            compile_node,
            train_node
        ]
    )
