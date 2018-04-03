# Experiments

This markdown document show results from different experiments and for different datasets.

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Experiments](#experiments)
- [Low quality images](#low-quality-images)
	- [Low quality image datasets - parameters and events](#low-quality-image-datasets-parameters-and-events)
		- [Low quality image datasets - Number of images](#low-quality-image-datasets-number-of-images)
	- [Head view - Low quality](#head-view-low-quality)
		- [Settings](#settings)
		- [Results - Table](#results-table)
		- [Results - Grahps](#results-grahps)
			- [5 Species](#5-species)
			- [20 Species](#20-species)
			- [50 Species](#50-species)
			- [97 Species](#97-species)
		- [Remarks](#remarks)

<!-- /TOC -->

# Low quality images

## Low quality image datasets - Number of images

|       Species |  5  |      20      |      50      |        97        |
|-------------: | :-: | :----------: | :----------: | :--------------: |
|        Images | 496 | 3638 (3523?) | 6526 (6525?) | 10,151 (10,150?) |
| Dorsal images | 496 |     1175     |     2176     |       3384       |
|   Head images | 496 |     1169     |     2166     |       3366       |
|Profile images | 496 |     1179     |     2183     |       3400       |

## Training shottype `head`

### Events and parameters
4 Datasets are created using the most imaged species on AntWeb. For a `n` species dataset, the `n` most imaged species were used.

#### 5 species
- `num_iter_per_epoch`: `8`
- Epoch 00039: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00063: early stopping

#### 20 species
- num_iter_per_epoch: `13` (should have been 18)

#### 50 species
- `num_iter_per_epoch`: `34`
- Epoch 00053: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00085: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

#### 97 species
- `num_iter_per_epoch`: `53`
- Epoch 00069: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.

### Settings

Training settings were:

- `Augmentation`: `small`
  - Image data is not strongly augmented.
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

### Results - Table

|           Species |    5   |   20   |   50   |   97   |
|------------------:|:------:|:------:|:------:|:------:|
|       Head images |    496 |   1169 |   2166 |   3366 |
|   Training images |    347 |    820 |   1516 |   2353 |
|                   |        |        |        |        |
| Validation images |    101 |    235 |    435 |    683 |
|              Loss |  0.776 | 1.5883 | 1.5451 | 1.9957 |
|          Accuracy | 0.8515 | 0.6591 | 0.7039 | 0.6944 |
|    Top 3 Accuracy | 0.9901 | 0.8529 | 0.8982 | 0.8501 |
|                   |        |        |        |        |
|       Test images |        |        |        |        |
|              Loss | 0.7963 | 1.5229 | 1.7074 | 1.8156 |
|          Accuracy | 0.8750 | 0.6754 | 0.7023 | 0.7242 |
|    Top 3 Accuracy | 0.9792 | 0.8509 | 0.8791 | 0.8879 |

### Results - Graphs
X-axis are the epochs. All training sessions were set for 100 epochs, but with early stopping. Left Y-axis shows the loss (for blue lines). The right Y-axis shows the accuracy for top-1 (red) and top-3 accuracy (green). Solid lines represent training and dashed lines represent validation.

#### 5 Species

![5 Species](/docs/top5species_Qlow.png)

#### 20 Species

![20 Species](/docs_experiments/top20species_Qlow.png)

#### 50 Species

![50 Species](/docs_experiments/top50species_Qlow.png)

#### 97 Species

![97 Species](/docs_experiments/top97species_Qlow.png)


### Remarks
It is clear that 5 species is the easiest to train, but training 50 species shows a higher accuracy than training with 20 species. Which is strange, because each time a species is added, it has less images.
