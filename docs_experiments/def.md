## Settings

Training settings as below:

```python
number_of_species="97"
image_quality="med"
castes="all"
num_epochs=100
learning_rate=0.001
batch_size=32
dropout=0.5
optimizer="Nadam" # With following settings:
	lr =learning_rate,
	beta_1 =0.9,
	beta_2 =0.999,
	epsilon =1e-08,
	schedule_decay =0.004
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

## Dorsal
`T97_CaAll_QuM_ShD_AugM_D05_LR0001_E100_I4_def`

### Training
-

![](/docs_experiments/T97_CaAll_QuM_ShD_AugM_D05_LR0001_E100_I4_def.png)

### Confusion matrix

![](/docs_experiments/CM-T97_CaAll_QuM_ShD_AugM_D05_LR0001_E100_I4_def.png)

## Head
`T97_CaAll_QuM_ShH_AugM_D05_LR0001_E100_I4_def`

### Training
- Epoch 00044: ReduceLROnPlateau reducing learning rate to `0.00010000000474974513`.
- Epoch 00088: ReduceLROnPlateau reducing learning rate to `1.0000000474974514e-05`.

![](/docs_experiments/T97_CaAll_QuM_ShH_AugM_D05_LR0001_E100_I4_def.png)

### Confusion matrix

![](/docs_experiments/CM-T97_CaAll_QuM_ShH_AugM_D05_LR0001_E100_I4_def.png)

## Profile
`T97_CaAll_QuM_ShP_AugM_D05_LR0001_E100_I4_def`

### Training
-

![](/docs_experiments/T97_CaAll_QuM_ShP_AugM_D05_LR0001_E100_I4_def.png)

### Confusion matrix

![](/docs_experiments/CM-T97_CaAll_QuM_ShP_AugM_D05_LR0001_E100_I4_def.png)
