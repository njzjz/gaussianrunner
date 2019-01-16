import unittest
import os
from . import GaussianRunner, GaussianAnalyst


class Test_all(unittest.TestCase):
    def test_gaussianrunner(self):
        folder = "test"
        if not os.path.exists(folder):
            os.makedirs(folder)
        species = ['C', 'C=C', 'CC', 'CO', 'OCCO', 'C=O', 'CN', 'O=O', 'O']
        paths = [os.path.join(folder, f'{spec}.log') for spec in species]
        logfiles = GaussianRunner(
            keywords='opt freq b3lyp/6-31g(d,p)').runGaussianInParallel('SMILES', species, outputlist=paths)
        results = GaussianAnalyst(
            properties=['free_energy']).readFromLOGs(logfiles)
        print(results)

        self.assertTrue(results is not None)


if __name__ == '__main__':
    unittest.main()
