# GaussianRunner

[![python version](https://img.shields.io/pypi/pyversions/gaussianrunner.svg?logo=python&logoColor=white)](https://pypi.org/project/gaussianrunner)
[![PyPI](https://img.shields.io/pypi/v/gaussianrunner.svg)](https://pypi.org/project/gaussianrunner)
[![codecov](https://codecov.io/gh/njzjz/gaussianrunner/branch/master/graph/badge.svg)](https://codecov.io/gh/njzjz/gaussianrunner)

A Python script to run Gaussian automatically and in batches.

## Installation

Before you use GaussianRunner, please install [Gaussian](http://gaussian.com/) first.

```sh
pip install gaussianrunner
```

You can test whether the program is running normally:
```sh
python setup.py pytest
```

## Examples
### Simple example

```py
from gaussianrunner import GaussianRunner, GaussianAnalyst

logfiles = GaussianRunner(keywords="opt freq b3lyp/6-31g(d,p)").runGaussianInParallel(
    "SMILES", ["C", "C=C", "CC", "CO", "OCCO", "C=O", "CN", "O=O", "O"]
)
GaussianAnalyst(properties=["free_energy"]).readFromLOGs(logfiles)
```

```py
[
    {"name": "C.log", "free_energy": -40.49868},
    {"name": "C=C.log", "free_energy": -78.563562},
    {"name": "CC.log", "free_energy": -79.786915},
    {"name": "CO.log", "free_energy": -115.69529},
    {"name": "OCCO.log", "free_energy": -230.198798},
    {"name": "C=O.log", "free_energy": -114.498144},
    {"name": "CN.log", "free_energy": -95.822381},
    {"name": "O=O.log", "free_energy": -150.272624},
    {"name": "O.log", "free_energy": -76.416031},
]
```

### Running across nodes with MPI

First, install [MPI4PY](https://github.com/mpi4py/mpi4py) and [MPICH 2](https://github.com/pmodels/mpich):

```bash
conda install mpi4py
```

Then run [mpiexample.py](examples/mpiexample.py) with MPI:
```bash
mpirun -n 9 --hostfile hostfile python mpiexample.py
```

There should be hostfile in the folder.
