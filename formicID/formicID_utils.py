def save_model():
    #save models

def load_model():
    #load models

def read_model():
    #read models

def split_validation_set():
    #split training and validation

def show_image():
    #show image

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
