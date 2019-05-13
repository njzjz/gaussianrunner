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
        properties = ['energy', 'free_energy',
                      'force', 'atomic_number', 'coordinate']
        logfiles = GaussianRunner(
            keywords='opt force b3lyp/6-31g(d,p)').runGaussianInParallel(
                'SMILES', species, properties=properties)
        results = GaussianAnalyst(
            properties=properties).readFromLOGs(logfiles)
        print(results)

        assert results is not None
