################################################################################
#                                                                              #
#                                  main.py                                     #
#                          Main will run everything                            #
#                                                                              #
################################################################################

from keras import __version__ as keras_version

def run():
    """
    Run everything
    """
    AW_network = neuralNetwork(NUM_SPECIES=3,
                               input_shape=(3,IMG_HEIGHT,IMG_WIDTH),
                               optimizer="Nadam")
 
    AW_network.build_neural_network()
    AW_network.compile_neural_network()


if __name__ == '__main__':
    print('Keras version: {}'.format(keras_version))
    run()
