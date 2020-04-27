from typing import Optional

from keras import Model


def fit_generator(model: Model, train_set, validation_set, epochs: int, callbacks=None,
                  steps_per_epoch: Optional[int] = None,
                  validation_steps: Optional[int] = None):
    history = model.fit_generator(train_set,
                                  epochs=epochs,
                                  validation_data=validation_set,
                                  callbacks=callbacks,
                                  validation_steps=validation_steps,
                                  steps_per_epoch=steps_per_epoch)

    return dict(model=model, history=history)
