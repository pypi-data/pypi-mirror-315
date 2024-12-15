import unittest
from stochastic_models.hull_white import HullWhiteModel

class TestHullWhiteModel(unittest.TestCase):
    def test_simulation(self):
        model = HullWhiteModel(r0=0.03, a=0.1, sigma=0.01, T=1, n=1000, paths=1000)
        r = model.simulate()
        self.assertEqual(r.shape, (1000, 1000))
        self.assertGreater(r.mean(), 0)  # Ensure rates are reasonable

if __name__ == '__main__':
    unittest.main()
