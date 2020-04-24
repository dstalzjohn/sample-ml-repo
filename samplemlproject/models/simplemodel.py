from typing import Tuple

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Dense
from keras.optimizers import SGD


def get_simple_model(input_shape: Tuple) -> dict:
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.1))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.02))

    model.add(Flatten())
    # Fully-Connected
    model.add(Dense(units=128, activation='relu'))
    # Ausgabeschicht
    model.add(Dense(units=1, activation='sigmoid'))

    return dict(model=model)


def compile_model(model):
    model.compile(optimizer=SGD(lr=0.001), loss='binary_crossentropy', metrics=['accuracy'])

    return dict(compiled_model=model)

