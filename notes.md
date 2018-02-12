# Notes and code lines

# Pigar requirements.txt update
```sh
cd /Users/nijram13/Google\ Drive/4.\ Biologie/Studie\ Biologie/Master\ Year\ 2/Internship\ CNN/8.\ FormicID/FormicID
pigar
```

## Conda update all packages
```sh
conda update --all
```

## Pip update all packages
```sh
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
```

## Tensorboard launch
In order to launch TensorBoard from the terminal, copy:
```sh
tensorboard --logdir="/Users/nijram13/Google Drive/4. Biologie/Studie Biologie/Master Year 2/Internship CNN/8. FormicID/FormicID/graphs/logs"
```