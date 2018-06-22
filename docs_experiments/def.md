# Final experiments for dorsal, head & profile

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Final experiments for dorsal, head & profile](#final-experiments-for-dorsal-head-profile)
- [Dataset example](#dataset-example)
- [Augmentation](#augmentation)
- [Settings](#settings)
- [Augmentation settings for training only:](#augmentation-settings-for-training-only)
- [Dorsal](#dorsal)
	- [Experiment dorsal](#experiment-dorsal)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)
	- [Experiment dorsal clean](#experiment-dorsal-clean)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)
- [Head](#head)
	- [Experiment head](#experiment-head)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)
	- [Experiment head clean](#experiment-head-clean)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)
- [Profile](#profile)
	- [Experiment profile](#experiment-profile)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)
- [Profile](#profile)
	- [Experiment profile clean](#experiment-profile-clean)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)
- [Statia 2015](#statia-2015)
- [Caste distribution](#caste-distribution)

<!-- /TOC -->

# Dataset example
A few example images from the dataset (all shottypes and species at random).
![](/docs_experiments/dataset_example.png)


# Augmentation
Augmentation of _Eciton burchellii_ (CASENT0009221), head view.
![](/docs_experiments/Augmentation_eciton_burchellii_casent0009221_h.png)

# Settings
Training settings as below:
```python
number_of_species="97"
image_quality="med"
castes="all"
num_epochs=100
batch_size=32
dropout=0.5
optimizer="Nadam" # With following settings:
	lr=0.001,
	beta_1=0.9,
	beta_2=0.999,
	epsilon=1e-08,
	schedule_decay=0.004
model=InceptionResNetV2 # With modified top layers dropout and a dense layer with num_species.
seed=1
testsplit=0.1
validationsplit=0.2
weights initialization="imagenet"
The prelast Dense Layer activation="relu"
# Augmentation settings for training only:
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
```

# Dorsal

## Experiment dorsal
`T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def`

### Training
- Epoch 00041: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00079: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.
- Epoch 00103: early stopping

### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def.png)

### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def.png)

## Experiment dorsal clean
`T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def`

### Training
- Epoch 00047: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.

### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def_clean.png)

### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def_clean.png)


# Head

## Experiment head
`T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def`

### Training
- Epoch 00066: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00099: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.
- Epoch 00123: early stopping

### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def.png)

### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def.png)


## Experiment head clean
`T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def_clean`
The dataset has been cleaned of bad specimens.

### Training
- Epoch 00066: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00099: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.
- Epoch 00123: early stopping

### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def_clean.png)

### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def_clean.png)


# Profile

## Experiment profile
`T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def`
__Epochs are defined as E100, but should be E200 (naming is wrong, settings are correct).__

### Training
- Epoch 00058: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00099: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.
- Epoch 00123: early stopping

### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def.png)

### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def.png)


# Profile

## Experiment profile clean
`T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def_clean`

### Training
- Epoch 00054: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00102: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.
- Epoch 00126: early stopping

### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def_clean.png)

### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def_clean.png)

# Statia 2015

![](/docs_experiments/Statiafolders.png)

![](/docs_experiments/mfloricola.png)

# Caste distribution

![](/docs_experiments/caste_distribution.png)

## No test images anymore
### Dorsal
- Species 3: azteca_alfari has no test images anymore.
- Species 49: mystrium_mirror has no test images anymore.
- Species 54: nylanderia_madagascarensis has no test images anymore.
- Species 75: polyrhachis_dives has no test images anymore.
- Species 86: technomyrmex_vitiensis has no test images anymore.

### Head
- Species 76: pseudomyrmex_gracilis has no test images anymore.

### Profile
- Species 47: monomorium_termitobium has no test images anymore.
- Species 75: polyrhachis_dives has no test images anymore.
- Species 82: strumigenys_rogeri has no test images anymore.
