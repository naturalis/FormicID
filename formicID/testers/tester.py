###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                 Model testing                               #
#                                                                             #
###############################################################################
'''
Description:
After the model is trained evaluation can be started using these scripts.
After evaluation looks good, we can test the model with unseen images.
'''

# Packages
###############################################################################

import logging

from keras.model import test_on_batch

# Parameters and settings
###############################################################################


# Validation
###############################################################################


def model_evaluate(model, X_test, Y_test):
    """Evaluation will return the score of the model on a test set. This
    function will return the loss and accuracy.

    Args:
        model (Keras model instance): A trained Keras model instance.

    Returns:
        float: Returns the loss and accuracy for the trained model on a test
            set.

    """

    loss, accuracy = model.evaluate(X_test, Y_test, verbose=0)

    logging.info("Loss: {:2f}, Accuracy: {:2f}".format(loss, accuracy * 100))

    return loss, accuracy


def model_test(image, model):
    """Short summary.

    Args:
        image (type): Description of parameter `image`.
        model (type): Description of parameter `model`.

    Returns:
        type: Description of returned object.

    Raises:        ExceptionName: Why the exception is raised.

    """
    # model.test_on_batch(x,y)
    # model.test is for testing a image for label..
    raise NotImplementedError
