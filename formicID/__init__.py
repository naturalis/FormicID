################################################################################
#                                                                              #
#                                __init__.py                                   #
#                                                                              #
################################################################################

from __future__ import print_function
from __future__ import absolute_import

__all__ = ['formicID_AntWeb', 'formicID_build', 'formicID_input',
           'formicid_train']

# from formicID.formicID_AntWeb import *
from formicID.formicID_build import neuralNetwork
# from formicID.formicID_input import *
from formicID.formicID_train import build_tensorboard, train_model


__version__ = '0.1.3'
