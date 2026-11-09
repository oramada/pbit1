"""Encode a weight array and recover an approximate version."""
import pbit1

program = pbit1.encode([0.1, 0.5, 0.9])
result = program.reconstruct(4096, seed=7)

print("Original weights: [0.1, 0.5, 0.9]")
print("Sampled weights: ", result.weights.round(4))
