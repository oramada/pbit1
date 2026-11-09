# Contributing

PBit1 welcomes focused improvements to the SDK, reproducible bug reports, and
clearly scoped experiment contributions.

## Local setup

```bash
git clone https://github.com/oramada/pbit1.git
cd pbit1
python -m venv .venv
source .venv/bin/activate
python -m pip install '.[dev]'
python -m pytest -q
python examples/quickstart.py
python -m pbit1 --samples 32 --chains 2
python -m build
```

Requires Python 3.12+. On Windows, activate with `.venv\Scripts\activate`.
Install `.[thrml,dev]` to run the optional official-backend tests and example:

```bash
python -m pytest -q tests/test_native.py
python -m pbit1 --backend thrml --samples 32 --chains 2
```

## Bug reports and changes

Open an [issue](https://github.com/oramada/pbit1/issues) with the package and Python
versions, operating system, backend, a small runnable example, and the full error.
For sampling differences, include the seed, sample count, grouping, and NumPy
version. Avoid posting private checkpoints or credentials.

Keep NumPy-only use independent of optional JAX/THRML imports. Add focused tests
for behavior changes and update the relevant example or API documentation.
Preserve published benchmark values and their provenance; new experiments should
have separate inputs, seeds, and result files.

## Research claims

Distinguish logical state count from controller/range storage, numerical precision
from task quality, and simulation from measured hardware. Label changes to the
one-p-bit constraint explicitly. Full research artifacts live in the separate
private research repository; contributions do not imply access to that repository.
