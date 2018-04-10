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
"""
Description:
Evaluation will check if the model is accurately trained using the test set or other images.
"""

# Packages
###############################################################################

# Standard library imports
import itertools
import logging
import os
from io import BytesIO
from math import ceil
from urllib.parse import urlparse

# Deeplearning tools imports
from keras import backend as K
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.utils.np_utils import to_categorical

# Data tools imports
import numpy as np
from sklearn.metrics import confusion_matrix

# Graphical tools imports
import matplotlib.pyplot as plt
from PIL import Image

# Additional project imports
import requests

# FormicID imports
from trainers.train import _data_generator_dir
from utils.img import show_img

# Parameters and settings
###############################################################################


# Evaluate generator for test metrics
###############################################################################


def evaluator(model, config):
    """Evaluation will return the score of the model on a test set. This
    function will return the loss, accuracy and top-3 accuracy.

    Args:
        model (Keras model instance): A trained Keras model instance.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        The loss, accuracy and top 3 accuracy for the trained model on the
            test set.

    """
    shottype = config.shottype
    dataset = config.data_set
    test_data_gen_dir, _, _ = _data_generator_dir(
        dataset=dataset, config=config, shottype=shottype, target_gen="test"
    )
    score = model.evaluate_generator(test_data_gen_dir)
    print(
        "Test metrics: "
        "Loss: {:.4f}, "
        "Accuracy: {:.4f}, "
        "Top 3 accuracy: {:.4f}".format(score[0], score[1], score[2])
    )
    return score


# Predict labels generator
###############################################################################


def predictor(model, config):
    """Returns the predition of labels for the test set.

    Args:
        model (Keras model instance): A trained Keras model instance.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        True labels, predicted labels and the label names.

    """
    dataset = config.data_set
    shottype = config.shottype
    test_data_gen_dir, classes, class_indices = _data_generator_dir(
        dataset=dataset, config=config, shottype=shottype, target_gen="test"
    )
    labels = class_indices.keys()
    Y_true = classes
    # print('\nClasses indices from gen:', class_indices)
    # print('\nY_true before argmax:', Y_true)
    Y_pred = model.predict_generator(test_data_gen_dir, verbose=0)
    # Y_true = K.argmax(to_categorical(Y_true, 5), axis=-1)
    Y_true = [i for i in Y_true]
    # print('\nY_pred before argmax:',Y_pred)
    # Y_pred = K.argmax(to_categorical(Y_pred, 5), axis=-1)
    Y_pred = [i.argmax() for i in Y_pred]
    # print('\nY_true after argmax:', Y_true)
    # print('\nY_pred after argmax:', Y_pred)
    return Y_true, Y_pred, labels


# Predict one image
###############################################################################


def predict_image_from_url(model, url):
    """Predict the label from one image retrieved by an URL.

    Args:
        model (Keras model instance): A trained Keras model instance.
        url (str): An valid image URL.

    Returns:
        A prediction of the correct species.

    Raises:
        ValueError: When the image URL does not have a correct image exentsion.

    """
    dissasembled = urlparse(url)
    _, ext = os.path.splitext(os.path.basename(dissasembled.path))
    if ext not in [".png", ".jpg", ".jpeg", ".gif", ".bmp"]:
        raise ValueError(
            "The image exenstion should be one of `.png`, `.jpg`, `.jpeg`, "
            '`.gif`, `.bmp`, instead of "{}".'.format(ext)
        )

    response = requests.get(url)
    print("Predicting: {}".format(url))
    image = Image.open(BytesIO(response.content))
    image = img_to_array(image)
    image = preprocess_input(image)
    image = image.reshape((1,) + image.shape)
    prediction = model.predict(image, batch_size=None, verbose=0, steps=None)
    pred = prediction.argmax()
    # TODO: fix prediction as a number, to show as species name
    print("Predicted species: {}".format(pred))


# Plotting a confusion matrix
###############################################################################


def plot_confusion_matrix(
    Y_pred,
    Y_true,
    target_names=None,
    title="Confusion matrix for 5 species",
    cmap=None,
    normalize=False,
):
    """Plot a confusion matrix of the predicted labels and the true labels for
    the test set species.

    Args:
        Y_pred (array): Predicted labels.
        Y_true (array): True labels.
        target_names (list): The species names as genus + species. Defaults to
            None.
        title (str): Title of the confusion matrix. Defaults to 'Confusion
            matrix for 5 species'.
        cmap (str): Colormap of the plot. Defaults to None.
        normalize (Bool): Will normalize the confusion matrix to [0,1].
            Defaults to False.

    Returns:
        A confusion matrix plot.

    """
    cm = confusion_matrix(y_pred=Y_pred, y_true=Y_true)
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy
    if cmap is None:
        cmap = plt.get_cmap("Blues")
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)
    if normalize:
        cm = cm.astype("float32") / cm.sum(axis=1)
        cm = np.round(cm, 2)
    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(
                j,
                i,
                "{:0.2f}".format(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
            )
        else:
            plt.text(
                j,
                i,
                "{:,}".format(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
            )
    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel(
        "Predicted label\naccuracy={:0.4f}\n misclass={:0.4f}".format(
            accuracy, misclass
        )
    )
    plt.show()


# Plot predictions
###############################################################################


# def plot_predictions(
#     n_images,
#     n_cols,
#     # predictions=None
# ):
#     n_rows = int(ceil(max_img // n_cols))
#     fig, axes = plt.subplots(n_row, n_cols, figsize=(10, 10))
#
#     test_data_gen_dir, classes, class_indices = _data_generator_dir(
#         dataset=dataset,
#         config=config,
#         shottype=shottype,
#         target_gen='test')
#
#     for i in range(n_row):
#         for j in range(n_col):
#             try:
#                 images = X_test[i * n_cols + j]
#                 print(images)
#             except:
#                 break
#             axes[j][k].set_axis_off()
#             if i_inds < N:
#                 axes[j][k].imshow(X[i_data,...], interpolation='nearest')
#                 label = labels[np.argmax(Y[i_data,...])]
#                 axes[j][k].set_title(label)
#                 if predictions is not None:
#                     pred = labels[np.argmax(predictions[i_data,...])]
#                     if label != pred:
#                         label += " n"
#                         axes[j][k].set_title(pred, color='red')
#
#     fig.set_tight_layout(True)
#       return(fig)
# --------
#     for prediction in Y_pred:
#         for classe in classes:
#             key, value = class_indices.get()
#             if value == prediction:
#                 print('5:', prediction, key, classes)
#     print('6:',predictions)
# --------
#     for images, labels in test_data_gen_dir:
#         labs = [i.argmax() for i in labels]
#         for key, value in class_indices.items():
#             if value == labs:
#                 print(labs, key)
#             plt.imshow(images[i,:,:,:])
#             plt.title('title')
#             plt.show()
#     for image in images:
#         for lab in labs:
# -----------
#     x, y in next(test_data_gen_dir)
#     for j in range(0,5):
#         image = x[j]
#         plt.imshow(image)
#         plt.show()
