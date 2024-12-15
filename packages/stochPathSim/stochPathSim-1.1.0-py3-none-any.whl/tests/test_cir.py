import unittest
from stochastic_models.cir import CoxIngersollRossModel

class TestCIRModel(unittest.TestCase):
    def test_simulation(self):
        model = CoxIngersollRossModel(r0=0.03, kappa=0.2, theta=0.05, sigma=0.02, T=1, n=1000, paths=1000)
        r = model.simulate()
        self.assertEqual(r.shape, (1000, 1000))
        self.assertTrue((r >= 0).all())  # Rates should be non-negative

if __name__ == '__main__':
    unittest.main()
