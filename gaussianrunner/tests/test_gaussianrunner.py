import tempfile
import logging
import os
from gaussianrunner import GaussianRunner, GaussianAnalyst


class Test_all:
    def test_gaussianrunner(self):
        folder = tempfile.mkdtemp(prefix='testfiles-', dir='.')
        logging.info(f'Folder: {folder}:')
        os.chdir(folder)
        if not os.path.exists(folder):
            os.makedirs(folder)
        species = ['C']
        logfiles = GaussianRunner(
            keywords='opt b3lyp/6-31g(d,p)').runGaussianInParallel('SMILES', species)
        results = GaussianAnalyst(
            properties=['energy']).readFromLOGs(logfiles)
        print(results)

        assert results is not None
