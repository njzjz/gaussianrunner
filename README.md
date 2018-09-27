# GaussianRunner
[![python3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://badge.fury.io/py/GaussianRunner)[![pypi](https://badge.fury.io/py/GaussianRunner.svg)](https://badge.fury.io/py/MDDatasetMaker)

A Python script to run Gaussian automatically and in batches.

**Author**: Jinzhe Zeng

**Email**: jzzeng@stu.ecnu.edu.cn

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
>>> from GaussianRunner import GaussianRunner,GaussianAnalyst
>>> logfiles=GaussianRunner(keywords='opt freq b3lyp/6-31g(d,p)').runGaussianInParallel('SMILES',['C','C=C','CC','CO','OCCO','C=O','CN','O=O','O'])
>>> GaussianAnalyst(properties=['free_energy']).readFromLOGs(logfiles)
[{'name': 'C.log', 'free_energy': -40.49868}, {'name': 'C=C.log', 'free_energy': -78.563562}, {'name': 'CC.log', 'free_energy': -79.786915}, {'name': 'CO.log', 'free_energy': -115.69529}, {'name': 'OCCO.log', 'free_energy': -230.198798}, {'name': 'C=O.log', 'free_energy': -114.498144}, {'name': 'CN.log', 'free_energy': -95.822381}, {'name': 'O=O.log', 'free_energy': -150.272624}, {'name': 'O.log', 'free_energy': -76.416031}]
```
