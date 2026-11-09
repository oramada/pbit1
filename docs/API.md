# API reference

The default installation needs NumPy. Importing `pbit1`, encoding finite programs,
and running the default CLI do not require JAX or THRML.

## FinitePBitProgram

```python
from pbit1 import FinitePBitProgram

program = FinitePBitProgram.encode(weights, group_size=128, layout="storage_flat")
result = program.reconstruct(32768, seed=7, parameter_index=0)
```

| Method | Returns |
|---|---|
| `encode(weights, *, group_size=128, layout="storage_flat")` | A finite-control program in the input tensor shape |
| `reconstruct(n_samples, *, seed, parameter_index=0)` | A `Reconstruction` containing FP32 weights and count metadata |
| `expectation()` | FP32 expected weights under the finite controller, without sampling |
| `storage()` | A dictionary of array payload sizes and separately counted logical states |

Inputs must be nonempty and finite after FP32 conversion. Group size is an integer
from 1 through 65,536. Layout is `storage_flat` or `transposed_matrix`; the latter
requires a two-dimensional matrix. Reconstruction supports integer sample counts
from 1 through `2**32 - 1` and nonnegative integer parameter indices.

`Reconstruction` has these fields:

| Field | Meaning |
|---|---|
| `weights` | FP32 array with the original tensor shape and orientation |
| `counts_sha256` | Digest of the sampled counts for reproducibility checks |
| `counter_dtype` | `uint16` through 65,535 samples; `uint32` above that |
| `maximum_count` | Largest sampled count in this reconstruction |
| `samples` | Samples per scalar |

`parameter_index` separates tensor streams within one experiment seed. Use a
stable index for each tensor when reproducing a multi-tensor reconstruction.
The hash depends on the recorded NumPy random-number implementation and the
program's sampling order; record your package versions for exact replay.

See [the finite-program guide](FINITE_PROGRAM.md) for the control mapping,
constant groups, layouts, and storage fields. The API returns FP32; it does not
silently round to BF16 or replace weights inside another framework.

## SinglePBit

`SinglePBit` is the ideal NumPy reference encoder, with explicit sampled affine
weight tensors. Unlike `FinitePBitProgram`, it does not quantize probability
commands to the finite 12-bit grid.

```python
import numpy as np
from pbit1 import SinglePBit

weights = np.array([[-0.7, 0.2], [0.3, 0.8], [-0.1, 0.4]])
inputs = np.array([[1.0, -0.5, 0.25]])
codec = SinglePBit(eps=0)
encoded = codec.encode(weights)
output = codec.forward(inputs, encoded, 8192, np.random.default_rng(7))
```

| Method | Shape or behavior |
|---|---|
| `encode(weights, group_ids=None)` | Returns `SinglePBitWeights`; omitted IDs put all weights in one range |
| `sample(encoded, n_samples, rng)` | Affine sampled weights with shape `(n_samples, *weights.shape)` |
| `decode(samples)` | Averages the leading sample axis |
| `forward(inputs, encoded, n_samples, rng)` | Averages linear outputs; weights have shape `(input_features, output_features)` |

The default `eps=1e-6` clips probabilities. Explicit `eps=0` permits ideal
endpoints. Constant groups have zero radius. Custom `group_ids` must match the
weight tensor shape. This reference path materializes sampled tensors;
`FinitePBitProgram` uses count sampling for larger reconstruction budgets.

## NativeProbabilityBank

Requires the optional `thrml` extra. Each finite input value in `[0,1]` specifies
the probability of one logical THRML spin. These probabilities are independent
weight controls, not a softmax distribution across weights.

```python
import numpy as np
from pbit1 import NativeProbabilityBank

bank = NativeProbabilityBank(np.array([0.1, 0.5, 0.9]))
states = bank.sample(seed=7, n_samples=1024, n_chains=4)
print(states.mean(axis=(0, 1)))
print(bank.controls())
```

| Interface | Returns |
|---|---|
| `NativeProbabilityBank(weights, beta=1.0)` | A bank of logical THRML nodes; beta must be positive and finite |
| `sample(seed, n_samples, n_chains=1, initial_one=False)` | Binary states with shape `(chains, samples, *weights.shape)` |
| `realized_probabilities` | Probabilities after float32 bias-field rounding |
| `logical_pbits` | Node count, including clamped endpoints |
| `controls()` | Logical/free/clamped counts, float32 bias storage, and backend details |

An isolated spin uses `bias = logit(p) / (2 * beta)`. Exact zero and one are
represented by clamped nodes. The adapter defaults to CPU and uses the official
THRML sampler. It has floating-point bias fields; it is distinct from the finite
12-bit NumPy program and is not a physical hardware driver.

## Command-line interface

```bash
python -m pbit1                                    # NumPy demo
python -m pbit1 --samples 4096 --chains 4 --seed 7
python -m pbit1 --backend thrml --samples 1024      # optional backend
python -m pbit1 --version
python -m pbit1 --help
```

The `pbit1` console script accepts the same options. Both backends emit JSON with
the version, selected backend, seed, sampling budget, control costs, and reference
and sampled dot products. NumPy adds reconstructed weights and finite-controller
means; THRML adds observed probabilities and bias-rounded target probabilities.
The default backend changed to NumPy in `0.1.0a2.dev2`; use `--backend thrml` to
select the earlier native demonstration explicitly.
