# SQFA

[![Build Status](https://github.com/dherrera1911/sqfa/actions/workflows/install.yml/badge.svg)](https://github.com/dherrera1911/sqfa/actions/workflows/install.yml)
[![Tests Status](https://github.com/dherrera1911/sqfa/actions/workflows/tests.yml/badge.svg)](https://github.com/dherrera1911/sqfa/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/sqfa/badge/?version=latest)](https://sqfa.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/dherrera1911/sqfa?tab=MIT-1-ov-file)
![Python version](https://img.shields.io/badge/python-3.9|3.10|3.11|3.12-blue.svg)
[![codecov](https://codecov.io/gh/dherrera1911/sqfa/graph/badge.svg?token=NN44R5G18I)](https://codecov.io/gh/dherrera1911/sqfa)


Supervised Quadratic Feature Analysis (SQFA) is a supervised dimensionality
reduction technique. It learns a set of linear features that
maximize the differences in second-order statistics between
classes. The `sqfa` package provides an implementation of the SQFA algorithm in PyTorch.

SQFA uses a geometric loss on the class-specific second moment matrices,
considered as points in the SPD manifold. Intuitively, the distance between
the SPD matrices of different classes is a measure of their second-order
dissimilarity. SQFA finds the features that maximize this distance.

For detailed information on the method, see the
[sqfa package tutorials](https://sqfa.readthedocs.io/en/latest/tutorials/spd_geometry.html).

## Overview

The `sqfa` package provides a class `SQFA` that can be used to train the
model. The class has an API similar to that of `sklearn` models.
An example of how to use the `SQFA` class is shown below:

```python
import sqfa
import torchvision

### Download dataset

trainset = torchvision.datasets.MNIST(
    root="./data", train=True, download=True
)
x = trainset.data.reshape(-1, 28 * 28).float()
y = trainset.targets
# Normalize x
x = x / (x.std() * 28.0)
x = x - x.mean(dim=0, keepdim=True)

### Initialize SQFA model

model = sqfa.model.SQFA(
    n_dim=x.shape[-1],
    n_filters=4,
    feature_noise=0.01,
)

### Fit model. Two options:

# 1) Give data and labels as input
model.fit(X=x, y=y)

# 2) Give scatter matrices as input
data_stats = sqfa.statistics.class_statistics(x, y)
model.fit(data_scatters=data_stats["second_moments"])

### Transform data to the learned feature space

x_transformed = model.transform(x).detach()
```

See the tutorials for more details on the model usage and behavior.

## Installation

### Virtual environment

We recommend installing the package in a virtual environment. For this,
you can first install `miniconda` 
([install instructions link](https://docs.anaconda.com/miniconda/install/#quick-command-line-install)),
and then create a virtual environment with Python 3.11 with the following
shell command:

```bash
conda create -n my-sqfa python=3.11
```

You can then activate the virtual environment with the following command:

```bash
conda activate my-sqfa
```

You should activate the `my-sqfa` environment to install the package, and every
time you want to use it.

### Install package

You can install `sqfa` with `pip` by running the following commands in
the shell:

```bash
git clone git@github.com:dherrera1911/sqfa.git
cd sqfa
pip install -e .
```

The first command clones the repository, the second command moves to the
repository directory, and the third command installs the package in
editable mode. If you want to install the dependencies needed to run
the tutorials, you should substitute the last command with the following:

```bash
pip install -e .[dev]
```
