# Experiments

This markdown document shows results from different experiments and different datasets. Experiments are named as follow:

`number_of_species` `_` `castes` `_` `shottype` `_` `quality` `_` `Aug` `_` `Dropout` `_` `LR` `_` `epochs`

So
`T5_CaAll_QuL_ShH_AugM_D05_LR0001_E100` means:
- `5` Species
- all castes
- shottype: `head`
- low quality images
- medium augmentation attacks
- dropout `0.5`
- learning rate of `0.001`
- set for `100` epochs

# Tabel of Contents
<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Experiments](#experiments)
- [Tabel of Contents](#tabel-of-contents)
- [Low quality image datasets - Number of images](#low-quality-image-datasets-number-of-images)
- [Augmentation example](#augmentation-example)
- [Training shottype `head`](#training-shottype-head)
	- [Settings](#settings)
- [With following settings:](#with-following-settings)
- [Augmentation as below:](#augmentation-as-below)
	- [Results - Table](#results-table)
	- [Results - Graphs](#results-graphs)
		- [5 Species](#5-species)
			- [T5_CaAll_QuL_ShH_AugM_D05_LR0001_E100](#t5caallqulshhaugmd05lr0001e100)
		- [20 species](#20-species)
			- [T20_CaAll_QuL_ShH_AugM_D05_LR0001_E100](#t20caallqulshhaugmd05lr0001e100)
			- [T20_CaAll_QuL_ShH_AugH_D05_LR0001_E100](#t20caallqulshhaughd05lr0001e100)
			- [T20_CaAll_QuL_ShH_AugL_D05_LR0001_E100](#t20caallqulshhaugld05lr0001e100)
			- [T20_CaAll_QuL_ShH_AugM_D00_LR0001_E100](#t20caallqulshhaugmd00lr0001e100)
			- [T20_CaAll_QuL_ShH_AugM_D025_LR0001_E100](#t20caallqulshhaugmd025lr0001e100)
			- [T20_CaAll_QuL_ShH_AugM_D075_LR0001_E100](#t20caallqulshhaugmd075lr0001e100)
			- [T20_CaAll_QuL_ShH_AugM_D05_LR00001_E100](#t20caallqulshhaugmd05lr00001e100)
			- [T20_CaAll_QuL_ShH_AugH_D075_LR0001_E100](#t20caallqulshhaughd075lr0001e100)
			- [T20_CaAll_QuL_ShH_AugH_D025_LR0001_E100](#t20caallqulshhaughd025lr0001e100)
			- [T20_CaAll_QuL_ShH_AugH_D025_LR00005_E100](#t20caallqulshhaughd025lr00005e100)
		- [50 Species](#50-species)
			- [T50_CaAll_QuL_ShH_AugM_D05_LR0001_E100](#t50caallqulshhaugmd05lr0001e100)
		- [97 Species](#97-species)
			- [T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100 - 1st try](#t97caallqulshhaugmd05lr0001e100-1st-try)
			- [T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100 - 2nd try](#t97caallqulshhaugmd05lr0001e100-2nd-try)
			- [T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100_I4](#t97caallqulshhaugmd05lr0001e100i4)
			- [T97_CaAll_QuM_ShH_AugM_D05_LR0001_E100_I4](#t97caallqumshhaugmd05lr0001e100i4)
		- [97 species confusion matrix](#97-species-confusion-matrix)
		- [Test image](#test-image)

<!-- /TOC -->
# Low quality image datasets - Number of images

|       Species |  5  |      20      |      50      |        97        |
|-------------: | :-: | :----------: | :----------: | :--------------: |
|        Images | 496 | 3,523       | 6,525       | 10,150         |
| Dorsal images | 496 |     1,175     |   2,176     |    3,384       |
|   Head images | 496 |     1,169     |   2,166     |    3,366       |
|Profile images | 496 |     1,179     |   2,183     |    3,400       |
|num_iter_per_epoch | 8 | 18 | 34 | 53 |

# Augmentation example

![](/docs_experiments/augmentation.png)

# Training shottype `head`

## Settings

Training settings were mostly as mentioned below. Some of the parameters changes as the optimal parameter is searched.

```python
number_of_species="97" # $ datasets: 5, 20, 50 or 97 species
image_quality="low"
castes="all"
num_epochs=100
learning_rate=0.001 # Variates in between experiments
batch_size=64
dropout=0.5 # Variates in between experiments
optimizer="Nadam"
# With following settings:
	lr =learning_rate,
	beta_1 =0.9,
	beta_2 =0.999,
	epsilon =1e-08,
	schedule_decay =0.004
model=InceptionV3 # With modified top layers dropout and a dense layer with num_species.
seed=1
testsplit=0.1
validationsplit=0.2
weights initialization="imagenet"
The prelast Dense Layer activation="relu" or PReLU
# Augmentation as below:
rotation_range=40,
width_shift_range=0.2, # Variates in between experiments
height_shift_range=0.2, # Variates in between experiments
shear_range=0.2, # Variates in between experiments
zoom_range=0.2, # Variates in between experiments
horizontal_flip=True # Variates in between experiments
```

## Results - Table

|           Species |    5   |   20   |   50   | 97 1st | 97 2nd   |
|------------------:|:------:|:------:|:------:|:------:|:-----:   |
|       Head images |    496 |   1169 |   2166 |   3366 | 3366	   |
|   Training images |    347 |    820 |   1516 |   2353 | 2353	   |
|                   |        |        |        |        |		   |
| Validation images |    101 |    235 |    435 |    683 | 683	   |
|              Loss |  0.776 | 0.9002 | 1.5451 | 1.9957 | 2.3290   |
|          Accuracy | 0.8515 | 0.8214 | 0.7039 | 0.6944 | 0.6378   |
|    Top 3 Accuracy | 0.9901 | 0.9331 | 0.8982 | 0.8501 | 0.8416   |
|                   |        |        |        |        |		   |
|       Test images |     48 |    114 |    215 |    330 |	330	   |
|              Loss | 0.7963 | 0.7521 | 1.7074 | 1.8156 | 2.0839   |
|          Accuracy | 0.8750 | 0.7982 | 0.7023 | 0.7242 | 0.6879   |
|    Top 3 Accuracy | 0.9792 | 0.9737 | 0.8791 | 0.8879 | 0.8667   |

## Results - Graphs
The graphs shows epochs vs loss and accuracy (top-1 and top-3) for training (solid lines) and validation (dashed lines).


### 5 Species

#### T5_CaAll_QuL_ShH_AugM_D05_LR0001_E100
- Epoch 00039: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00063: early stopping

![](/docs_experiments/T5_CaAll_QuL_ShH_AugM_D05_LR0001_E100.png)

### 20 species

#### T20_CaAll_QuL_ShH_AugM_D05_LR0001_E100
- Epoch 00046: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00087: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

![](/docs_experiments/T20_CaAll_QuL_ShH_AugM_D05_LR0001_E100.png)

#### T20_CaAll_QuL_ShH_AugH_D05_LR0001_E100

```python
rotation_range=45,
width_shift_range=0.3,
height_shift_range=0.3,
shear_range=0.25,
zoom_range=0.25,
horizontal_flip=True
```
![](/docs_experiments/T20_CaAll_QuL_ShH_AugH_D05_LR0001_E100.png)

#### T20_CaAll_QuL_ShH_AugL_D05_LR0001_E100

```python
rotation_range=40,
width_shift_range=0.15,
height_shift_range=0.15,
shear_range=0.15,
zoom_range=0.15,
horizontal_flip=True
```
![](/docs_experiments/T20_CaAll_QuL_ShH_AugL_D05_LR0001_E100.png)


#### T20_CaAll_QuL_ShH_AugM_D00_LR0001_E100
- Epoch 00047: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00087: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

![](/docs_experiments/T20_CaAll_QuL_ShH_AugM_D00_LR0001_E100.png)

#### T20_CaAll_QuL_ShH_AugM_D025_LR0001_E100
- Epoch 00085: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00091: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

![](/docs_experiments/T20_CaAll_QuL_ShH_AugM_D025_LR0001_E100.png)

#### T20_CaAll_QuL_ShH_AugM_D075_LR0001_E100

Epoch 00043: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00091: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

![](/docs_experiments/T20_CaAll_QuL_ShH_AugM_D075_LR0001_E100.png)

#### T20_CaAll_QuL_ShH_AugM_D05_LR00001_E100
- Epoch 00033: ReduceLROnPlateau reducing learning rate to `9.999999747378752e-06`.
- Epoch 00057: early stopping

![](/docs_experiments/T20_CaAll_QuL_ShH_AugM_D05_LR00001_E100.png)


#### T20_CaAll_QuL_ShH_AugH_D075_LR0001_E100
```python
rotation_range=40,
width_shift_range=0.35,
height_shift_range=0.35,
shear_range=0.35,
zoom_range=0.35,
horizontal_flip=True
```
- Epoch 00093: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.

![](/docs_experiments/T20_CaAll_QuL_ShH_AugH_D075_LR0001_E100.png)

#### T20_CaAll_QuL_ShH_AugH_D025_LR0001_E100
```python
rotation_range=40,
width_shift_range=0.35,
height_shift_range=0.35,
shear_range=0.35,
zoom_range=0.35,
horizontal_flip=True
```
- Epoch 00069: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.

![](/docs_experiments/T20_CaAll_QuL_ShH_AugH_D025_LR0001_E100.png)

#### T20_CaAll_QuL_ShH_AugH_D025_LR00005_E100
```python
rotation_range=40,
width_shift_range=0.35,
height_shift_range=0.35,
shear_range=0.35,
zoom_range=0.35,
horizontal_flip=True
```
- Epoch 00048: ReduceLROnPlateau reducing learning rate to `5.0000002374872565e-05`.
- Epoch 00087: ReduceLROnPlateau reducing learning rate to `5.000000237487257e-06`.

![](/docs_experiments/T20_CaAll_QuL_ShH_AugH_D025_LR00005_E100.png)

#### T20_CaAll_QuL_ShH_AugM_D05_LR00001_E100_I4_Eve
Training with the Eve optimizer as follows:

```python
lr=0.0001,  	# Important!
beta_1=0.9,
beta_2=0.999,
beta_3=0.999,
small_k=0.1,
big_K=10,
epsilon=1e-8,
decay=0.0001 	# Important!
```

- Epoch 00053: ReduceLROnPlateau reducing learning rate to `9.999999747378752e-06`.

![](/docs_experiments/T20_CaAll_QuL_ShH_AugM_D05_LR00001_E100_I4_Eve.png)


### 50 Species

#### T50_CaAll_QuL_ShH_AugM_D05_LR0001_E100
- Epoch 00053: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00085: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

![](/docs_experiments/T50_CaAll_QuL_ShH_AugM_D05_LR0001_E100.png)

### 97 Species
#### T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100 - 1st try
- Epoch 00069: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.

![](/docs_experiments/T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100.png)

#### T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100 - 2nd try
- Epoch 00064: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00097: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

![](/docs_experiments/T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100-2.png)

#### T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100_I4
- InceptionResNetV2 did not work with `batch_size = 64` due to memory issues. So `batch_size = 32` was used.
- Epoch 00043: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00082: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

![](/docs_experiments/T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100_I4.png)

#### T97_CaAll_QuM_ShH_AugM_D05_LR0001_E100_I4
- Epoch 00044: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00090: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

![](/docs_experiments/T97_CaAll_QuM_ShH_AugM_D05_LR0001_E100_I4.png)


### 97 species confusion matrix
- created from [T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100_I4](#T97_CaAll_QuL_ShH_AugM_D05_LR0001_E100_I4)

![](/docs_experiments/confusion_matrix_test.png)

### Test image
Below is an example of an external image, tested in the model. When trained with high accuracy, this could be used to identify new material.
The image is taken from:

`https://upload.wikimedia.org/wikipedia/commons/f/fd/Camponotus_atriceps_casent0173392_head_1.jpg`

![](/docs_experiments/testimage.png)
