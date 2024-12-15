import numpy as np

class GeometricBrownianMotion:
    def __init__(self, mu, sigma, s0, T, n, paths):
        """
        Initialize the Geometric Brownian Motion parameters.
        :param mu: Expected return (drift)
        :param sigma: Volatility
        :param s0: Initial stock price
        :param T: Time horizon (in years)
        :param n: Number of time steps
        :param paths: Number of simulation paths
        """
        self.mu = mu
        self.sigma = sigma
        self.s0 = s0
        self.T = T
        self.n = n
        self.paths = paths

    def simulate(self):
        """
        Simulate Geometric Brownian Motion using Monte Carlo.
        :return: Time array and simulated paths
        """
        dt = self.T / self.n
        t = np.linspace(0, self.T, self.n)
        W = np.random.standard_normal((self.paths, self.n))  # Brownian increments
        W = np.cumsum(W, axis=1) * np.sqrt(dt)  # Brownian motion
        S = self.s0 * np.exp((self.mu - 0.5 * self.sigma**2) * t + self.sigma * W)
        return t, S
