# GaussianRunner

[![python version](https://img.shields.io/pypi/pyversions/gaussianrunner.svg?logo=python&logoColor=white)](https://pypi.org/project/gaussianrunner)
[![PyPI](https://img.shields.io/pypi/v/gaussianrunner.svg)](https://pypi.org/project/gaussianrunner)
[![Build Status](https://travis-ci.com/njzjz/gaussianrunner.svg?branch=master)](https://travis-ci.com/njzjz/gaussianrunner)
[![Coverage Status](https://coveralls.io/repos/github/njzjz/gaussianrunner/badge.svg?branch=master)](https://coveralls.io/github/njzjz/gaussianrunner?branch=master)
[![codecov](https://codecov.io/gh/njzjz/gaussianrunner/branch/master/graph/badge.svg)](https://codecov.io/gh/njzjz/gaussianrunner)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cd4677ce1411486da534f62bd9306c2c)](https://www.codacy.com/app/jzzeng/gaussianrunner?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=njzjz/gaussianrunner&amp;utm_campaign=Badge_Grade)

A Python script to run Gaussian automatically and in batches.

**Author**: Jinzhe Zeng

**Email**: jzzeng@stu.ecnu.edu.cn

[![Research Group](https://img.shields.io/website-up-down-green-red/http/computchem.cn.svg?label=Research%20Group)](http://computechem.cn)

## Requirements
* [Gaussian](http://gaussian.com/)
* [OpenBabel](https://github.com/openbabel/openbabel)
* [MPI4PY](https://github.com/mpi4py/mpi4py) (if you need to run with MPI)

## Installation

Before you use GaussianRunner, please install [Gaussian](http://gaussian.com/) and [OpenBabel](https://github.com/openbabel/openbabel) first.

### With pip

```sh
$ pip install gaussianrunner
```

### Build from source

```sh
$ git clone https://github.com/njzjz/GaussianRunner.git
$ cd GaussianRunner/
$ pip install .
```

You can test whether the program is running normally:
```sh
% python setup.py pytest
```

## Examples
### Simple example

```python
>>> from gaussianrunner import GaussianRunner,GaussianAnalyst
>>> logfiles=GaussianRunner(keywords='opt freq b3lyp/6-31g(d,p)').runGaussianInParallel('SMILES',['C','C=C','CC','CO','OCCO','C=O','CN','O=O','O'])
>>> GaussianAnalyst(properties=['free_energy']).readFromLOGs(logfiles)
[{'name': 'C.log', 'free_energy': -40.49868}, {'name': 'C=C.log', 'free_energy': -78.563562}, {'name': 'CC.log', 'free_energy': -79.786915}, {'name': 'CO.log', 'free_energy': -115.69529}, {'name': 'OCCO.log', 'free_energy': -230.198798}, {'name': 'C=O.log', 'free_energy': -114.498144}, {'name': 'CN.log', 'free_energy': -95.822381}, {'name': 'O=O.log', 'free_energy': -150.272624}, {'name': 'O.log', 'free_energy': -76.416031}]
```

### Running across nodes with MPI

First, install [MPI4PY](https://github.com/mpi4py/mpi4py) and [MPICH 2](https://github.com/pmodels/mpich):

```bash
$ conda install mpi4py
```

Then run [mpiexample.py](examples/mpiexample.py) with MPI:
```bash
$ mpirun -n 9 --hostfile hostfile python mpiexample.py
```

There should be hostfile in the folder.
