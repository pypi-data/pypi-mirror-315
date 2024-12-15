import math
from scipy.stats import norm
import numpy as np

class BlackScholes:
    @staticmethod
    def option_price(S, K, T, r, sigma, option_type="call"):
        """
        Calculate the Black-Scholes price for European options.
        :param S: Spot price
        :param K: Strike price
        :param T: Time to maturity (in years)
        :param r: Risk-free interest rate
        :param sigma: Volatility
        :param option_type: 'call' or 'put'
        :return: Option price
        """
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type == "call":
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif option_type == "put":
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        else:
            raise ValueError("Invalid option type. Use 'call' or 'put'.")

    @staticmethod
    def monte_carlo_simulation(S0, K, T, r, sigma, paths, n, option_type="call"):
        """
        Monte Carlo simulation for option pricing using Black-Scholes.
        :param S0: Initial stock price
        :param K: Strike price
        :param T: Time to maturity
        :param r: Risk-free interest rate
        :param sigma: Volatility
        :param paths: Number of simulation paths
        :param n: Number of time steps
        :param option_type: 'call' or 'put'
        :return: Simulated option prices
        """
        dt = T / n
        S = np.zeros((paths, n))
        S[:, 0] = S0
        for t in range(1, n):
            z = np.random.standard_normal(paths)
            S[:, t] = S[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
        
        payoff = np.maximum(0, S[:, -1] - K if option_type == "call" else K - S[:, -1])
        return np.exp(-r * T) * np.mean(payoff)
