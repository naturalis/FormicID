# Experiments

This markdown document show results from different experiments and for different datasets.

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Experiments](#experiments)
- [Low quality image datasets - Number of images](#low-quality-image-datasets-number-of-images)
- [Training shottype `head`](#training-shottype-head)
	- [Settings](#settings)
	- [Events and parameters](#events-and-parameters)
		- [T5_Qlow_AugM_D05_LR0001_E100 - events](#t5qlowaugmd05lr0001e100-events)
		- [T20_Qlow_AugM_D05_LR0001_E100 - events](#t20qlowaugmd05lr0001e100-events)
		- [T50_Qlow_AugM_D05_LR0001_E100 - events](#t50qlowaugmd05lr0001e100-events)
		- [T97_Qlow_AugM_D05_LR0001_E100 - events](#t97qlowaugmd05lr0001e100-events)
	- [Results - Table](#results-table)
	- [Results - Graphs](#results-graphs)
		- [T5_Qlow_AugM_D05_LR0001_E100 - graph](#t5qlowaugmd05lr0001e100-graph)
		- [T20_Qlow_AugM_D05_LR0002_E100 - graph](#t20qlowaugmd05lr0002e100-graph)
			- [T20_Qlow_AugH_D05_LR0001_E100 - graph](#t20qlowaughd05lr0001e100-graph)
			- [T20_Qlow_AugL_D05_LR0001_E100 - graph](#t20qlowaugld05lr0001e100-graph)
			- [T20_Qlow_AugM_D025_LR0001_E100 - graph](#t20qlowaugmd025lr0001e100-graph)
		- [T50_Qlow_AugM_D05_LR0003_E100 - graph](#t50qlowaugmd05lr0003e100-graph)
		- [T97_Qlow_AugM_D05_LR0004_E100 - 1st try - graph](#t97qlowaugmd05lr0004e100-1st-try-graph)
		- [T97_Qlow_AugM_D05_LR0004_E100 - 2nd try - graph](#t97qlowaugmd05lr0004e100-2nd-try-graph)

<!-- /TOC -->

# Low quality image datasets - Number of images

|       Species |  5  |      20      |      50      |        97        |
|-------------: | :-: | :----------: | :----------: | :--------------: |
|        Images | 496 | 3,523       | 6,525       | 10,150         |
| Dorsal images | 496 |     1,175     |   2,176     |    3,384       |
|   Head images | 496 |     1,169     |   2,166     |    3,366       |
|Profile images | 496 |     1,179     |   2,183     |    3,400       |

# Training shottype `head`

## Settings

Training settings were:

- `Augmentation`:
```  
preprocessing_function=preprocess_input,
rotation_range=40,
width_shift_range=0.2,
height_shift_range=0.2,
shear_range=0.2,
zoom_range=0.2,
horizontal_flip=True
```
- `num_epochs`: `10`
- `learning_rate`: `0.001`
- `batch_size`: `64`
- `dropout`: `0.5`
- `optimizer`: `Nadam`
  - `lr` : `learning_rate`,
  - `beta_1` : `0.9`,
  - `beta_2` : `0.999`,
  - `epsilon` : `1e-08`,
  - `schedule_decay` : `0.004`
- `model`: `InceptionV3`
  - With modified top layer as a dense layer with `num_species`.
- `seed`: `1`
- `testsplit`: `0.1`
  - 10 % of the dataset is a test set.
- `validationsplit`: `0.2`
  - 20 % of the dataset is a test set.
- `weights initialization`: `imagenet`

## Events and parameters
4 Datasets are created using the most imaged species on AntWeb. For a `n` species dataset, the `n` most imaged species were used.

### T5_Qlow_AugM_D05_LR0001_E100 - events

- `num_iter_per_epoch`: `8`
- Epoch 00039: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00063: early stopping

### T20_Qlow_AugM_D05_LR0001_E100 - events

- `num_iter_per_epoch`: `18`
- Epoch 00046: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00087: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

### T50_Qlow_AugM_D05_LR0001_E100 - events

- `num_iter_per_epoch`: `34`
- Epoch 00053: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00085: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

### T97_Qlow_AugM_D05_LR0001_E100 - events

**First time**
- `num_iter_per_epoch`: `53`
- Epoch 00069: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.

**Second time**
- `num_iter_per_epoch`: `53`
- Epoch 00064: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00097: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

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

### T5_Qlow_AugM_D05_LR0001_E100 - graph

![5 Species](/docs_experiments/top5species_Qlow.png)

### T20_Qlow_AugM_D05_LR0002_E100 - graph

![20 Species](/docs_experiments/top20species_Qlow.png)

#### T20_Qlow_AugH_D05_LR0001_E100 - graph

```
preprocessing_function=preprocess_input,
rotation_range=45,
width_shift_range=0.3,
height_shift_range=0.3,
shear_range=0.25,
zoom_range=0.25,
horizontal_flip=True
```
![20 Species](/docs_experiments/top20species_Qlow_AugHigh.png)

#### T20_Qlow_AugL_D05_LR0001_E100 - graph

```
preprocessing_function=preprocess_input,
rotation_range=40,
width_shift_range=0.15,
height_shift_range=0.15,
shear_range=0.15,
zoom_range=0.15,
horizontal_flip=True
```
![20 Species](/docs_experiments/top20species_Qlow_AugLow.png)

#### T20_Qlow_AugM_D025_LR0001_E100 - graph

![20 Species](/docs_experiments/top20species_Qlow_DO025.png)

### T50_Qlow_AugM_D05_LR0003_E100 - graph

![50 Species](/docs_experiments/top50species_Qlow.png)

###T97_Qlow_AugM_D05_LR0004_E100 - 1st try - graph

![97 Species](/docs_experiments/top97species_Qlow.png)

### T97_Qlow_AugM_D05_LR0004_E100 - 2nd try - graph

![97 Species](/docs_experiments/top97species_Qlow2.png)
