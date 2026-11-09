"""Encode, reconstruct, and inspect finite-control weights using NumPy only."""
import numpy as np
from pbit1 import FinitePBitProgram

weights = np.array([[-0.7, 0.2], [0.3, 0.8], [-0.1, 0.4]], dtype=np.float32)
inputs = np.array([[1.0, -0.5, 0.25]], dtype=np.float32)
program = FinitePBitProgram.encode(weights, group_size=3)
sample = program.reconstruct(32768, seed=7)

print("Reference output:    ", inputs @ weights)
print("Reconstructed output:", inputs @ sample.weights)
print("Program storage:     ", program.storage())
print("Count digest:        ", sample.counts_sha256)
