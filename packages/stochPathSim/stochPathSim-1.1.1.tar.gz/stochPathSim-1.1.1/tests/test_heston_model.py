import unittest
from stochastic_models.heston_model import HestonModel

class TestHestonModel(unittest.TestCase):
    def test_simulation(self):
        model = HestonModel(v0=0.04, kappa=2.0, theta=0.04, sigma=0.3, rho=-0.7, s0=100, T=1, n=1000, paths=1000)
        S, V = model.simulate()
        self.assertEqual(S.shape, (1000, 1000))
        self.assertEqual(V.shape, (1000, 1000))
        self.assertTrue((V >= 0).all())  # Variance should be non-negative

if __name__ == '__main__':
    unittest.main()
