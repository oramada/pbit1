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

**One logical p-bit per weight. Tested on models up to 1.73 billion parameters.**

Your network has millions—or billions—of weights. PBit1 lets you explore a
different way to represent them: encode each weight as a programmable probability,
then recover precision through sampling.

**The tradeoff: fewer binary-state bits, more sampling work.** Try it locally with
NumPy, tune the sampling budget, and inspect the storage costs. Extropic’s official
THRML simulator is available as an optional backend.

## The benchmark: close to BF16 task quality

Every learned parameter was converted in the selected research configurations,
including biases and normalization parameters.

| Model | Parameters | BF16 reference | PBit1 result | Change |
|:---|---:|---:|---:|:---|
| **GPT-2** | 124M | Perplexity 25.50149 | Perplexity 25.66953 | **+0.66% perplexity** |
| **DistilBERT** | 67M | Accuracy 87.512% | Mean accuracy 87.4944% | **−0.0176 percentage points** |
| **LFM3-1.7B** | 1.73B | Perplexity 18.93015 | Perplexity 18.97918 | **+0.26% perplexity** |

All three selected configurations passed their predefined quality margins across
five independent weight draws. A further GPT-2 configuration used **41.7% fewer
nominal sampling observations** while passing the same margin.

![Five-seed benchmark quality relative to BF16](docs/assets/spark_cross_model_20261106.svg)

These model runs used 32,768 samples per weight, 12-bit probability controls,
and shared ranges, followed by ordinary BF16 neural computation. They evaluate
fixed, previously inspected datasets. Lower perplexity is better. These are
task-quality results, not numerical BF16 equality, a speedup, or a memory-compression benchmark.

[Benchmark details and storage costs](docs/BENCHMARKS.md) ·
[Machine-readable results](benchmarks/spark_cross_model_20261106.json)

## Where does the 16× opportunity come from?

BF16 uses 16 bits per weight. One logical p-bit has one binary state:
**16× fewer binary-state bits**, counting states alone.

For the tested LFM3 model, that comparison is **3.458 GB of BF16 weights versus
0.216 GB of binary states**. Probability controls, shared ranges, and reconstructed
weights are additional. **The current Python package does not deliver 16× total
model-memory compression.** Its implemented command and range arrays alone
occupy 3.566 GB, before reconstructed weights.

PBit1 makes this design space testable: measure quality, sampling work, and
storage together before committing to a hardware implementation.
[See the complete accounting](docs/BENCHMARKS.md#what-the-storage-numbers-mean).

## Try it now

Requires Python 3.12+ and Git.

```bash
python -m pip install "pbit1 @ git+https://github.com/oramada/pbit1.git@main"
python -m pbit1
```

The demo shows the original result, sampled result, and difference. No model
download or hardware access is needed.

## Use your own weights

```python
import pbit1

program = pbit1.encode([0.1, 0.5, 0.9])
result = program.reconstruct(4096, seed=7)

print(result.weights)
```

Signed weights and NumPy matrices work too. The output keeps the input shape.
More samples generally reduce sampling noise; a fixed seed makes the draw
repeatable in the same environment.

```bash
pbit1 --samples 4096        # Explore a larger sampling budget
pbit1 --seed 42             # Try a different draw
pbit1 --json                # Inspect controls and diagnostics
```

The SDK handles array encoding and simulation. Full-model integration and
operator-specific range selection are manual; the three model benchmarks use
separate research runners, not the short array example above.

[Getting started](docs/GETTING_STARTED.md) · [API](docs/API.md) ·
[THRML setup](docs/GETTING_STARTED.md#use-thrml) · [Examples](examples/)

## Built to inspect, repeat, and extend

- **Start small:** encode an array and run a CPU demo in minutes.
- **Control the tradeoff:** choose sample counts and local weight groups.
- **See the costs:** report probability-control and range storage explicitly.
- **Build on the evidence:** public benchmark summaries, tests, and optional THRML integration.

[Documentation](docs/README.md) · [Report an issue](https://github.com/oramada/pbit1/issues) ·
[Contribute](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [License](LICENSE)

Independent software by Omar Ramadan and contributors. Uses Extropic software
without affiliation or endorsement. [Third-party notices](NOTICE).
