# Notes and code lines

## Run main.py

```shell
$ cd /Users/nijram13/Google\ Drive/4.\ Biologie/Studie\ Biologie/Master\ Year\ 2/Internship\ CNN/8.\ FormicID/FormicID
$ python3 formicID/main.py -c formicID/configs/config.json
```

## Pigar requirements.txt update

```shell
$ cd /Users/nijram13/Google\ Drive/4.\ Biologie/Studie\ Biologie/Master\ Year\ 2/Internship\ CNN/8.\ FormicID/FormicID
$ pigar
```

## Tensorboard launch

In order to launch TensorBoard from the terminal, copy:

```shell
$ tensorboard --logdir="experiments/test5sp/summary" --port=6006
```

## Pip3 update all packages

```shell
$ pip3 freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip3 install -U
```

## Delete all .DS_Store in project folders

```shell
$ cd /Users/nijram13/Google\ Drive/4.\ Biologie/Studie\ Biologie/Master\ Year\ 2/Internship\ CNN/8.\ FormicID/FormicID
$ find . -name '.DS_Store' -type f -delete
```
