###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                          Tester of a trained network                        #
#                                                                             #
###############################################################################
'''
Description:
<placeholder txt>
'''

# Packages
###############################################################################
from keras.model import test_on_batch

# Parameters and settings
###############################################################################


# Validation
###############################################################################


def model_evaluate(model):
    # Evaluate is for getting score and accuracy on test set.
    # model.test is for testing a image for label.
    loss, accuracy = model.evaluate(testdataX, testdataY)

    print("\nLoss: {:2f}, Accuracy: {:2f}".format(loss, accuracy*100))
    return loss, accuracy


def model_test(image, model):
    # model.test_on_batch(x,y)

    raise NotImplementedError
