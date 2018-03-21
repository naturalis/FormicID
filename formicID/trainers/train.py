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

# Data tools imports
import pandas as pd

# Parameters and settings
###############################################################################


# csv iterator
###############################################################################

class CsvIterator(Iterator):
    """Iterator capable of reading images from a directory on disk.

    # Args
        directory: Path to the directory to read images from.
            Each subdirectory in this directory will be
            considered to contain images from one class,
            or alternatively you could specify class subdirectories
            via the `classes` argument.
        image_data_generator: Instance of `ImageDataGenerator`
            to use for random transformations and normalization.
        target_size: tuple of integers, dimensions to resize input images to.
        color_mode: One of `"rgb"`, `"grayscale"`. Color mode to read images.
        classes: Optional list of strings, names of subdirectories
            containing images from each class (e.g. `["dogs", "cats"]`).
            It will be computed automatically if not set.
        class_mode: Mode for yielding the targets:
            `"binary"`: binary targets (if there are only two classes),
            `"categorical"`: categorical targets,
            `"sparse"`: integer targets,
            `"input"`: targets are images identical to input images (mainly
                used to work with autoencoders),
            `None`: no targets get yielded (only input images are yielded).
        batch_size: Integer, size of a batch.
        shuffle: Boolean, whether to shuffle the data between epochs.
        seed: Random seed for data shuffling.
        data_format: String, one of `channels_first`, `channels_last`.
        subset: Subset of data (`"training"` or `"validation"`) if
            validation_split is set in ImageDataGenerator.
        interpolation: Interpolation method used to resample the image if the
            target size is different from that of the loaded image.
            Supported methods are "nearest", "bilinear", and "bicubic".
            If PIL version 1.1.3 or newer is installed, "lanczos" is also
            supported. If PIL version 3.4.0 or newer is installed, "box" and
            "hamming" are also supported. By default, "nearest" is used.

    """

    def __init__(self, input_csv, image_data_generator,
                 target_size=(256, 256), color_mode='rgb',
                 classes=None, class_mode='categorical',
                 batch_size=32, shuffle=True, seed=None,
                 data_format=None,
                 follow_links=False,
                 subset=None,
                 interpolation='nearest'):
        if data_format is None:
            data_format = K.image_data_format()
        self.input_csv = input_csv
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
    ####################################################

        # first, count the number of samples and classes
        self.samples = 0

        if not classes:
            with open(input_csv, 'rt') as csv_open:
                df = pd.read_csv(csv_open, sep=',')
                classes_counts = df.species.value_counts()
                classes = df.species.nunique()
                self.num_classes = classes
                counts = df.shottype.value_counts()
                h_count = counts['head']
                d_count = counts['dorsal']
                p_count = counts['profile']
                self.samples = (h_count + d_count + p_count)
        # TODO: count classes after shottype count
        print('Found a total {0} images belonging to {1} classes (head: {2}, dorsal: {3}, profile: {4}).'.format(self.samples, self.num_classes, h_count, d_count, p_count))





        # second, build an index of the images in the different class subfolders
        results = []

        self.filenames = []
        self.classes = np.zeros((self.samples,), dtype='int32')
        i = 0
        for dirpath in (os.path.join(directory, subdir) for subdir in classes):
            results.append(pool.apply_async(_list_valid_filenames_in_directory,
                                            (dirpath, white_list_formats, split,
                                             self.class_indices, follow_links)))
        for res in results:
            classes, filenames = res.get()
            self.classes[i:i + len(classes)] = classes
            self.filenames += filenames
            i += len(classes)

        pool.close()
        pool.join()
        super(DirectoryIterator, self).__init__(
            self.samples, batch_size, shuffle, seed)
    #
    # def _get_batches_of_transformed_samples(self, index_array):
    #     batch_x = np.zeros((len(index_array),) +
    #                        self.image_shape, dtype=K.floatx())
    #     grayscale = self.color_mode == 'grayscale'
    #     # build batch of image data
    #     for i, j in enumerate(index_array):
    #         fname = self.filenames[j]
    #         img = load_img(os.path.join(self.directory, fname),
    #                        grayscale=grayscale,
    #                        target_size=self.target_size,
    #                        interpolation=self.interpolation)
    #         x = img_to_array(img, data_format=self.data_format)
    #         x = self.image_data_generator.random_transform(x)
    #         x = self.image_data_generator.standardize(x)
    #         batch_x[i] = x
    #
    #     # build batch of labels
    #     if self.class_mode == 'input':
    #         batch_y = batch_x.copy()
    #     elif self.class_mode == 'sparse':
    #         batch_y = self.classes[index_array]
    #     elif self.class_mode == 'binary':
    #         batch_y = self.classes[index_array].astype(K.floatx())
    #     elif self.class_mode == 'categorical':
    #         batch_y = np.zeros(
    #             (len(batch_x), self.num_classes), dtype=K.floatx())
    #         for i, label in enumerate(self.classes[index_array]):
    #             batch_y[i, label] = 1.
    #     else:
    #         return batch_x
    #     return batch_x, batch_y



# Training data
###############################################################################


def idg_train():
    """Initialize an augmentation generator for training.

    Augmentation options:
        rescale: Rescaling factor; normalizing the data to [0:1]
        rotation_range: degree range for random rotations (integer)
        width_shift_range: range for random horizontal shifts (float)
        height_shift_range: range for random vertical shifts (float)
        shear_range: shear intensity (float)
        zoom_range: range for random zoom (float)
        horizontal_flip: randomly flip inputs horizontally (boolean)

    Returns:
        generator: A Keras image data generator object.

    """
    idg = ImageDataGenerator(preprocessing_function=preprocess_input,
                             rotation_range=40,
                             width_shift_range=0.2,
                             height_shift_range=0.2,
                             shear_range=0.2,
                             zoom_range=0.2,
                             horizontal_flip=True)

    return idg


def train_data_generator(X_train,
                         Y_train,
                         config):
    """Configueres the training generator for taking image and label data.

    Args:
        X_train (array): Image data as 4D numpy array.
        Y_train (array): Label data as 2D numpy array.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        generator: A image data generator with its `.flow` method applied.

    """
    batch_size = config.batch_size
    seed = config.seed
    idgen_train = idg_train()

    # .flow() takes npdata en label arrays, and generates batches for
    # augmented/normalized data. Yields batches indefinitely, in an infinite
    # loop.
    idgen_train = idgen_train.flow(X_train,
                                   Y_train,
                                   batch_size=batch_size,
                                   seed=seed)
    return idgen_train


# Validation data
###############################################################################


def idg_val():
    """Initialize an augmentation generator for validation. Validation data
    should not be augmentatd, only correctly preprocessed for the model.

    Returns:
        generator: A Keras image data generator object.

    """
    idg = ImageDataGenerator(preprocessing_function=preprocess_input)

    return idg


def val_data_generator(X_val,
                       Y_val,
                       config):
    """Configueres the validation generator for taking image and label data.

    Args:
        X_val (array): Image data as 4D numpy array.
        Y_val (array): Label data as 2D numpy array.
        config (Bunch object): The JSON configuration Bunch object.

    Returns:
        generator: A image data generator with its `.flow` method applied.

    """
    batch_size = config.batch_size
    seed = config.seed
    idgen_val = idg_val()

    idgen_val = idgen_val.flow(X_val,
                               Y_val,
                               batch_size=batch_size,
                               seed=config.seed)

    return idgen_val

# Trainer
###############################################################################


def trainer(model,
            X_train,
            Y_train,
            X_val,
            Y_val,
            config,
            callbacks=None):
    """Initializes training on a model with training and validation image +
    label data as input.

    Args:
        model (Keras model instance): A Keras model instance.
        X_train (array): 4D numpy array training data for images.
        Y_train (array): 2D numpy array training data for labels.
        X_val (array): 4D numpy array validation data for images.
        Y_val (array): 2D numpy array validation data for labels.
        config (Bunch object): The JSON configuration Bunch object.
        callbacks (Callback object): One or a list of Keras Callback Objects.
            Defaults to `None`.

    Returns:
        training instance: Applies the `.fit_generator` method to a Keras
            model instance.

    """
    epochs = config.num_epochs
    batch_size = config.batch_size
    nb_X_train = len(X_train)

    train_data_gen = train_data_generator(X_train=X_train,
                                          Y_train=Y_train,
                                          config=config)

    val_data_gen = val_data_generator(X_val=X_val,
                                      Y_val=Y_val,
                                      config=config)

    model.fit_generator(train_data_gen,
                        validation_data=val_data_gen,
                        steps_per_epoch=(nb_X_train // batch_size),
                        epochs=epochs,
                        callbacks=callbacks)

# flow_from_directory part
###############################################################################


def _train_data_generator_dir(data_dir,
                              shottype,
                              config
                              ):
    """Short summary.

    Args:
        data_dir (type): Description of parameter `data_dir`.
        shottype (type): Description of parameter `shottype`.
        config (type): Description of parameter `config`.

    Returns:
        type: Description of returned object.

    """
    batch_size = config.batch_size
    seed = config.seed
    idgen_train = idg_train()
    data_dir = os.path.join('data',
                            data_dir,
                            'images',
                            shottype,
                            '1-training')
    idgen_train = idgen_train.flow_from_directory(
        directory=data_dir,
        target_size=(299, 299),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=batch_size,
        seed=1
    )

    return idgen_train


def _val_data_generator_dir(data_dir,
                            shottype,
                            config
                            ):
    """Short summary.

    Args:
        data_dir (type): Description of parameter `data_dir`.
        shottype (type): Description of parameter `shottype`.
        config (type): Description of parameter `config`.

    Returns:
        type: Description of returned object.

    """
    batch_size = config.batch_size
    seed = config.seed
    idgen_val = idg_val()
    data_dir = os.path.join('data',
                            data_dir,
                            'images',
                            shottype,
                            '2-validation')
    idgen_val = idgen_val.flow_from_directory(
        directory=data_dir,
        target_size=(299, 299),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=batch_size,
        seed=1
    )

    return idgen_val


def trainer_dir(model,
                data_dir,
                shottype,
                config,
                callbacks=None
                ):
    """Short summary.

    Args:
        model (type): Description of parameter `model`.
        data_dir (type): Description of parameter `data_dir`.
        shottype (type): Description of parameter `shottype`.
        config (type): Description of parameter `config`.
        callbacks (type): Description of parameter `callbacks`. Defaults to
            None.

    Returns:
        type: Description of returned object.

    """
    epochs = config.num_epochs
    batch_size = config.batch_size
    train_data_gen_dir = _train_data_generator_dir(data_dir=data_dir,
                                                   shottype=shottype,
                                                   config=config
                                                   )
    val_data_gen_dir = _val_data_generator_dir(data_dir=data_dir,
                                               shottype=shottype,
                                               config=config
                                               )
    model.fit_generator(
        generator=train_data_gen_dir,
        steps_per_epoch=32,
        epochs=epochs,
        validation_data=val_data_gen_dir,
        validation_steps=32,
        callbacks=callbacks
    )
