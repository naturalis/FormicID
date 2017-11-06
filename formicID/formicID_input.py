################################################################################
#                                                                              #
#                              FormicID input                                  #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
from keras.preprocessing.image import ImageDataGenerator
# from keras.preprocessing.image import array_to_img, img_to_array, load_img

"""
    Beforehand images should be divided in 5:1:1 subsets (train:val:test) and put in the right directories
    load images from a directory
    target_size reshapes the images to a certain dimension

    ToDo:
    Create test set code
    The directory structure:

    data/
        train/
            speciesX/
                speciesX0001.jpg
                speciesX0002.jpg
                ...
            speciesY/
                speciesY0001.jpg
                speciesY0002.jpg
                ...
        validation/
            speciesX/
                speciesX0001.jpg
                speciesX0002.jpg
                ...
            speciesY/
                speciesY0001.jpg
                speciesY0002.jpg
                ...

"""

# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
SEED = 1
IMG_HEIGHT, IMG_WIDTH = 120, 148  # input for width and height
validation_data_dir = './data/validation'
BATCH_SIZE = 32

# Train en test data augumentation
# //////////////////////////////////////////////////////////////////////////////
train_datagen = ImageDataGenerator(
    """
rescale: Rescaling factor; normalizing the data to [0:1]
rotation_range: degree range for random rotations (integer)
width_shift_range: range for random horizontal shifts (float)
height_shift_range: range for random vertical shifts (float)
shear_range: shear intensity (float)
zoom_range: range for random zoom (float)
horizontal_flip: randomly flip inputs horizontally (boolean)
"""
    rescale=1. / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Don't augment the testdata. Only rescale to normalize the data
test_datagen = ImageDataGenerator(
    rescale=1. / 255
)


# Train en validation datagenerators
# //////////////////////////////////////////////////////////////////////////////
def train_data_generator(directory):
    """
    input = link to a folder containing a set of validation images

    target_size resizes images to new dimensions
    class_mode must be 'categorical' because of 2D data

    # Don't set classes. It will take the classes from subdirectories.
    # save_dir= 'dir' # can use to save the augmentated images
    # also use (save_prefix, save_format) then

    """
    train_generator = train_datagen.flow_from_directory(
        directory,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    return train_generator


def validation_data_generator(directory):
    """
    input = link to a folder containing a set of validation images

    target_size resizes images to new dimensions
    class_mode must be 'categorical' because of 2D data

    # Don't set classes. It will take the classes from subdirectories.
    # save_dir= 'dir' # can use to save the augmentated images
    # also use (save_prefix, save_format) then

    """
    validation_generator = test_datagen.flow_from_directory(
        directory,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    return validation_generator


"""

Visualizing data agumentation

# Data augmentation
# //////////////////////////////////////////////////////////////////////////////
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

# this is a PIL image
img = load_img('data/train/lasiusflavus/lasiusflavus1.jpg')

# this is a Numpy array with shape (3, 150, 150)
x = img_to_array(img)

# this is a Numpy array with shape (1, 3, 150, 150)
x = x.reshape((1,) + x.shape)

# the .flow() command below generates batches of randomly transformed images
# and saves the results to the `preview/` directory
i = 0
for batch in datagen.flow(x, batch_size=1,
                          save_to_dir='preview',
                          save_prefix='lasiusflavus',
                          save_format='jpeg'):
    i += 1
    if i > 20:
        break  # otherwise the generator would loop indefinitely
"""
