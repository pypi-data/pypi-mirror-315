import unittest
from stochastic_models.black_scholes import BlackScholes

class TestBlackScholes(unittest.TestCase):
    def test_option_price_call(self):
        price = BlackScholes.option_price(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call")
        self.assertGreater(price, 0)

    def test_option_price_put(self):
        price = BlackScholes.option_price(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="put")
        self.assertGreater(price, 0)

    def test_monte_carlo_simulation(self):
        price = BlackScholes.monte_carlo_simulation(S0=100, K=100, T=1, r=0.05, sigma=0.2, paths=1000, n=1000, option_type="call")
        self.assertGreater(price, 0)

if __name__ == '__main__':
    unittest.main()
