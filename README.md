# GaussianRunner
[![python3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://badge.fury.io/py/GaussianRunner)[![pypi](https://badge.fury.io/py/GaussianRunner.svg)](https://badge.fury.io/py/MDDatasetMaker)

A Python script to run Gaussian automatically and in batches.

Author: Jinzhe Zeng

Email: njzjz@qq.com  10154601140@stu.ecnu.edu.cn

[Research Group](http://computchem.cn)

## Requirements
* [Gaussian](http://gaussian.com/)
* [OpenBabel](https://github.com/openbabel/openbabel)

## Installation

Before you use GaussianRunner, please install [Gaussian](http://gaussian.com/) and [OpenBabel](https://github.com/openbabel/openbabel) first.

### With pip
```sh
$ pip install GaussianRunner
```
### Build from source
```sh
$ git clone https://github.com/njzjz/GaussianRunner.git
$ cd GaussianRunner/
$ python3 setup.py install
```

## Examples
### Simple example

```python
>>> from GaussianRunner import GaussianRunner
>>> GaussianRunner(keywords='opt freq b3lyp/6-31g(d,p)').runGaussianInParallel('SMILES',['C','C=C','CC','CO','OCCO','C=O','CN','O=O','O'])

```
