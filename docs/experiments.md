# Experiments

## Head - Low quality - variable number of species

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

### Datasets
- [x] Downloaded 5 species
  - "num_iter_per_epoch": 8
  - epoch 63: Early stopping
- [x] Downloaded 20 species
  - "num_iter_per_epoch": 13 (should have been 18)
- [x] Downloaded 50 species
  - "num_iter_per_epoch": 34
- [x] Downloaded 97 species
  - "num_iter_per_epoch": 53

### Results - Head
|        Species |    5   |      20      |      50      |        97        |
|---------------:|:------:|:------------:|:------------:|:----------------:|
|         Images |    496 | 3638 (3523?) | 6526 (6525?) | 10,151 (10,150?) |
| Dorsal images  |    496 |         1175 |         2176 |             3384 |
| Head images    |    496 |         1169 |         2166 |             3366 |
| Profile images |    496 |         1179 |         2183 |             3400 |
|                |        |              |              |                  |
|     Validation |        |              |              |                  |
|           Loss |  0.776 |       1.5883 |              |                  |
|       Accuracy | 0.8515 |       0.6591 |              |                  |
| Top 3 Accuracy | 0.9901 |       0.8529 |              |                  |
|                |        |              |              |                  |
|           Test |        |              |              |                  |
|           Loss | 0.7963 |       1.5229 |              |                  |
|       Accuracy | 0.8750 |       0.6754 |              |                  |
| Top 3 Accuracy | 0.9792 |       0.8509 |              |                  |

_insert image_
