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

# Standard library imports
import logging

# Deeplearning tools imports
from keras.models import Model
from keras.applications.inception_v3 import preprocess_input

# Data tools imports
import numpy as np
from sklearn.metrics import confusion_matrix

# Additional project imports
import matplotlib.pylab as plt

from trainers.train import _data_generator_dir

# Parameters and settings
###############################################################################


# Test generator
###############################################################################

def tester(
    model,
    dataset,
    shottype,
    config
):
    """Evaluation will return the score of the model on a test set. This
    function will return the loss and accuracy.

    Args:
        model (Keras model instance): A trained Keras model instance.

    Returns:
        float: Returns the loss, accuracy and RMSE for the trained model on a
        test set.

    """
    # print(model.metrics_names)
    score = model.evaluate_generator(
        _data_generator_dir(
            dataset=dataset,
            config=config,
            shottype=shottype,
            target_gen='test'
        )
    )
    logging.info('Loss: {:.4f}, '
                 'Accuracy: {:.2f}%, '
                 'RMSE: {:.4f}'.format(score[0],
                                       score[1] * 100,
                                       score[2]))
    return score


def model_test(image, model, X_test, Y_test):
    """Short summary.

    Args:
        image (type): Description of parameter `image`.
        model (type): Description of parameter `model`.

    Returns:
        type: Description of returned object.

    """
    model.test_on_batch(X_test, Y_test)
    # model.test is for testing a image for label..
    raise NotImplementedError


def plot_confusion_matrix(Y_pred,
                          Y_true,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=False):
    cm = confusion_matrix(y_pred=predictions, y_true=y_true)
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy
    if cmap is None:
        cmap = plt.get_cmap('Blues')
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float32') / cm.sum(axis=1)
        cm = np.round(cm, 2)

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.2f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel("Predicted label\naccuracy={:0.4f}\n misclass={:0.4f}".format(
        accuracy, misclass))
    plt.show()

# plot_confusion_matrix(cm, normalize=True, target_names=labels)
