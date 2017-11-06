################################################################################
#                                                                              #
#                        FormicID Evaluation                                   #
#                                                                              #
################################################################################

""" Warning: Validation is integrated in formicID_train."""

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
from formicID.formicID_build import *
from formicID.formicID_input import *
from formicID.formicID_train import *


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////
IMG_HEIGHT, IMG_WIDTH = 120, 148  # input for height and width


# Validation
# //////////////////////////////////////////////////////////////////////////////

AW_generated_data_val = validation_data_generator(validation_data_dir)

def model_evaluate(model):
    loss, accuracy = model.evaluate(X, Y)
    print("\nLoss: {:2f}, Accuracy: {:2f}".format(loss, accuracy*100))

model_evalute(AW_model_trained)
