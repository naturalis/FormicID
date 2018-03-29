# Experiments
This markdown document will show results from experiments.


<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Experiments](#experiments)
- [Low quality images](#low-quality-images)
	- [Low quality image datasets - parameters and events](#low-quality-image-datasets-parameters-and-events)
		- [Low quality image datasets - Number of images](#low-quality-image-datasets-number-of-images)
	- [Head view - Low quality](#head-view-low-quality)
		- [Settings](#settings)
		- [Results](#results)

<!-- /TOC -->
# Low quality images
## Low quality image datasets - parameters and events
- [x] Downloaded 5 species
  - "num_iter_per_epoch": 8
  - Epoch 00039: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
  - Epoch 00063: early stopping
- [x] Downloaded 20 species
  - "num_iter_per_epoch": 13 (should have been 18)
- [x] Downloaded 50 species
  - "num_iter_per_epoch": 34
  - Epoch 00053: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
  - Epoch 00085: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.
- [x] Downloaded 97 species
  - "num_iter_per_epoch": 53

### Low quality image datasets - Number of images

|        Species |    5   |      20      |      50      |        97        |
|---------------:|:------:|:------------:|:------------:|:----------------:|
|         Images |    496 | 3638 (3523?) | 6526 (6525?) | 10,151 (10,150?) |
| Dorsal images  |    496 |         1175 |         2176 |             3384 |
| Head images    |    496 |         1169 |         2166 |             3366 |
| Profile images |    496 |         1179 |         2183 |             3400 |

## Head view - Low quality
### Settings
Settings:
```
"Augmentation": 'small',
"exp_name": "top20species_Qlow",
"num_epochs": 10,
"learning_rate": 0.001,
"batch_size": 64,
"dropout": 0.5,
"optimizer": "Nadam",
"model": "InceptionV3",
"seed": 1,
"testsplit": 0.1,
"validationsplit": 0.2

```
### Results

|        Species |    5   |   20   |   50   |  97  |
|---------------:|:------:|:------:|:------:|:----:|
| Head images    |    496 |   1169 |   2166 | 3366 |
|  Training      | 347    |   820  |   1516 |      |
|                |        |        |        |      |
|     Validation |  101   | 235    |   435  |      |
|           Loss |  0.776 | 1.5883 | 1.5451 |      |
|       Accuracy | 0.8515 | 0.6591 | 0.7039 |      |
| Top 3 Accuracy | 0.9901 | 0.8529 | 0.8982 |      |
|                |        |        |        |      |
|           Test |  48    |  114   |  215   |      |
|           Loss | 0.7963 | 1.5229 | 1.7074 |      |
|       Accuracy | 0.8750 | 0.6754 | 0.7023 |      |
| Top 3 Accuracy | 0.9792 | 0.8509 | 0.8791 |      |

#### 5 Species
![5 Species](/docs/lowquality/top5species_Qlow.png)

#### 20 Species
![5 Species](/docs/lowquality/top20species_Qlow.png)

#### 50 Species
![5 Species](/docs/lowquality/top50species_Qlow.png)

#### 5 Species
image
