import unittest
from stochastic_models.gbm import GeometricBrownianMotion

class TestGeometricBrownianMotion(unittest.TestCase):
    def test_simulation(self):
        model = GeometricBrownianMotion(mu=0.1, sigma=0.2, s0=100, T=1, n=1000, paths=1000)
        t, S = model.simulate()
        self.assertEqual(S.shape, (1000, 1000))
        self.assertEqual(len(t), 1000)
        self.assertGreater(S.mean(), 0)  # Ensure simulated values are positive

if __name__ == '__main__':
    unittest.main()
