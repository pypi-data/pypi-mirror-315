import unittest
from stochastic_models.vasicek import VasicekModel

class TestVasicekModel(unittest.TestCase):
    def test_simulation(self):
        model = VasicekModel(r0=0.03, kappa=0.15, theta=0.05, sigma=0.01, T=1, n=1000, paths=1000)
        r = model.simulate()
        self.assertEqual(r.shape, (1000, 1000))
        self.assertTrue((r >= 0).all())  # Ensure rates are valid

if __name__ == '__main__':
    unittest.main()
