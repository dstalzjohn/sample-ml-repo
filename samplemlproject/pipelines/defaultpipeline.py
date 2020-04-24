from kedro.pipeline import Pipeline, node

from samplemlproject.datasets.imagedata import get_image_flow_directory_generator
from samplemlproject.models.simplemodel import get_simple_model, compile_model
from samplemlproject.procedures.defaulttrain import fit_generator


def create_pipeline(**kwargs):
    data_node = node(
        get_image_flow_directory_generator,
        dict(filepath="/Users/djohn/Projects/01_general/04_engineering_data/fruits-360_dataset/fruits-360",
             batch_size="",
             sub_dir="Training",
             rescale=1/255.,
             classes=["Avocado", "Banana"],
             ),
        dict(data_set="data_set"),
    )

    model_node = node(
        get_simple_model,
        inputs=dict(),
        outputs=dict(model="model"),
    )

    compile_node = node(
        compile_model,
        inputs=dict(model="model"),
        outputs=dict(compiled_model="compiled_model"),
    )

    train_node = node(
        fit_generator,
        inputs=dict(model="compiled_model"),
        outputs=dict(history="history", final_model="model")
    )

    return Pipeline(
        [
            data_node,
            model_node,
            compile_node,
            train_node
        ]
    )
