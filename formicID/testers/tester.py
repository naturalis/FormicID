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
import itertools
import logging

# Deeplearning tools imports
from keras.applications.inception_v3 import preprocess_input
from keras.models import Model
from keras import backend as K
from keras.utils.np_utils import to_categorical

# Data tools imports
import numpy as np
from sklearn.metrics import confusion_matrix
from math import ceil

# Graphical tools imports
import matplotlib.pyplot as plt

# FormicID imports
from trainers.train import _data_generator_dir
from utils.img import show_img

# Parameters and settings
###############################################################################


# Evaluate generator
###############################################################################

def evaluator(
    model,
    config,
):
    """Evaluation will return the score of the model on a test set. This
    function will return the loss and accuracy.

    Args:
        model (Keras model instance): A trained Keras model instance.
        dataset (str): The dataset name.
        config (Bunch object): The JSON configuration Bunch object.
        shottype (str): The shottype that will be tested. Defaults to `head`.

    Returns:
        floats: Returns the loss, accuracy and top 3 accuracy for the trained
            model on atest set.

    """
    shottype = config.shottype
    dataset = config.data_set
    test_data_gen_dir, _, _ = _data_generator_dir(
        dataset=dataset,
        config=config,
        shottype=shottype,
        target_gen='test'
    )
    score = model.evaluate_generator(test_data_gen_dir)
    print('Test metrics: '
          'Loss: {:.4f}, '
          'Accuracy: {:.2f}%, '
          'Top 3 accuracy: {:.2f}%'.format(score[0],
                                          score[1] * 100,
                                          score[2] * 100)
          )
    return score


# Predict labels generator
###############################################################################


def predictor(
    model,
    config,
    shottype='head'
):
    """Returns the predition of labels from a set of test images

    Args:
        model (Keras model instance): A trained Keras model instance.
        dataset (str): The dataset name.
        config (Bunch object): The JSON configuration Bunch object.
        shottype (str): The shottype that will be tested. Defaults to `head`.

    Returns:
        (type): txt

    """
    dataset = config.data_set
    test_data_gen_dir, classes, class_indices = _data_generator_dir(
        dataset=dataset,
        config=config,
        shottype=shottype,
        target_gen='test')
    Y_pred = model.predict_generator(test_data_gen_dir, steps=1)
    print(classes)
    Y_true = K.argmax(to_categorical(classes, 5), axis=-1)
    Y_pred = K.argmax(to_categorical(Y_pred, 5), axis=-1)
    print(Y_pred)
    print(Y_true)
    # predictions = [i.argmax() for i in Y_pred]
    # for prediction in predictions:
    #     for classe in classes:
    #         key, value in class_indices.get()
    #         if value == prediction:
    #             print(prediction, key, classes)
    # # print(predictions)

    # for images, labels in test_data_gen_dir:
    #     labs = [i.argmax() for i in labels]
    #     for key, value in class_indices.items():
    #         if value == labs:
    #             print(labs, key)
    #         plt.imshow(images[i,:,:,:])
    #         plt.title('title')
    #         plt.show()
    # for image in images:
    #     for lab in labs:



    return Y_pred


# def plot_predictions(
#     X_test,
#     # Y_test,
#     n_images,
#     n_col,
#     # predictions=None
# ):
#     n_row = int(ceil(1.0 * n_images // n_col))
#     fig, axes = plt.subplots(n_row, n_col, figsize=(10, 10))
#
#     for i in range(n_row):
#         for j in range(n_col):
#             try:
#                 images = X_test[i * n_cols + j]
#                 print(images)
#             except:
#                 break
#           axes[j][k].set_axis_off()
#           if i_inds < N:
#             axes[j][k].imshow(X[i_data,...], interpolation='nearest')
#             label = labels[np.argmax(Y[i_data,...])]
#             axes[j][k].set_title(label)
#             if predictions is not None:
#               pred = labels[np.argmax(predictions[i_data,...])]
#               if label != pred:
#                 label += " n"
#                 axes[j][k].set_title(pred, color='red')
#
#       fig.set_tight_layout(True)
#       return(fig)

# Predict one image
###############################################################################

def model_test(model, image):
    """Test 1 image.

    Args:
        model (type): Description of parameter `model`.
        image (type): Description of parameter `image`.

    Returns:
        type: Description of returned object.

    """
    image = load_img(image)
    image = img_to_array(image)
    # TODO: do the same preprocess_input
    # idg(target_gen='test')
    prediction = model.predict(image)
    return prediction

# Predict labels generator
###############################################################################


def plot_confusion_matrix(
    Y_pred,
    Y_true,
    target_names=None,
    title='Confusion matrix',
    cmap=None,
    normalize=False
):
    cm = confusion_matrix(y_pred=Y_pred, y_true=Y_true)

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
