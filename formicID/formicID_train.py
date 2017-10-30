################################################################################
#                                                                              #
#                        FormicID Network Training                             #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
import formicID.formicID_build
import formicID.formicID_input


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
train_data_dir = './data/train'


# Training
# //////////////////////////////////////////////////////////////////////////////
AW_model = build_neural_network()
AW_model_comp = compile_neural_network(AW_model)

x = train_data(train_data_dir)

def train_model(model):
    AW_model_fit = model.fit_generator(
        x,
        steps_per_epoch=5,
        epochs=5,
        #validation_data=validation_generator,
        #validation_steps=10,
        #callbacks=Callbacks_Tensorboard
    )
    return AW_model_fit

AW_model_trained = train_model(AW_model_comp)
