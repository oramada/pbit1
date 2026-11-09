# Getting started

PBit1 converts weight arrays into probability-based representations and samples
approximate weights back from them. Start with a small array, then use the same
steps for your own data.

## 1. Install

Use Python 3.12 or newer with Git installed:

```bash
python -m pip install "pbit1 @ git+https://github.com/oramada/pbit1.git@main"
```

Run the built-in example:

```bash
python -m pbit1
```

You will see the original result, sampled result, and difference. They can differ
because sampling is approximate. Run `pbit1 --help` to see the available options.

## 2. Encode some weights

```python
import pbit1

program = pbit1.encode([0.1, 0.5, 0.9])
```

An encoded program stores the probability controls and shared ranges needed to
reconstruct the weights. The original values can be positive or negative.

## 3. Reconstruct them

```python
result = program.reconstruct(4096, seed=7)
print(result.weights)
```

The first argument is the number of samples per weight. More samples usually
reduce sampling noise, with more work. Finite control precision also limits
accuracy. The seed makes the draw repeatable in the same software environment.

`result.weights` is an FP32 NumPy array with the original shape.

## 4. Use the result

Reconstructed weights work with ordinary NumPy calculations:

```python
import numpy as np
import pbit1

weights = np.array([[0.1, -0.2], [0.3, 0.8]], dtype=np.float32)
inputs = np.array([[1.0, 0.5]], dtype=np.float32)

program = pbit1.encode(weights)
result = program.reconstruct(4096, seed=7)

print("Original:", inputs @ weights)
print("Sampled: ", inputs @ result.weights)
```

These array examples do not automatically convert or run a pretrained model.
Measure task quality when integrating the reconstructed weights into your model.

## Use THRML

Install the optional backend:

```bash
python -m pip install "pbit1[thrml] @ git+https://github.com/oramada/pbit1.git@main"
pbit1 --backend thrml
```

This demo uses Extropic’s official CPU simulator. Its setup needs a platform
supported by the pinned JAX packages. No physical hardware access is required.

For Python usage, see the [THRML example](../examples/native_probability.py).

## Useful commands

```bash
pbit1 --samples 4096 --runs 4 --seed 7
pbit1 --json
pbit1 --version
```

`--runs` averages independent draws in the demo; `--chains` is its supported alias.
`--json` includes the full result, controls, and diagnostics for scripts.

## Next steps

- [API reference](API.md): methods, arguments, and return values.
- [Technical details](FINITE_PROGRAM.md): grouping, precision, and storage costs.
- [Research results](SPARK_VERIFICATION.md): measured model quality and its limits.
