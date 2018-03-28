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
'''
Description:
This file contains data generators. These generators generate batches of tensor
image data while also augmenting the images in real-time. The data will be
looped over (in batches) indefinitely. There is a train_data_generator, which
also augments the images with different methods, and a val_data_generator which
does only preprocess the data. Validation data should not be augmented. The
`preprocessing_function` is needed for the inception_v3 model. It scales the
pixels in  `[-1, 1]`, samplewise and using the following calculation:
    `x /= 127.5
     x -= 1.
     return x`
'''

# Packages
###############################################################################

# Standard library imports
import os

# Deeplearning tools imports
from keras import backend as K
from keras.applications.inception_v3 import preprocess_input
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import Iterator
from keras.preprocessing.image import *

# Data tools imports
import numpy as np
import pandas as pd

# TODO: fix the * import, as for now it is just a temporary  fix for importing
# image transform functions


# Parameters and settings
###############################################################################


# CSV Iterator and ImageDataGenerator
###############################################################################


class MyImageDataGenerator(object):
    def __init__(self,
                 rotation_range=0.,
                 width_shift_range=0.,
                 height_shift_range=0.,
                 shear_range=0.,
                 zoom_range=0.,
                 fill_mode='nearest',
                 cval=0.,
                 horizontal_flip=False,
                 rescale=None,
                 preprocessing_function=None,
                 data_format=None,
                 validation_split=0.0):
        if data_format is None:
            data_format = K.image_data_format()
        self.rotation_range = rotation_range
        self.width_shift_range = width_shift_range
        self.height_shift_range = height_shift_range
        self.shear_range = shear_range
        self.zoom_range = zoom_range
        self.horizontal_flip = horizontal_flip
        self.rescale = rescale
        self.preprocessing_function = preprocessing_function

        if data_format not in {'channels_last', 'channels_first'}:
            raise ValueError('`data_format` should be `"channels_last"` (channel after row and '
                             'column) or `"channels_first"` (channel before row and column). '
                             'Received arg: ', data_format)
        self.data_format = data_format
        if data_format == 'channels_first':
            self.channel_axis = 1
            self.row_axis = 2
            self.col_axis = 3
        if data_format == 'channels_last':
            self.channel_axis = 3
            self.row_axis = 1
            self.col_axis = 2
        if validation_split and not 0 < validation_split < 1:
            raise ValueError('`validation_split` must be strictly between 0 and 1. '
                             ' Received arg: ', validation_split)
        self._validation_split = validation_split

        self.mean = None
        self.std = None
        self.principal_components = None

        if np.isscalar(zoom_range):
            self.zoom_range = [1 - zoom_range, 1 + zoom_range]
        elif len(zoom_range) == 2:
            self.zoom_range = [zoom_range[0], zoom_range[1]]
        else:
            raise ValueError('`zoom_range` should be a float or '
                             'a tuple or list of two floats. '
                             'Received arg: ', zoom_range)

    def standardize(self, x):
        if self.preprocessing_function:
            x = self.preprocessing_function(x)
        if self.rescale:
            x *= self.rescale
        return x

    def random_transform(self, x, seed=None):
        # x is a single image, so it doesn't have image number at index 0
        img_row_axis = self.row_axis - 1
        img_col_axis = self.col_axis - 1
        img_channel_axis = self.channel_axis - 1

        if seed is not None:
            np.random.seed(seed)

        # use composition of homographies
        # to generate final transform that needs to be applied
        if self.rotation_range:
            theta = np.deg2rad(
                np.random.uniform(-self.rotation_range, self.rotation_range))
        else:
            theta = 0

        if self.height_shift_range:
            tx = np.random.uniform(-self.height_shift_range,
                                   self.height_shift_range)
            if self.height_shift_range < 1:
                tx *= x.shape[img_row_axis]
        else:
            tx = 0

        if self.width_shift_range:
            ty = np.random.uniform(-self.width_shift_range,
                                   self.width_shift_range)
            if self.width_shift_range < 1:
                ty *= x.shape[img_col_axis]
        else:
            ty = 0

        if self.shear_range:
            shear = np.deg2rad(
                np.random.uniform(-self.shear_range, self.shear_range))
        else:
            shear = 0

        if self.zoom_range[0] == 1 and self.zoom_range[1] == 1:
            zx, zy = 1, 1
        else:
            zx, zy = np.random.uniform(
                self.zoom_range[0], self.zoom_range[1], 2)

        if self.horizontal_flip:
            if np.random.random() < 0.5:
                x = flip_axis(x, img_col_axis)

        return x

    def flow_from_csv(self, csv, shotview='head',
                      target_size=(256, 256), color_mode='rgb',
                      classes=None, class_mode='categorical',
                      batch_size=32, shuffle=True, seed=None,
                      subset=None,
                      interpolation='nearest'):
        return CsvIterator(
            self, csv, shotview=shotview,
            target_size=target_size, color_mode=color_mode,
            classes=classes, class_mode=class_mode,
            data_format=self.data_format,
            batch_size=batch_size, shuffle=shuffle, seed=seed,
            subset=subset,
            interpolation=interpolation)


def _iter_csv_rows(csv, shotview):
    with open(csv, 'rt') as open_csv:
        df = pd.read_csv(open_csv, sep=',')
        df_shot = df.loc[df['shottype'] == shotview]
        for row in df_shot.itertuples():
            # yield path, species
            path = row[4]
            fname = row[2]
            yield path, fname


def _count_pathways_in_csv(csv, split, shotview):
    num_paths = len(list(_iter_csv_rows(csv, shotview)))
    if split:
        start, stop = int(split[0] * num_paths), int(split[1] * num_paths)
    else:
        start, stop = 0, num_paths
    return stop - start


def _list_pathways_in_csv(csv, split, class_indices, shotview):
    if split:
        num_paths = len(list(_iter_csv_rows(csv, shotview)))
        start, stop = int(split[0] * num_paths), int(split[1] * num_paths)
        pathways = list(_iter_csv_rows(csv, shotview))[start: stop]
    else:
        pathways = _iter_csv_rows(csv, shotview)

    classes = []
    paths = []
    for path, fname in pathways:
        classes.append(class_indices[fname])
        paths.append(path)

    return classes, paths


class CsvIterator(Iterator):
    def __init__(self, image_data_generator,
                 csv, shotview='head',
                 target_size=(299, 299), color_mode='rgb',
                 classes=None, class_mode='categorical',
                 batch_size=32, shuffle=True, seed=None,
                 data_format=None,
                 subset=None,
                 interpolation='nearest'):
        if data_format is None:
            data_format = K.image_data_format()
        self.csv = csv
        self.image_data_generator = image_data_generator
        self.target_size = tuple(target_size)
        if color_mode not in {'rgb', 'grayscale'}:
            raise ValueError('Invalid color mode:', color_mode,
                             '; expected "rgb" or "grayscale".')
        self.color_mode = color_mode
        self.data_format = data_format
        if self.color_mode == 'rgb':
            if self.data_format == 'channels_last':
                self.image_shape = self.target_size + (3,)
            else:
                self.image_shape = (3,) + self.target_size
        else:
            if self.data_format == 'channels_last':
                self.image_shape = self.target_size + (1,)
            else:
                self.image_shape = (1,) + self.target_size
        self.classes = classes
        if class_mode not in {'categorical', 'binary', 'sparse',
                              'input', None}:
            raise ValueError('Invalid class_mode:', class_mode,
                             '; expected one of "categorical", '
                             '"binary", "sparse", "input"'
                             ' or None.')
        self.class_mode = class_mode
        self.interpolation = interpolation
        if subset is not None:
            validation_split = self.image_data_generator._validation_split
            if subset == 'validation':
                split = (0, validation_split)
            elif subset == 'training':
                split = (validation_split, 1)
            else:
                raise ValueError('Invalid subset name: ', subset,
                                 '; expected "training" or "validation"')
        else:
            split = None
        self.subset = subset

    ###########################################################################
        # first, count the number of samples and classes

        # self.samples = 0
        if not classes:
            with open(csv, 'rt') as csv_open:
                df = pd.read_csv(csv_open, sep=',')
                # filter for shottype
                df_shot = df.loc[df['shottype'] == shotview]
                # get classes, count and put in dict
                classes = df_shot.species.unique()
                self.num_classes = len(classes)
                self.class_indices = dict(zip(classes, range(len(classes))))
                self.samples = _count_pathways_in_csv(csv, split, shotview)

                # TODO shottype incorporation instead of filtering
                shottypes = df_shot.shottype.unique()
                self.num_shottypes = len(shottypes)
                self.shottype_indicies = dict(
                    zip(shottypes, range(len(shottypes))))

        print('Found {0} images belonging to {1} classes for shottype {2}.'.format(
            self.samples, self.num_classes, shotview))

    ###########################################################################
        # second build an index of the images in the different class subfolders
        # results = []
        # self.pathways = []
        # self.classes = np.zeros((self.samples,), dtype='int32')
        i = 0
        # with open(csv, 'rt') as csv_open:
        #     df = pd.read_csv(csv_open, sep=',')
        #     for row in df.itertuples():
        results = _list_pathways_in_csv(
            csv,
            split,
            self.class_indices,
            shotview
        )
        self.classes, self.pathways = results

        # TODO: Fix lines below
        # for res in results:
        #     # 0, species = dict{0: species}.get()
        #     classes, pathways = res.get()
        #     self.classes[i:i + len(classes)] = classes
        #     # self.pathways += pathways
        #     i += len(classes)

        super(CsvIterator, self).__init__(
            self.samples, batch_size, shuffle, seed)

    def _get_batches_of_transformed_samples(self, index_array):
        batch_x = np.zeros((len(index_array),) +
                           self.image_shape, dtype=K.floatx())
        grayscale = self.color_mode == 'grayscale'
        # build batch of image data
        for i, j in enumerate(index_array):
            fname = self.pathways[j]
            img = load_img(fname,
                           grayscale=grayscale,
                           target_size=self.target_size,
                           interpolation=self.interpolation)
            x = img_to_array(img, data_format=self.data_format)
            x = self.image_data_generator.random_transform(x)
            x = self.image_data_generator.standardize(x)
            batch_x[i] = x

        # build batch of labels
        if self.class_mode == 'categorical':
            batch_y = np.zeros(
                (len(batch_x), self.num_classes), dtype=K.floatx())
            # TODO: fix 2 lines below - What do they do?
            # for i, label in enumerate(self.classes[index_array]):
            #     batch_y[i, label] = 1.
        else:
            return batch_x
        return batch_x, batch_y


def trainer_csv(model,
                csv,
                shottype,
                config,
                callbacks=None
                ):
    epochs = config.num_epochs
    batch_size = config.batch_size
    idg_t = MyImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.20
    )
    train_data_generator = idg_t.flow_from_csv(
        csv=csv,
        shotview='head',
        subset='training'
    )
    idg_v = MyImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=0.20
    )
    val_data_generator = idg_v.flow_from_csv(
        csv=csv,
        shotview='head',
        subset='validation'
    )
    model.fit_generator(
        generator=train_data_generator,
        steps_per_epoch=3,
        epochs=epochs,
        validation_data=val_data_generator,
        validation_steps=3,
        callbacks=callbacks
    )


# ImageDataGenerator
###############################################################################


def idg(
    target_gen='training'
):
    """Initialize an augmentation generator for validation. Validation data
    should not be augmentatd, only correctly preprocessed for the model.

    Args:
        target_gen (str): Should be either `training`, `validation`, or
            `test`. Defaults to `training`.

    Returns:
        generator: A Keras image data generator object.

    Raises:
        ValueError: If target_gen is not set correctly.

    """
    if target_gen not in [
        'training',
        'validation',
        'test'
    ]:
        raise ValueError(
            'Argument {} is in invalid  for `target_gen`. It should be one of '
            '`training`, `validation`, or `testing`.'.format(target_gen))
    if target_gen == 'training':
        idg = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True
        )
    if target_gen in ['validation', 'test']:
        idg = ImageDataGenerator(preprocessing_function=preprocess_input)

    return idg


# flow_from_directory part
###############################################################################


def _data_generator_dir(
    dataset,
    config,
    shottype='head',
    target_gen='training'
):
    """Short summary.

    Args:
        dataset (type): Description of parameter `dataset`.
        config (type): Description of parameter `config`.
        shottype (type): Description of parameter `shottype`.
        target_gen (str): Should be either `training`, `validation`, or
            `test`. Defaults to `training`..

    Returns:
        type: Description of returned object.

    """
    batch_size = config.batch_size
    seed = config.seed
    if target_gen == 'training':
        shuffle = True
        dir = '1-training'
    if target_gen == 'validation':
        shuffle = False
        dir = '2-validation'
    if target_gen == 'test':
        shuffle = False
        dir = '3-test'
    data_dir = os.path.join(
        'data',
        dataset,
        'images',
        shottype,
        dir
    )
    idgen = idg(target_gen=target_gen)
    idgen = idgen.flow_from_directory(
        directory=data_dir,
        target_size=(299, 299),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=shuffle,
        seed=1
    )
    classes = idgen.classes
    class_indices = idgen.class_indices
    return idgen, classes, class_indices


def trainer_dir(
    model,
    dataset,
    shottype,
    config,
    callbacks=None
):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.
        dataset (type): Description of parameter `dataset`.
        shottype (type): Description of parameter `shottype`.
        config (type): Description of parameter `config`.
        callbacks (type): Description of parameter `callbacks`. Defaults to
            None.

    Returns:
        type: Description of returned object.

    """
    steps_per_epoch = config.num_iter_per_epoch
    epochs = config.num_epochs
    batch_size = config.batch_size
    train_data_gen_dir, _, _ = _data_generator_dir(
        dataset=dataset,
        shottype=shottype,
        config=config,
        target_gen='training'
    )
    val_data_gen_dir, _, _  = _data_generator_dir(
        dataset=dataset,
        shottype=shottype,
        config=config,
        target_gen='validation'
    )
    history = model.fit_generator(
        generator=train_data_gen_dir,
        steps_per_epoch=steps_per_epoch,  # Fix by using samples // batch size
        epochs=epochs,
        validation_data=val_data_gen_dir,
        validation_steps=steps_per_epoch,  # Fix by using samples // batch size
        callbacks=callbacks
    )

    return history
