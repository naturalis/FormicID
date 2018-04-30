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
Testing functions will check if the model is accurately trained using the test set or other images.
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
from trainers.train import _generator_dir

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
    test_data_gen_dir, _, _ = _generator_dir(config=config, target_gen="test")
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


def predictor(model, config, plot=False, n_img=None, n_cols=None):
    """Returns the prediction of labels for the test set.

    Args:
        model (Keras model instance): A trained Keras model instance.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        True labels, predicted labels and the label names.

    """
    if plot == False:
        n_img, n_cols = None, None
    dataset = config.data_set
    shottype = config.shottype
    test_data_gen_dir, classes, class_indices = _generator_dir(
        config=config, target_gen="test"
    )
    labels = class_indices.keys()
    Y_true = classes
    # print("Classes indices from gen:", class_indices)
    Y_pred = model.predict_generator(test_data_gen_dir, verbose=0)
    # print('Y_true before argmax:', Y_true)
    # print('Y_pred before argmax:',Y_pred)
    # Y_true = K.argmax(to_categorical(Y_true, 5), axis=-1)
    # Y_pred = K.argmax(to_categorical(Y_pred, 5), axis=-1)
    Y_true = [i for i in Y_true]
    Y_pred = [i.argmax() for i in Y_pred]
    # print("Y_true after argmax:", Y_true)
    # print("Y_pred after argmax:", Y_pred)
    # for i in Y_pred:
    #     for j in Y_true:
    #         if i == value in class_indices.items():
    #             print(i, key, j)
    # if plot == True:
    #     n_rows = int(ceil(n_img // n_cols))
    #     fig = plt.figure()
    #     for i in range(1, n_img + 1):
    #         x, y = next(test_data_gen_dir)
    #         sub = plt.subplots(n_rows, n_cols, figsize=(10, 10))
    #         # sub.set_title('y')
    #         # sub.axis("off")
    #         sub.imshow(data[x])
    #     plt.show()

    return Y_true, Y_pred, labels, class_indices


# Predict one image
###############################################################################


def _process_species_dict(dict, species):
    for k, v in dict.items():
        if v == species:
            return str(k)


def predict_image(model, url=None, image=None, species_dict=None):
    """Predict the label from one image, either retrieved by URL, or a local
    input.

    Args:
        model (Keras model instance): A trained Keras model instance.
        url (str): An URL leading to an image. Defaults to None.
        image (str): The pathway to an image. Defaults to None.
        species_dict (dict): dictionary mapping of the species, as output by
            the `predictor` function. Defaults to None.

    Returns:
        A prediction of the correct species.

    Raises:
        ValueError: When the image is not in the correct image exentsion.

    """
    dissasembled = urlparse(url)
    _, ext = os.path.splitext(os.path.basename(dissasembled.path))
    if ext not in [".png", ".jpg", ".jpeg", ".gif", ".bmp"]:
        raise ValueError(
            "The image exenstion should be one of `.png`, `.jpg`, `.jpeg`, "
            '`.gif`, `.bmp`, instead of "{}".'.format(ext)
        )

    if url:
        response = requests.get(url)
        logging.info("Predicting from URL: {}".format(url))
        img = Image.open(BytesIO(response.content))
    if image:
        logging.info("Predicting from local image: {}".format(image))
        img = load_img(image)
    plt.imshow(img)
    img = img_to_array(img)
    img = preprocess_input(img)
    img = img.reshape((1,) + img.shape)
    prediction = model.predict(img, batch_size=None, verbose=0, steps=None)
    pred = prediction.argmax()
    species = _process_species_dict(species_dict, pred)
    species = species.capitalize()
    species = species.replace("_", " ")
    print("Predicted species: {}".format(species))

    plt.title("Predicted species: {}".format(species))
    plt.show()


# Plotting a confusion matrix
###############################################################################


def plot_confusion_matrix(
    Y_pred,
    Y_true,
    target_names=None,
    title="Confusion matrix",
    cmap=None,
    normalize=False,
    scores=False,
    save=None,
):
    """Plot a confusion matrix of the predicted labels and the true labels for
    the test set species.

    Args:
        Y_pred (array): Predicted labels.
        Y_true (array): True labels.
        target_names (list): The species names as genus + species. Defaults to
            None.
        title (str): Title of the confusion matrix. Defaults to 'Confusion
            matrix'.
        cmap (str): Colormap of the plot. Defaults to None.
        normalize (Bool): Will normalize the confusion matrix to [0,1].
            Defaults to False.
        scores (Bool): If set to True it will show scores for predicted labels
            and true labels in the confusion matrix. Defaults to False.

    Returns:
        A confusion matrix plot.

    """
    # TODO: Fix the tick lines through the plot
    cm = confusion_matrix(y_pred=Y_pred, y_true=Y_true)
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy
    if cmap is None:
        cmap = plt.get_cmap("Blues")
    if normalize:
        cm = cm.astype("float32") / cm.sum(axis=1)[:, np.newaxis]
        cm = np.round(cm, 2)
    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    plt.figure(figsize=(25, 15))
    plt.title(title)
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.colorbar()
    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(
            tick_marks, target_names, rotation=45, horizontalalignment="right"
        )
        plt.yticks(tick_marks, target_names)
    if scores:
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            if normalize:
                if cm[i, j] > 0:
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
    if save is not None:
        plt.savefig(save)
        print("The confusion matrix has been saved as {}".format(save))
    plt.show()


# Plot predictions
###############################################################################


# def plot_predictions(, predictions=None):
#     dataset = config.data_set
#     shottype = config.shottype
#     test_data_gen_dir, classes, class_indices = _generator_dir(
#         dataset=dataset, config=config, shottype=shottype, target_gen="test"
#     )


#
# for i in range(n_rows):
#     for j in range(n_cols):
# for img in img_list[0:max_img]:
#     image = load_img(path=os.path.join(aug_dir, img))
#     fig.add_subplot(n_rows, n_cols, i)
#     plt.imshow(image)
# plt.show()
#
#
#
#         axes[j][k].set_axis_off()
#         if i_inds < N:
#             axes[j][k].imshow(X[i_data, ...], interpolation="nearest")
#             label = labels[np.argmax(Y[i_data, ...])]
#             axes[j][k].set_title(label)
#             if predictions is not None:
#                 pred = _process_species_dict(species_dict, pred)
#                 if label != pred:
#                     label += " n"
#                     axes[j][k].set_title(pred, color="red")
#
# fig.set_tight_layout(True)
#
# return(fig)
#
#
# for images, labels in test_data_gen_dir:
#     labs = [i.argmax() for i in labels]
#     for key, value in class_indices.items():
#         if value == labs:
#             print(labs, key)
#         plt.imshow(images[i, :, :, :])
#         plt.title("title")
#         plt.show()
# for image in images:
#     for lab in labs:
#         break
