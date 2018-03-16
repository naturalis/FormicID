# Notes and code lines

Below are some lines that I run a lot.

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Notes and code lines](#notes-and-code-lines)
	- [Running formiCID](#running-formicid)
		- [Changing the current directory](#changing-the-current-directory)
			- [MacOS](#macos)
			- [Windows 10](#windows-10)
		- [Running the script](#running-the-script)
			- [MacOS](#macos)
			- [Windows](#windows)
		- [Tensorboard launch](#tensorboard-launch)
	- [Dependancies](#dependancies)
		- [Pip3 update all packages](#pip3-update-all-packages)
		- [Pigar requirements.txt update](#pigar-requirementstxt-update)
	- [Additional](#additional)
		- [Delete all .DS_Store in project folders](#delete-all-dsstore-in-project-folders)

<!-- /TOC -->

## Running formiCID

### Changing the current directory

#### MacOS

```shell
$ cd /Users/nijram13/Google\ Drive/4.\ Biologie/Studie\ Biologie/Master\ Year\ 2/Internship\ CNN/8.\ FormicID/FormicID
```

#### Windows 10

```shell
$ cd C:\Users\admin.marijn.boer\Github\FormicID
```

### Running the script

#### MacOS

```shell
$ python3 formicID/main.py -c formicID/configs/config.json
```

#### Windows

```shell
$ python formicID\main.py -c formicID\configs\config.json
```

### Tensorboard launch

In order to launch TensorBoard from the terminal, copy the line below and replace the `test` with the correct experiment name:

```shell
$ tensorboard --logdir="experiments/test/summary" --port=6006
```

## Dependancies

### Pip3 update all packages

```shell
$ pip3 freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip3 install -U
```

### Pigar requirements.txt update
In order to automatically update the requirements.txt file, run `pigar` in the project working directory.
```shell
$ pigar
```

## Additional

### Delete all .DS_Store in project folders
These files happen to break the script as it sometimes needs to know which files there are in a folder, and how many. These files cause no harm, as they store information on MacOS on how the finder window is set. They can be deleted savely. *Run this script only in the project folder directory!*

```shell
$ find . -name '.DS_Store' -type f -delete
```
