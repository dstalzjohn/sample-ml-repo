from typing import Tuple

from keras.models import Sequential, Model
from keras.layers import Conv2D, Activation, LeakyReLU, BatchNormalization
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Dense
from keras.optimizers import RMSprop


def get_simple_model(input_shape: Tuple, output_classes: int) -> dict:
    model = Sequential()

    # first hidden layer
    model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
    model.add(Activation('relu'))

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
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    # Outputs from dense layer are projected onto output layer
    model.add(Dense(output_classes))
    model.add(Activation('sigmoid'))

    return dict(model=model)


def compile_model(model: Model, output_classes_count: int):
    loss = 'binary_crossentropy' if output_classes_count == 1 else 'categorical_crossentropy'

    model.compile(optimizer=RMSprop(lr=0.0001, decay=1e-6), loss=loss, metrics=['accuracy'])

    return dict(compiled_model=model)

