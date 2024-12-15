import numpy as np

class HullWhiteModel:
    def __init__(self, r0, a, sigma, T, n, paths):
        """
        Initialize the Hull-White model parameters.
        :param r0: Initial interest rate
        :param a: Mean reversion speed
        :param sigma: Volatility of interest rate
        :param T: Time horizon (in years)
        :param n: Number of time steps
        :param paths: Number of simulation paths
        """
        self.r0 = r0
        self.a = a
        self.sigma = sigma
        self.T = T
        self.n = n
        self.paths = paths

    def simulate(self):
        """
        Simulate interest rate paths using the Hull-White model.
        :return: Simulated interest rate paths
        """
        dt = self.T / self.n
        r = np.zeros((self.paths, self.n))
        r[:, 0] = self.r0

        for t in range(1, self.n):
            dr = (
                -self.a * r[:, t-1] * dt
                + self.sigma * np.sqrt(dt) * np.random.normal(size=self.paths)
            )
            r[:, t] = r[:, t-1] + dr

        return r
