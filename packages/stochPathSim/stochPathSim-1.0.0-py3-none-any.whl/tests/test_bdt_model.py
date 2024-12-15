import unittest
from stochastic_models.bdt_model import BlackDermanToyModel

class TestBDTModel(unittest.TestCase):
    def test_simulation(self):
        model = BlackDermanToyModel(r0=0.03, sigma=0.01, T=1, n=1000, paths=1000)
        r = model.simulate()
        self.assertEqual(r.shape, (1000, 1000))

if __name__ == '__main__':
    unittest.main()
