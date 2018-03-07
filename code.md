# Notes and code lines

## Run main.py

```sh
cd /Users/nijram13/Google\ Drive/4.\ Biologie/Studie\ Biologie/Master\ Year\ 2/Internship\ CNN/8.\ FormicID/FormicID
python3 formicID/main.py -c formicID/configs/config.json
```

## Pigar requirements.txt update

```sh
cd /Users/nijram13/Google\ Drive/4.\ Biologie/Studie\ Biologie/Master\ Year\ 2/Internship\ CNN/8.\ FormicID/FormicID
pigar
```

## Tensorboard launch

In order to launch TensorBoard from the terminal, copy:

```sh
tensorboard --logdir="experiments/test1/summary" --port=6006
```

## Pip3 update all packages

```sh
pip3 freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
```

## Delete all .DS_Store in project folders

```sh
cd /Users/nijram13/Google\ Drive/4.\ Biologie/Studie\ Biologie/Master\ Year\ 2/Internship\ CNN/8.\ FormicID/FormicID
find . -name '.DS_Store' -type f -delete
```
