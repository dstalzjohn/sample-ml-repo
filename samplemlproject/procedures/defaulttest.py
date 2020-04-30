from typing import Dict

from keras.models import load_model, Model

from samplemlproject.utilities.experimentdata import ExperimentData

from samplemlproject.utilities.predictionutils import Predictions, prediction_factory


def defaulttest(test_set, experiment: ExperimentData) -> Predictions:
    model_path = experiment.get_model_path()
    model: Model = load_model(model_path)
    preds_output = model.predict_generator(test_set)
    filenames = test_set.filenames
    class_indices = test_set.class_indices
    classes = test_set.classes
    predictions: Predictions = prediction_factory(preds_output, filenames, classes, class_indices)

    return predictions


def defaulttest_node(test_set, experiment: ExperimentData) -> Dict[str, Predictions]:
    return dict(predictions=defaulttest(test_set, experiment))

