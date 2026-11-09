"""Sample one official THRML logical p-bit per probability weight.

Install the optional [thrml] extra before running this example.
"""
import numpy as np
from pbit1 import NativeProbabilityBank

weights = np.array([0.1, 0.5, 0.9])
bank = NativeProbabilityBank(weights)
states = bank.sample(seed=7, n_samples=1024, n_chains=4)

print("Requested probabilities:", weights)
print("Observed probabilities: ", states.mean(axis=(0, 1)))
print("Control costs:          ", bank.controls())
