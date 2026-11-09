# Finite probability programs

`FinitePBitProgram` implements the finite-control NumPy reconstruction used in
the DGX Spark research. It is available in the current development package;
the older `v0.1.0a1` tag predates this API.

```python
import numpy as np
from pbit1 import FinitePBitProgram

weights = np.linspace(-0.5, 0.7, 256).reshape(16, 16)
program = FinitePBitProgram.encode(
    weights, group_size=128, layout="transposed_matrix"
)
result = program.reconstruct(32768, seed=7, parameter_index=0)

print(result.weights)          # FP32, original matrix shape and orientation
print(program.expectation())  # finite-controller mean, without sampling
print(program.storage())      # command and range payload sizes
```

## Control mapping and ranges

Each group stores an FP32 minimum and span. Each scalar uses a 12-bit command
with 4,096 levels over the half-logit interval `[-4, 4]`. The decoded probability
is `sigmoid(2 * field)`. A constant group has zero span and reconstructs its
constant value regardless of the sampled states.

`storage_flat` groups consecutive values in the original flattened tensor.
`transposed_matrix` transposes a 2D matrix before flattening and restores the
original orientation afterward. Groups can cross row boundaries. For depthwise
filters with seven coefficients, `group_size=7` can keep each filter together.
Choose groups to match the intended operator; the SDK does not select them
from model activations automatically.

Finite field limits clip endpoint probabilities away from exact zero and one
in nonconstant groups. Additional samples reduce sampling variance around the
finite-controller mean, not the difference between that mean and the original
weights.

## Sampling and replay

The simulator draws exact independent binomial counts instead of emitting every
Bernoulli state. Counts use uint16 through 65,535 samples and uint32 above that.
The seed and parameter index identify the tensor's random stream. `counts_sha256`
allows replay checks when the input, program, random-number implementation, and
sampling order match.

The output is FP32. The research neural runners separately round to BF16. This
API does not install weights into a model, simulate correlated devices, or
perform native THRML execution.

## Storage accounting

| `storage()` field | Includes |
|---|---|
| `parameters` / `logical_pbits` | One logical stochastic element per scalar |
| `controller_storage_bytes` | Implemented uint16 command arrays: two bytes per scalar |
| `range_metadata_bytes` | Two FP32 values per group: eight bytes per group |
| `actual_program_array_bytes` | Command and range arrays together |
| `ideal_packed_program_bits` | Hypothetical packed 12-bit commands plus range bits |
| `physical_binary_state_bits_additional` | Conceptual one-bit state per logical element, counted separately |

The ideal packed format is an accounting alternative, not the implemented
array layout. Sampling counters, reconstructed weights, Python objects, and
physical controller circuitry are additional. One logical p-bit does not imply
one bit of total storage.

The [API reference](API.md#finitepbitprogram) documents validation and return fields.
The [research verification](SPARK_VERIFICATION.md) describes exact count/BF16 replay
against the frozen experiment sampler.
