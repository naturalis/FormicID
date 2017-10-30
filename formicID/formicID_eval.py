################################################################################
#                                                                              #
#                        FormicID Validation                                   #
#                                                                              #
################################################################################

# Packages
# //////////////////////////////////////////////////////////////////////////////
from __future__ import print_function
import formicID.formicID_train


# Parameters and settings
# //////////////////////////////////////////////////////////////////////////////

# Validation
# //////////////////////////////////////////////////////////////////////////////
def model_evaluate(model):
    loss, accuracy = model.evaluate(X, Y)
    print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))

model_evalute(AW_model_trained)
