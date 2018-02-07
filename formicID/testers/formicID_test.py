################################################################################
#                                                                              #
#                        FormicID testing                                   #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////


# Validation
# //////////////////////////////////////////////////////////////////////////////

def model_evaluate(model):
    loss, accuracy = model.evaluate(testdataX, testdataY)
    print("\nLoss: {:2f}, Accuracy: {:2f}".format(loss, accuracy*100))

model_evaluate(AW_model_trained)
