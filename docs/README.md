# PBit1 documentation

Start with the [README quickstart](../README.md#quickstart). A NumPy-only installation
can run `python -m pbit1` immediately; the official THRML backend is optional.

## Learn the package

| Guide | Covers |
|---|---|
| [API reference](API.md) | Public interfaces, tensor shapes, outputs, and examples |
| [Finite probability programs](FINITE_PROGRAM.md) | Group layouts, finite controls, reproducibility, and memory |
| [NumPy example](../examples/quickstart.py) | Encode, reconstruct, inspect storage, compute an output |
| [THRML example](../examples/native_probability.py) | Sample probability weights using the official backend |
| [Contributing](../CONTRIBUTING.md) | Local setup, checks, and useful bug reports |
| [Changelog](../CHANGELOG.md) | Package changes and compatibility notes |

## Read the research

| Guide | Covers |
|---|---|
| [Technical brief](EXTROPIC_BRIEF.md) | The research question, evidence, and hardware boundary |
| [DGX Spark verification](SPARK_VERIFICATION.md) | Complete model results, diagnostics, and limits |
| [Historical results](HISTORY.md) | Earlier adapted-model and cross-GPU experiments |
| [November 5 verification](BROAD_VERIFICATION_20261105.md) | Preserved earlier successes, failures, and nonideality studies |
| [Public data](../benchmarks/) | Machine-readable benchmark and audit summaries |

The [complete research repository](https://github.com/oramada/pbit1-research)
contains the manuscript and detailed artifacts and is **private**. The public
package contains encoding primitives, not a complete pretrained-model deployment
engine. It runs software simulations; it does not require or control physical
Extropic hardware.
