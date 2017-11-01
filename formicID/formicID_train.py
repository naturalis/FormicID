################################################################################
#                                                                              #
#                        FormicID Network Training                             #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
from formicID.formicID_build import *
from formicID.formicID_input import *
from keras.callbacks import TensorBoard
from datetime import datetime


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
train_data_dir = './data/train'


# Training
# //////////////////////////////////////////////////////////////////////////////
AW_model = build_neural_network()
AW_model_comp = compile_neural_network(AW_model)

x = train_data_generator(train_data_dir)

# Callbacks
def build_tensorboard(model):
    """
    In order to launch TensorBoard from the terminal:
    "tensorboard --logdir="/Users/nijram13/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/8. FormicID/FormicID/graphs/logs""
    """
    AW_tensorboard = TensorBoard(
                    log_dir='./graphs/logs/{0}'.format(datetime.now()),
                    histogram_freq=0, batch_size=32,
                    write_graph=True, write_images=True)
    AW_tensorboard.set_model(model)
    Callbacks_Tensorboard = []
    Callbacks_Tensorboard.append(AW_tensorboard)
    return Callbacks_Tensorboard



def train_model(model):
    AW_model_fit = model.fit_generator(
        x,
        steps_per_epoch=5,
        epochs=5,
        #validation_split=(1/7), # 1/7th of the total (which divides
        # everything in 5:1:1 (train:val:test))
        #validation_data=validation_generator,
        #validation_steps=10,
        callbacks=build_tensorboard(model)
    )
    return AW_model_fit

AW_model_trained = train_model(AW_model_comp)
