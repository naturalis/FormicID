################################################################################
#                     __                      _      ___ ____                  #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                 #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |                #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |                #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                 #
#                                                                              #
#                                  Utilitiies                                  #
#                                                                              #
################################################################################
'''
Description:
This file has code for utility functions that can be used in other scripts.

# TODO: load JSON config
'''
def save_model():
    # TODO return save models

def load_model():
    # TODO return load models

def read_model():
    # TODO return read models

def split_validation_set():
    # TODO return split training and validation

def show_image():
    # TODO return show image

def model_summary(model):
    return model.summary()

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
