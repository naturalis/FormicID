import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FormiciID - '
    'Identification of ant images')
    parser.add_argument('', type=str, nargs='+',
                        help='info on the argument')

    args = parser.parse_args()

if __name__ == '__main__':
    print('Keras version: {}'.format(keras.__version__))
