###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                  Trainer                                    #
#                                                                             #
###############################################################################
"""
Description:
This file contains data generators. These generators generate batches of tensor
image data while also augmenting the images in real-time. The data will be
looped over (in batches) indefinitely. There is a train_data_generator, which
also augments the images with different methods, and a val_data_generator which
does only preprocess the data. Validation data should not be augmented and
could be used for testing. The `preprocessing_function` is needed for the
inception_v3 model. It scales the pixels in  `[-1, 1]`, samplewise and using
the following calculation:

    `x /= 127.5
     x -= 1.
     return x`

"""

# Packages
###############################################################################

# Standard library imports
import os
import warnings
import logging

# Deeplearning tools imports
from keras import backend as K
from keras.applications.densenet import preprocess_input as ppi_Dn
from keras.applications.inception_resnet_v2 import preprocess_input as ppi_IR
from keras.applications.inception_v3 import preprocess_input as ppi_I3
from keras.applications.resnet50 import preprocess_input as ppi_Rn
from keras.preprocessing.image import *

# Data tools imports
import numpy as np
import pandas as pd

###############################################################################

# TODO: This function is implemented in Keras 2.1.5
# But due to a bug in 2.1.5, 2.1.4 is used.
# So when this bug is fixed, Keras can be updated and random_brightness
# could be imported from `keras.preprocessing.image`.


# def random_brightness(x, brightness_range):
#     """Perform a random brightness shift.
#     # Arguments
#         x: Input tensor. Must be 3D.
#         brightness_range: Tuple of floats; brightness range.
#         channel_axis: Index of axis for channels in the input tensor.
#     # Returns
#         Numpy image tensor.
#     # Raises
#         ValueError if `brightness_range` isn't a tuple.
#     """
#     if len(brightness_range) != 2:
#         raise ValueError(
#             "`brightness_range should be tuple or list of two floats. "
#             "Received arg: ",
#             brightness_range,
#         )
#
#     x = array_to_img(x)
#     x = imgenhancer_Brightness = ImageEnhance.Brightness(x)
#     u = np.random.uniform(brightness_range[0], brightness_range[1])
#     x = imgenhancer_Brightness.enhance(u)
#     x = img_to_array(x)
#     return x
#
#
# # Parameters and settings
# ###############################################################################
#
#
# # CSV Iterator and ImageDataGenerator
# ###############################################################################
#
#
# class MyImageDataGenerator(object):
#
#     def __init__(
#         self,
#         featurewise_center=False,
#         samplewise_center=False,
#         featurewise_std_normalization=False,
#         samplewise_std_normalization=False,
#         zca_whitening=False,
#         zca_epsilon=1e-6,
#         rotation_range=0.,
#         width_shift_range=0.,
#         height_shift_range=0.,
#         brightness_range=None,
#         shear_range=0.,
#         zoom_range=0.,
#         channel_shift_range=0.,
#         fill_mode="nearest",
#         cval=0.,
#         horizontal_flip=False,
#         vertical_flip=False,
#         rescale=None,
#         preprocessing_function=None,
#         data_format=None,
#         validation_split=0.0,
#     ):
#         if data_format is None:
#             data_format = K.image_data_format()
#         self.rotation_range = rotation_range
#         self.width_shift_range = width_shift_range
#         self.height_shift_range = height_shift_range
#         self.shear_range = shear_range
#         self.zoom_range = zoom_range
#         self.horizontal_flip = horizontal_flip
#         self.rescale = rescale
#         self.preprocessing_function = preprocessing_function
#
#         if data_format not in {"channels_last", "channels_first"}:
#             raise ValueError(
#                 '`data_format` should be `"channels_last"` (channel after row and '
#                 'column) or `"channels_first"` (channel before row and column). '
#                 "Received arg: ",
#                 data_format,
#             )
#
#         self.data_format = data_format
#         if data_format == "channels_first":
#             self.channel_axis = 1
#             self.row_axis = 2
#             self.col_axis = 3
#         if data_format == "channels_last":
#             self.channel_axis = 3
#             self.row_axis = 1
#             self.col_axis = 2
#         if validation_split and not 0 < validation_split < 1:
#             raise ValueError(
#                 "`validation_split` must be strictly between 0 and 1. "
#                 " Received arg: ",
#                 validation_split,
#             )
#
#         self._validation_split = validation_split
#
#         self.mean = None
#         self.std = None
#         self.principal_components = None
#
#         if np.isscalar(zoom_range):
#             self.zoom_range = [1 - zoom_range, 1 + zoom_range]
#         elif len(zoom_range) == 2:
#             self.zoom_range = [zoom_range[0], zoom_range[1]]
#         else:
#             raise ValueError(
#                 "`zoom_range` should be a float or "
#                 "a tuple or list of two floats. "
#                 "Received arg: ",
#                 zoom_range,
#             )
#
#         if zca_whitening:
#             if not featurewise_center:
#                 self.featurewise_center = True
#                 warnings.warn(
#                     "This ImageDataGenerator specifies "
#                     "`zca_whitening`, which overrides "
#                     "setting of `featurewise_center`."
#                 )
#             if featurewise_std_normalization:
#                 self.featurewise_std_normalization = False
#                 warnings.warn(
#                     "This ImageDataGenerator specifies "
#                     "`zca_whitening` "
#                     "which overrides setting of"
#                     "`featurewise_std_normalization`."
#                 )
#         if featurewise_std_normalization:
#             if not featurewise_center:
#                 self.featurewise_center = True
#                 warnings.warn(
#                     "This ImageDataGenerator specifies "
#                     "`featurewise_std_normalization`, "
#                     "which overrides setting of "
#                     "`featurewise_center`."
#                 )
#         if samplewise_std_normalization:
#             if not samplewise_center:
#                 self.samplewise_center = True
#                 warnings.warn(
#                     "This ImageDataGenerator specifies "
#                     "`samplewise_std_normalization`, "
#                     "which overrides setting of "
#                     "`samplewise_center`."
#                 )
#
#     def standardize(self, x):
#         if self.preprocessing_function:
#             x = self.preprocessing_function(x)
#         if self.rescale:
#             x *= self.rescale
#         if self.samplewise_center:
#             x -= np.mean(x, keepdims=True)
#         if self.samplewise_std_normalization:
#             x /= np.std(x, keepdims=True) + K.epsilon()
#
#         if self.featurewise_center:
#             if self.mean is not None:
#                 x -= self.mean
#             else:
#                 warnings.warn(
#                     "This ImageDataGenerator specifies "
#                     "`featurewise_center`, but it hasn't "
#                     "been fit on any training data. Fit it "
#                     "first by calling `.fit(numpy_data)`."
#                 )
#         if self.featurewise_std_normalization:
#             if self.std is not None:
#                 x /= self.std + K.epsilon()
#             else:
#                 warnings.warn(
#                     "This ImageDataGenerator specifies "
#                     "`featurewise_std_normalization`, but it hasn't "
#                     "been fit on any training data. Fit it "
#                     "first by calling `.fit(numpy_data)`."
#                 )
#         if self.zca_whitening:
#             if self.principal_components is not None:
#                 flatx = np.reshape(x, (-1, np.prod(x.shape[-3:])))
#                 whitex = np.dot(flatx, self.principal_components)
#                 x = np.reshape(whitex, x.shape)
#             else:
#                 warnings.warn(
#                     "This ImageDataGenerator specifies "
#                     "`zca_whitening`, but it hasn't "
#                     "been fit on any training data. Fit it "
#                     "first by calling `.fit(numpy_data)`."
#                 )
#         return x
#
#     def random_transform(self, x, seed=None):
#         # x is a single image, so it doesn't have image number at index 0
#         img_row_axis = self.row_axis - 1
#         img_col_axis = self.col_axis - 1
#         img_channel_axis = self.channel_axis - 1
#         if seed is not None:
#             np.random.seed(seed)
#         # use composition of homographies
#         # to generate final transform that needs to be applied
#         if self.rotation_range:
#             theta = np.deg2rad(
#                 np.random.uniform(-self.rotation_range, self.rotation_range)
#             )
#         else:
#             theta = 0
#         if self.height_shift_range:
#             tx = np.random.uniform(
#                 -self.height_shift_range, self.height_shift_range
#             )
#             if self.height_shift_range < 1:
#                 tx *= x.shape[img_row_axis]
#         else:
#             tx = 0
#         if self.width_shift_range:
#             ty = np.random.uniform(
#                 -self.width_shift_range, self.width_shift_range
#             )
#             if self.width_shift_range < 1:
#                 ty *= x.shape[img_col_axis]
#         else:
#             ty = 0
#         if self.shear_range:
#             shear = np.deg2rad(
#                 np.random.uniform(-self.shear_range, self.shear_range)
#             )
#         else:
#             shear = 0
#         if self.zoom_range[0] == 1 and self.zoom_range[1] == 1:
#             zx, zy = 1, 1
#         else:
#             zx, zy = np.random.uniform(
#                 self.zoom_range[0], self.zoom_range[1], 2
#             )
#         transform_matrix = None
#         if theta != 0:
#             rotation_matrix = np.array(
#                 [
#                     [np.cos(theta), -np.sin(theta), 0],
#                     [np.sin(theta), np.cos(theta), 0],
#                     [0, 0, 1],
#                 ]
#             )
#             transform_matrix = rotation_matrix
#         if tx != 0 or ty != 0:
#             shift_matrix = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
#             transform_matrix = (
#                 shift_matrix
#                 if transform_matrix is None
#                 else np.dot(transform_matrix, shift_matrix)
#             )
#         if shear != 0:
#             shear_matrix = np.array(
#                 [[1, -np.sin(shear), 0], [0, np.cos(shear), 0], [0, 0, 1]]
#             )
#             transform_matrix = (
#                 shear_matrix
#                 if transform_matrix is None
#                 else np.dot(transform_matrix, shear_matrix)
#             )
#         if zx != 1 or zy != 1:
#             zoom_matrix = np.array([[zx, 0, 0], [0, zy, 0], [0, 0, 1]])
#             transform_matrix = (
#                 zoom_matrix
#                 if transform_matrix is None
#                 else np.dot(transform_matrix, zoom_matrix)
#             )
#         if transform_matrix is not None:
#             h, w = x.shape[img_row_axis], x.shape[img_col_axis]
#             transform_matrix = transform_matrix_offset_center(
#                 transform_matrix, h, w
#             )
#             x = apply_transform(
#                 x,
#                 transform_matrix,
#                 img_channel_axis,
#                 fill_mode=self.fill_mode,
#                 cval=self.cval,
#             )
#         if self.channel_shift_range != 0:
#             x = random_channel_shift(
#                 x, self.channel_shift_range, img_channel_axis
#             )
#         if self.horizontal_flip:
#             if np.random.random() < 0.5:
#                 x = flip_axis(x, img_col_axis)
#         if self.vertical_flip:
#             if np.random.random() < 0.5:
#                 x = flip_axis(x, img_row_axis)
#         if self.brightness_range is not None:
#             x = random_brightness(x, self.brightness_range)
#         return x
#
#     def flow_from_csv(
#         self,
#         csv,
#         shotview="head",
#         target_size=(256, 256),
#         color_mode="rgb",
#         classes=None,
#         class_mode="categorical",
#         batch_size=32,
#         shuffle=True,
#         seed=None,
#         subset=None,
#         interpolation="nearest",
#     ):
#         return CsvIterator(
#             self,
#             csv,
#             shotview=shotview,
#             target_size=target_size,
#             color_mode=color_mode,
#             classes=classes,
#             class_mode=class_mode,
#             data_format=self.data_format,
#             batch_size=batch_size,
#             shuffle=shuffle,
#             seed=seed,
#             subset=subset,
#             interpolation=interpolation,
#         )
#
#
# def _iter_csv_rows(csv, shotview):
#     with open(csv, "rt") as open_csv:
#         df = pd.read_csv(open_csv, sep=",")
#         df_shot = df.loc[df["shottype"] == shotview]
#         for row in df_shot.itertuples():
#             # yield path, species
#             path = row[4]
#             fname = row[2]
#             yield path, fname
#
#
# def _count_pathways_in_csv(csv, split, shotview):
#     num_paths = len(list(_iter_csv_rows(csv, shotview)))
#     if split:
#         start, stop = int(split[0] * num_paths), int(split[1] * num_paths)
#     else:
#         start, stop = 0, num_paths
#     return stop - start
#
#
# def _list_pathways_in_csv(csv, split, class_indices, shotview):
#     if split:
#         num_paths = len(list(_iter_csv_rows(csv, shotview)))
#         start, stop = int(split[0] * num_paths), int(split[1] * num_paths)
#         pathways = list(_iter_csv_rows(csv, shotview))[start:stop]
#     else:
#         pathways = _iter_csv_rows(csv, shotview)
#
#     classes = []
#     paths = []
#     for path, fname in pathways:
#         classes.append(class_indices[fname])
#         paths.append(path)
#
#     return classes, paths
#
#
# class CsvIterator(Iterator):
#
#     def __init__(
#         self,
#         image_data_generator,
#         csv,
#         shotview="head",
#         target_size=(299, 299),
#         color_mode="rgb",
#         classes=None,
#         class_mode="categorical",
#         batch_size=32,
#         shuffle=True,
#         seed=None,
#         data_format=None,
#         subset=None,
#         interpolation="nearest",
#     ):
#         if data_format is None:
#             data_format = K.image_data_format()
#         self.csv = csv
#         self.image_data_generator = image_data_generator
#         self.target_size = tuple(target_size)
#         if color_mode not in {"rgb", "grayscale"}:
#             raise ValueError(
#                 "Invalid color mode:",
#                 color_mode,
#                 '; expected "rgb" or "grayscale".',
#             )
#
#         self.color_mode = color_mode
#         self.data_format = data_format
#         if self.color_mode == "rgb":
#             if self.data_format == "channels_last":
#                 self.image_shape = self.target_size + (3,)
#             else:
#                 self.image_shape = (3,) + self.target_size
#         else:
#             if self.data_format == "channels_last":
#                 self.image_shape = self.target_size + (1,)
#             else:
#                 self.image_shape = (1,) + self.target_size
#         self.classes = classes
#         if class_mode not in {
#             "categorical",
#             "binary",
#             "sparse",
#             "input",
#             None,
#         }:
#             raise ValueError(
#                 "Invalid class_mode:",
#                 class_mode,
#                 '; expected one of "categorical", '
#                 '"binary", "sparse", "input"'
#                 " or None.",
#             )
#
#         self.class_mode = class_mode
#         self.interpolation = interpolation
#         if subset is not None:
#             validation_split = self.image_data_generator._validation_split
#             if subset == "validation":
#                 split = (0, validation_split)
#             elif subset == "training":
#                 split = (validation_split, 1)
#             else:
#                 raise ValueError(
#                     "Invalid subset name: ",
#                     subset,
#                     '; expected "training" or "validation"',
#                 )
#
#         else:
#             split = None
#         self.subset = subset
#
#         #######################################################################
#         # first, count the number of samples and classes
#
#         # self.samples = 0
#         if not classes:
#             with open(csv, "rt") as csv_open:
#                 df = pd.read_csv(csv_open, sep=",")
#                 # filter for shottype
#                 df_shot = df.loc[df["shottype"] == shotview]
#                 # get classes, count and put in dict
#                 classes = df_shot.species.unique()
#                 self.num_classes = len(classes)
#                 self.class_indices = dict(zip(classes, range(len(classes))))
#                 self.samples = _count_pathways_in_csv(csv, split, shotview)
#
#                 # TODO shottype incorporation instead of filtering
#                 shottypes = df_shot.shottype.unique()
#                 self.num_shottypes = len(shottypes)
#                 self.shottype_indicies = dict(
#                     zip(shottypes, range(len(shottypes)))
#                 )
#
#         print(
#             "Found {0} images for {1} classes with shottype: {2}.".format(
#                 self.samples, self.num_classes, shotview
#             )
#         )
#
#         #######################################################################
#         # second build an index of the images in the different class subfolders
#         # results = []
#         # self.pathways = []
#         # self.classes = np.zeros((self.samples,), dtype='int32')
#         i = 0
#
#         results = _list_pathways_in_csv(
#             csv, split, self.class_indices, shotview
#         )
#         self.classes, self.pathways = results
#         print("self.classes: ", self.classes)
#         print("self.pathways: ", self.pathways)
#         assert len(self.classes) == len(self.pathways)
#         # TODO: Fix lines below
#         # for res in results:
#         #     classes, pathways = res.get()
#         #     self.classes[i:i + len(classes)] = classes
#         #     self.pathways += pathways
#         #     i += len(classes)
#
#         super(CsvIterator, self).__init__(
#             self.samples, batch_size, shuffle, seed
#         )
#
#     def _get_batches_of_transformed_samples(self, index_array):
#         batch_x = np.zeros(
#             (len(index_array),) + self.image_shape, dtype=K.floatx()
#         )
#         grayscale = self.color_mode == "grayscale"
#
#         # build batch of image data
#         for i, j in enumerate(index_array):
#             fname = self.pathways[j]
#             img = load_img(
#                 fname,
#                 grayscale=grayscale,
#                 target_size=self.target_size,
#                 interpolation=self.interpolation,
#             )
#             x = img_to_array(img, data_format=self.data_format)
#             x = self.image_data_generator.random_transform(x)
#             x = self.image_data_generator.standardize(x)
#             batch_x[i] = x
#
#         # build batch of labels
#         if self.class_mode == "categorical":
#             batch_y = np.zeros(
#                 (len(batch_x), self.num_classes), dtype=K.floatx()
#             )
#         # TODO: fix 2 lines below - What do they do?
#         # for i, label in enumerate(self.classes[index_array]):
#         #     batch_y[i, label] = 1.
#         else:
#             return batch_x
#
#         return batch_x, batch_y
#
#
# def trainer_csv(model, csv, shottype, config, callbacks=None):
#     epochs = config.num_epochs
#     batch_size = config.batch_size
#     if model in ["InceptionV3", "Xception", "Build"]:
#         preprocess_input = ppi_I3
#     if model == "InceptionResNetV2":
#         preprocess_input = ppi_IR
#     if model == "ResNet50":
#         preprocess_input = ppi_Rn
#     if model == "DenseNet169":
#         preprocess_input = ppi_Dn
#     idg_t = MyImageDataGenerator(
#         preprocessing_function=preprocess_input,
#         rotation_range=40,
#         width_shift_range=0.2,
#         height_shift_range=0.2,
#         shear_range=0.2,
#         zoom_range=0.2,
#         horizontal_flip=True,
#         validation_split=0.20,
#     )
#     train_data_generator = idg_t.flow_from_csv(
#         csv=csv, shotview="head", subset="training"
#     )
#     idg_v = MyImageDataGenerator(
#         preprocessing_function=preprocess_input, validation_split=0.20
#     )
#     val_data_generator = idg_v.flow_from_csv(
#         csv=csv, shotview="head", subset="validation"
#     )
#     model.fit_generator(
#         generator=train_data_generator,
#         steps_per_epoch=3,
#         epochs=epochs,
#         validation_data=val_data_generator,
#         validation_steps=3,
#         callbacks=callbacks,
#     )
#

# ImageDataGenerator
###############################################################################


def idg(config, target_gen="training"):
    """Initialize an augmentation generator for either a `training`,
    `validation`, `test` dataset.

    Args:
        config (Bunch object): The JSON configuration Bunch object.
        target_gen (str): Should be either `training`, `validation`, or
            `test`. Defaults to `training`.

    Returns:
        generator: A Keras image data generator object.

    Raises:
        ValueError: If target_gen is not set to acorrectly value.

    """
    model = config.model
    if model in ["InceptionV3", "Xception", "Build"]:
        preprocess_input = ppi_I3
    if model == "InceptionResNetV2":
        preprocess_input = ppi_IR
    if model == "ResNet50":
        preprocess_input = ppi_Rn
    if model == "DenseNet169":
        preprocess_input = ppi_Dn
    if target_gen not in ["training", "validation", "test"]:
        raise ValueError(
            "Argument {} is in invalid  for `target_gen`. It should be one of "
            "`training`, `validation`, or `testing`.".format(target_gen)
        )

    if target_gen == "training":
        idg = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
        )
    if target_gen in ["validation", "test"]:
        idg = ImageDataGenerator(preprocessing_function=preprocess_input)
    return idg


# flow_from_directory
###############################################################################


def _generator_dir(
    config, target_gen="training", shottype=None, data_dir=None
):
    """Generator for reading images out of directories. Can be used for a
    `training`, `validation` or `test` set. `Validation` and `test` sets will
    not be shuffled.

    Args:
        config (Bunch object): The JSON configuration Bunch object.
        target_gen (str): Sets the generator to either 'training',
            `validation` or `test.`. Defaults to 'training'.
        shottype (str): Should be either  `dorsal`, `head` or `profile`. If no
            shottype is provided, shottype will be taken from the
            configuration file. Defaults to None.
        data_dir (str): Directory that holds training, validation or test
            images. Optional, if not set, the default training, validation,
            test directories (created by `split_in_directory()`) will be used.
            Defaults to None.
        batch_size (int): set the batch size for the generator. If data_dir is None, batch should also be none. Defaults to None.

    Returns:
        Image directory generator.
        list: A list of all classes.
        dict: A dictionary mapping of the classes.

    """
    model = config.model
    seed = config.seed
    dataset = config.data_set
    if shottype == None:
        shottype = config.shottype
    if model in ["InceptionV3", "InceptionResNetV2", "Xception"]:
        target_size = (299, 299)
    if model in ["ResNet50", "DenseNet169"]:
        target_size = (224, 224)
    if target_gen == "training":
        shuffle = True
        dir = "1-training"
        batch_size = config.batch_size
    if target_gen == "validation":
        shuffle = False
        dir = "2-validation"
        batch_size = config.batch_size
    if target_gen == "test":
        shuffle = False
        dir = "3-test"
        batch_size = 1
    if data_dir is None:
        data_dir = os.path.join("data", dataset, "images", shottype, dir)
    idgen = idg(config=config, target_gen=target_gen)
    idgen = idgen.flow_from_directory(
        directory=data_dir,
        target_size=target_size,
        color_mode="rgb",
        class_mode="categorical",
        batch_size=batch_size,
        shuffle=shuffle,
        seed=seed,
    )
    classes = idgen.classes
    class_indices = idgen.class_indices
    return idgen, classes, class_indices


# Stitching idg and flow_from_directory in to one function
###############################################################################


def trainer_dir(model, config, callbacks=None):
    """The directory trainer. This combines the validation and training data
        generators and trains on the input model.

    Args:
        model (Keras model instance): A trained Keras model instance.
        config (Bunch object): The JSON configuration Bunch object.
        callbacks (type): A list of the callbacks for viewing training and
            validation metrics. Defaults to None.

    Returns:
        Keras History instance with training and validation metrics.

    """
    logging.info("Training started.")
    epochs = config.num_epochs
    batch_size = config.batch_size
    train_data_gen_dir, _, _ = _generator_dir(
        config=config, target_gen="training"
    )
    train_samples = train_data_gen_dir.samples
    val_data_gen_dir, _, _ = _generator_dir(
        config=config, target_gen="validation"
    )
    val_samples = val_data_gen_dir.samples
    history = model.fit_generator(
        generator=train_data_gen_dir,
        steps_per_epoch=train_samples // batch_size,
        epochs=epochs,
        validation_data=val_data_gen_dir,
        validation_steps=val_samples // batch_size,
        callbacks=callbacks,
    )
    logging.info("Training ended.")
    return history


# Multi-view generator with flow_from_directory
###############################################################################


# TODO: Fix functions below.


def multiview_generator_dir():
    train_h_data_gen_dir, _, _ = _generator_dir(
        config=config, target_gen="training", shottype="head"
    )
    train_d_data_gen_dir, _, _ = _generator_dir(
        config=config, target_gen="training", shottype="dorsal"
    )
    train_p_data_gen_dir, _, _ = _generator_dir(
        config=config, target_gen="training", shottype="profile"
    )
    while True:
        hgen = train_h_data_gen_dir.next()
        dgen = train_d_data_gen_dir.next()
        pgen = train_p_data_gen_dir.next()
        # TODO: catch the specimens that don't have all 3 shottypes
        yield [hgen[0], dgen[0], pgen[0]], hgen[1]


def train_multiview_dir(model, config, generator, callbacks=None):
    epochs = config.num_epochs
    batch_size = config.batch_size
    train_samples = generator.samples
    # TODO: fix validation
    # val_samples = val_data_gen_dir.samples
    history = model.fit_generator(
        generator=generator,
        steps_per_epoch=train_samples // batch_size,
        epochs=epochs,
        # validation_data=val_data_gen_dir,
        # validation_steps=val_samples // batch_size,
        callbacks=callbacks,
    )
    return history
