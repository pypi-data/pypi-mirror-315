import numpy as np

class HoLeeModel:
    def __init__(self, r0, theta, sigma, T, n, paths):
        """
        Initialize the Ho-Lee model parameters.
        :param r0: Initial short rate
        :param theta: Drift term (time-dependent mean adjustment)
        :param sigma: Volatility of the short rate
        :param T: Time horizon (in years)
        :param n: Number of time steps
        :param paths: Number of simulation paths
        """
        self.r0 = r0
        self.theta = theta
        self.sigma = sigma
        self.T = T
        self.n = n
        self.paths = paths

    def simulate(self):
        """
        Simulate short rate paths using the Ho-Lee model.
        :return: Simulated short rate paths
        """
        dt = self.T / self.n
        r = np.zeros((self.paths, self.n))
        r[:, 0] = self.r0

        for t in range(1, self.n):
            dr = self.theta * dt + self.sigma * np.sqrt(dt) * np.random.normal(size=self.paths)
            r[:, t] = r[:, t-1] + dr

        return r
