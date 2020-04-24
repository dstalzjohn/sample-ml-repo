from keras import Model


def fit_generator(model: Model, train_set, validation_set, callbacks=None):
    history = model.fit_generator(train_set,
                                  steps_per_epoch=118,
                                  epochs=12, validation_data=validation_set,
                                  validation_steps=21, callbacks=callbacks)

    return dict(model=model, history=history)