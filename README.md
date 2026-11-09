<p align="center">
  <img src="docs/assets/banner.png" alt="PBit1 — weights as probabilities" width="100%">
</p>

<p align="center">
  <sub>PBit1 is independent and is not affiliated with or endorsed by Extropic.</sub>
</p>

<p align="center">
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/version-0.1.0a2.dev3-089b88" alt="Version 0.1.0a2.dev3"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-5260ce" alt="Apache-2.0"></a>
  <a href="https://github.com/oramada/pbit1/actions/workflows/ci.yml"><img src="https://github.com/oramada/pbit1/actions/workflows/ci.yml/badge.svg" alt="Tests"></a>
</p>

**Turn weights into probabilities. Recover them through sampling.**

PBit1 is a Python toolkit for probabilistic weights. Give it an array of numbers,
encode it, and reconstruct an approximate array using a repeatable sample process.
It runs on your computer with NumPy. Extropic’s THRML simulator is optional.

## Get started

Requires Python 3.12+ and Git.

```bash
python -m pip install "pbit1 @ git+https://github.com/oramada/pbit1.git@main"
python -m pbit1
```

The demo compares an original calculation with its sampled result.

## Use it in Python

```python
import pbit1

program = pbit1.encode([0.1, 0.5, 0.9])
result = program.reconstruct(4096, seed=7)

print(result.weights)
```

The output has the same shape as your input. Signed weights and NumPy matrices
work too. Increase the sample count to reduce sampling noise; keep the seed fixed
to repeat a result in the same environment.

[Step-by-step guide](docs/GETTING_STARTED.md) · [API reference](docs/API.md) · [Examples](examples/)

## Adjust the demo

```bash
pbit1 --samples 4096        # Use more samples
pbit1 --seed 42             # Try a different random draw
pbit1 --json                # Full output for scripts and diagnostics
```

For the official THRML simulator, follow the [THRML setup](docs/GETTING_STARTED.md#use-thrml).

## What’s included

- A simple Python API for encoding and reconstructing weight arrays.
- Repeatable sampling and explicit storage reporting.
- NumPy and optional THRML backends.
- Examples, tests, and published benchmark summaries.

PBit1 currently handles array encoding and simulation. Integration into a complete
neural network is manual. Stored controls and sampling have additional costs;
see [how it works](docs/FINITE_PROGRAM.md).

## Validation

Research configurations have been evaluated on GPT-2, DistilBERT, and LFM3-1.7B.
The selected configurations met their predefined task-quality margins against
BF16 on the tested datasets. [Read the results and test conditions](docs/SPARK_VERIFICATION.md).

## Help and project information

[Documentation](docs/README.md) · [Report an issue](https://github.com/oramada/pbit1/issues) ·
[Contribute](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [License](LICENSE)

Independent software by Omar Ramadan and contributors. Uses Extropic software
without affiliation or endorsement. [Third-party notices](NOTICE).
