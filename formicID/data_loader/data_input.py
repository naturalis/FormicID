################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  data_input                                  #
################################################################################
'''
Description:
<placeholder txt>
'''

"""
    Beforehand images should be divided in 5:1:1 subsets (train:val:test) and put in the right directories
    load images from a directory
    target_size reshapes the images to a certain dimension

    ToDo:
    Create test set code
    The directory structure:

    data/
        head/
            speciesX/
                speciesX0001.jpg
                speciesX0002.jpg
                ...
            speciesY/
                speciesY0001.jpg
                speciesY0002.jpg
                ...
        dorsal/
            speciesX/
                speciesX0001.jpg
                speciesX0002.jpg
                ...
            speciesY/
                speciesY0001.jpg
                speciesY0002.jpg
                ...

"""
# Packages
# //////////////////////////////////////////////////////////////////////////////
import os
import cv2
import numpy as np
# from keras.preprocessing.image import ImageDataGenerator
# from keras.utils import to_categorical # one-hot encoding
# from keras.preprocessing.image import array_to_img, img_to_array, load_img

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
wd = os.getcwd()

seed = 1

# Load images
# //////////////////////////////////////////////////////////////////////////////


def image_loader(shottype, datadir):
    # TODO: SPLIT into training / validation / test

    data_dir = os.path.join(wd, 'data', datadir, 'images')
    if shottype == 'h':
        data_dir = os.path.join(data_dir, 'head')
    if shottype == 'd':
        data_dir = os.path.join(data_dir, 'dorsal')
    if shottype == 'p':
        data_dir = os.path.join(data_dir, 'profile')

    X_train = []
    Y_train = []
    print('Reading images from "{}"'.format(data_dir))
    for species in os.listdir(data_dir):
        for image in os.listdir(os.path.join(data_dir, species)):
            if '.jpg' in image:
                img = cv2.imread(os.path.join(data_dir, species, image))
                # returns BGR instead of RGB
                if img is not None:
                    # img = img[:, :, ::-1]  # Convert to RGB
                    X_train.append(img)
            label = species
            Y_train.append(label)
    return X_train, Y_train


X_train, Y_train = image_loader(shottype='h', datadir='2018-02-12-test')

print('Number of X_train: {}'.format(len(X_train)))
print('Number of Y_train: {}'.format(len(Y_train)))
# print(Y_train)
#
# cv2.imshow('image', X_train[200])
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# # Train en test data augumentation
# # //////////////////////////////////////////////////////////////////////////////
# """
# rescale: Rescaling factor; normalizing the data to [0:1]
# rotation_range: degree range for random rotations (integer)
# width_shift_range: range for random horizontal shifts (float)
# height_shift_range: range for random vertical shifts (float)
# shear_range: shear intensity (float)
# zoom_range: range for random zoom (float)
# horizontal_flip: randomly flip inputs horizontally (boolean)
# """
# train_datagen = ImageDataGenerator(
#     rescale=1. / 255,
#     rotation_range=40,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True
# )
#
# # Don't augment the testdata. Only rescale to normalize the data
# validation_gen = ImageDataGenerator(
#     rescale=1. / 255
# )
#
#
# # Train en validation datagenerators
# # //////////////////////////////////////////////////////////////////////////////
# def train_data_generator(directory):
#     """
#     input = link to a folder containing a set of validation images
#
#     target_size resizes images to new dimensions
#     class_mode must be 'categorical' because of 2D data
#
#     # Don't set classes. It will take the classes from subdirectories.
#     # save_dir= 'dir' # can use to save the augmentated images
#     # also use (save_prefix, save_format) then
#
#     """
#     train_generator = train_datagen.flow_from_directory(
#         directory,
#         target_size=(img_height, img_width),
#         batch_size=batch_size,
#         class_mode='categorical'
#     )
#     return train_generator
#
#
# def validation_data_generator(directory):
#     """
#     input = link to a folder containing a set of validation images
#
#     target_size resizes images to new dimensions
#     class_mode must be 'categorical' because of 2D data
#
#     # Don't set classes. It will take the classes from subdirectories.
#     # save_dir= 'dir' # can use to save the augmentated images
#     # also use (save_prefix, save_format) then
#
#     """
#     validation_generator = validation_gen.flow_from_directory(
#         directory,
#         target_size=(img_height, img_width),
#         batch_size=batch_size,
#         class_mode='categorical'
#     )
#     return validation_generator
#
#
# """
#
# Visualizing data agumentation
#
# # Data augmentation
# # //////////////////////////////////////////////////////////////////////////////
# datagen = ImageDataGenerator(
#     rotation_range=40,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     fill_mode='nearest')
#
# # this is a PIL image
# img = load_img('data/train/lasiusflavus/lasiusflavus1.jpg')
#
# # this is a Numpy array with shape (3, 150, 150)
# x = img_to_array(img)
#
# # this is a Numpy array with shape (1, 3, 150, 150)
# x = x.reshape((1,) + x.shape)
#
# # the .flow() command below generates batches of randomly transformed images
# # and saves the results to the `preview/` directory
# i = 0
# for batch in datagen.flow(x, batch_size=1,
#                           save_to_dir='preview',
#                           save_prefix='lasiusflavus',
#                           save_format='jpeg'):
#     i += 1
#     if i > 20:
#         break  # otherwise the generator would loop indefinitely
# """
