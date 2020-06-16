from typing import Tuple

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, Activation, LeakyReLU, BatchNormalization
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Optimizer


def get_simple_model(*args, **kwargs) -> dict:
    return dict(model=SimpleModel(*args, **kwargs))


class SimpleModel(object):
    def __init__(self, input_shape: Tuple, output_classes: int, *args, **kwargs):
        self.input_shape = input_shape
        self.output_classes = output_classes
        self.args = args
        self.kwargs = kwargs

    def __call__(self):

        model = Sequential()

        # first hidden layer
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=self.input_shape))
        model.add(Activation("relu"))

        # second hidden layer
        model.add(Conv2D(16, (3, 3), padding="same"))
        model.add(LeakyReLU(alpha=0.5))
        model.add(BatchNormalization())

        # max pooling
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # Flatten max filtered output into feature vector
        # and feed into dense layer
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))

        # Outputs from dense layer are projected onto output layer
        model.add(Dense(self.output_classes))
        model.add(Activation("sigmoid"))

        return model


def compile_model(model: Model, output_classes_count: int, optimizer: Optimizer):
    loss = (
        "binary_crossentropy"
        if output_classes_count == 1
        else "categorical_crossentropy"
    )

    model.compile(optimizer=optimizer, loss=loss, metrics=["accuracy"])

    return dict(compiled_model=model)
