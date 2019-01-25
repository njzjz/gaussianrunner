from gaussianrunner.mpi import GaussianRunner_MPI
GaussianRunner_MPI(cpu_num=28, nproc=28, keywords='opt freq b3lyp/6-31g(d,p)').run_MPI(
    'SMILES', ['C', 'C=C', 'CC', 'CO', 'OCCO', 'C=O', 'CN', 'O=O', 'O'])
