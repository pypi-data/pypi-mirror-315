import numpy as np

class HestonModel:
    def __init__(self, v0, kappa, theta, sigma, rho, s0, T, n, paths):
        """
        Initialize the Heston model parameters.
        :param v0: Initial variance
        :param kappa: Rate of mean reversion
        :param theta: Long-term variance
        :param sigma: Volatility of volatility
        :param rho: Correlation between Brownian motions
        :param s0: Initial stock price
        :param T: Time horizon (in years)
        :param n: Number of time steps
        :param paths: Number of simulation paths
        """
        self.v0 = v0
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho
        self.s0 = s0
        self.T = T
        self.n = n
        self.paths = paths

    def simulate(self):
        """
        Simulate stock prices and variance paths using the Heston model.
        :return: Simulated stock prices and variance paths
        """
        dt = self.T / self.n
        S = np.zeros((self.paths, self.n))
        V = np.zeros((self.paths, self.n))
        S[:, 0], V[:, 0] = self.s0, self.v0

        for t in range(1, self.n):
            z1 = np.random.normal(size=self.paths)
            z2 = np.random.normal(size=self.paths)
            z2 = self.rho * z1 + np.sqrt(1 - self.rho**2) * z2  # Correlated noise

            # Variance process
            V[:, t] = np.abs(
                V[:, t-1]
                + self.kappa * (self.theta - V[:, t-1]) * dt
                + self.sigma * np.sqrt(V[:, t-1] * dt) * z2
            )

            # Stock price process
            S[:, t] = S[:, t-1] * np.exp(
                -0.5 * V[:, t] * dt + np.sqrt(V[:, t] * dt) * z1
            )

        return S, V
