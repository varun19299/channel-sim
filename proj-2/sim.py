import numpy as np
from sacred import Experiment
from tqdm import tqdm
import matplotlib.pyplot as plt
from functools import partial

ex = Experiment("MLE-dist-simulation")

@ex.config
def config():
    A = 1
    N = 10000      # No of data points
    n = 100     # No of experiments to repeat over

@ex.capture
def plot_stats(distribution, estimator, A, N, n):
    pbar = tqdm(range(n))
    estimator_ll = []
    for i in pbar:
        data = distribution(size = N)
        estimator_ll.append(estimator(data))
        pbar.set_description(f"")

    estimator_ll = np.array(estimator_ll)
    estimator_mean = np.mean(estimator_ll)
    estimator_var = np.var(estimator_ll)

    plt.hist(estimator_ll, bins = 50)
    plt.show()

    return estimator_mean, estimator_var


@ex.automain
def main(_run):
    distribution = np.random.normal
    distribution = partial(distribution, loc = 1, scale = 1)
    plot_stats(distribution, np.mean)