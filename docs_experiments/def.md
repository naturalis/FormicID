# Final training for dorsal, head & profile
<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Final training for dorsal, head & profile](#final-training-for-dorsal-head-profile)
- [Settings](#settings)
- [Augmentation settings for training only:](#augmentation-settings-for-training-only)
- [Dorsal](#dorsal)
	- [Experiment name: `T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def`](#experiment-name-t97caallqumshdaugmd05lr0001e200i4def)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)
- [Head](#head)
	- [Experiment name: `T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def`](#experiment-name-t97caallqumshhaugmd05lr0001e200i4def)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)
	- [Experiment name: `T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def_clean`](#experiment-name-t97caallqumshhaugmd05lr0001e200i4defclean)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)
- [Profile](#profile)
	- [Experiment name: `T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def`](#experiment-name-t97caallqumshpaugmd05lr0001e200i4def)
		- [Training](#training)
		- [Training graph](#training-graph)
		- [Confusion matrix](#confusion-matrix)

<!-- /TOC -->
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
## Experiment name: `T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def`
### Training
- Epoch 00041: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00079: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.
- Epoch 00103: early stopping
### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def.png)
### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShD_AugM_D05_LR0001_E200_I4_def.png)
# Head
## Experiment name: `T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def`
### Training
- Epoch 00066: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00099: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.
- Epoch 00123: early stopping
### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def.png)
### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def.png)
## Experiment name: `T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def_clean`
The dataset has been cleaned of bad specimens.
### Training
- text
### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def_clean.png)
### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShH_AugM_D05_LR0001_E200_I4_def_clean.png)
# Profile
## Experiment name: `T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def`
__Epochs are defined as E100, but should be E200 (naming is wrong, settings are correct).__
### Training
- Epoch 00058: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00099: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.
- Epoch 00123: early stopping
### Training graph
![](/docs_experiments/T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def.png)
### Confusion matrix
![](/docs_experiments/CM-T97_CaAll_QuM_ShP_AugM_D05_LR0001_E200_I4_def.png)
