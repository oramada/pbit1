# Benchmarks: quality, sampling, and storage

PBit1's strongest demonstrated result is task-quality preservation with one
logical programmable p-bit per learned scalar. It is important to distinguish
that result from total memory compression or a physical hardware speedup.

## Complete-model quality

The selected configurations convert all learned parameters, including biases and
normalizations. Tied embeddings and output heads share one representation.

| Model/task | Scored evaluation | BF16 | Selected K1 | Ratio and five-seed MC95 interval |
|---|---|---:|---:|---|
| GPT-2 / WikiText-2 | 283,225 targets | PPL 25.50149 | PPL 25.66953 | 1.00659 [0.99927, 1.01397] |
| DistilBERT / IMDb | 25,000 reviews | Accuracy 87.512% | Mean accuracy 87.4944% | Categorical PPL 0.99966 [0.99676, 1.00256] |
| LFM3 / WikiText-2 | 294,442 targets | PPL 18.93015 | PPL 18.97918 | 1.00259 [0.98751, 1.01790] |

The language-model percentages in the README are relative perplexity changes,
not percentages of accuracy retained. DistilBERT's accuracy change is an absolute
0.0176 percentage-point decline. Its upper MC95 decline is 0.08383 percentage
points, below its two-point margin. All three selected conditions also meet the
frozen upper-confidence-bound probability-quality ratio of 1.02.

Each model uses 32,768 samples per scalar, finite 12-bit probability commands,
and shared local ranges selected using training/calibration data. Full-model
runs draw independent binomial counts to reconstruct weights and then execute
ordinary BF16 neural operators. The sampled model is reused across the task.

There are five independent stochastic weight draws per selected configuration.
The intervals quantify draw-to-draw variability on fixed data, not generalization
to every task. These datasets were inspected in prior experiments. Native THRML
validation is at operator scale; these are not complete model runs on physical
Extropic hardware.

[Raw summary](../benchmarks/spark_cross_model_20261106.json) ·
[Detailed verification](SPARK_VERIFICATION.md)

## Less sampling work at the same quality margin

A separate GPT-2 study uses a fixed sensitivity-based allocation selected from
training/calibration data. It retains one logical p-bit per parameter and a
maximum sample count of 32,768.

| Policy | Nominal observations per reconstruction | PPL ratio | MC95 upper bound |
|---|---:|---:|---:|
| Uniform | 4,077,643,628,544 | 1.00659 | 1.01397 |
| Sensitivity-based | 2,378,245,865,472 | 1.00780 | 1.01660 |

The reduction is **41.7%**, with 53,088 extra bytes of range metadata. Both
five-seed cohorts pass the same quality margin. This is not a measured inference
latency or energy reduction, and the two cohorts do not prove identical quality.

[Budget summary](../benchmarks/spark_reduced_work_20261106.json) ·
[Independent audit](../benchmarks/spark_reduced_work_audit_20261106.json)

## What the storage numbers mean

For the tested LFM3 model, there are 1,728,801,536 unique learned scalars and
13,542,448 range groups. GB below means decimal gigabytes.

| Representation or payload | GB | Interpretation |
|---|---:|---|
| BF16 weights | 3.458 | Two bytes per weight |
| K1 binary states alone | 0.216 | One state bit per weight; excludes controls and ranges |
| Ideal packed commands + ranges + states | 2.918 | 12-bit commands; hypothetical packing, not the NumPy layout |
| Implemented command + range arrays | 3.566 | uint16 commands and two FP32 values per group; no decoded weights |
| Implemented arrays + decoded BF16 weights | 7.024 | Illustrative R1 payload; software overhead and other buffers are additional |

The 16× figure compares only 16 BF16 bits with one binary state. A programmed
probability carries additional information in its controls. It cannot be omitted
from the accounting. Retaining an original reference copy adds another BF16
payload; the SDK's standalone reconstruction returns FP32, which also requires
more storage than BF16. Python objects, sampling counters, transient buffers,
and real control circuitry are separate costs.

The current SDK therefore does **not** demonstrate 16× model-file compression,
16× lower RAM/VRAM use, or 16× higher hardware density. The ideal packed total
above is about 84.38% of the BF16 weight payload, before working weights and
system costs. Physical p-bit area cannot be inferred from a bit-count ratio.

[Exact four-configuration ledger](../benchmarks/spark_storage_20261106.json) ·
[Program storage API](FINITE_PROGRAM.md#storage-accounting)

## Failure cases remain part of the result

At the same 32,768 samples, original-layout GPT-2 misses its quality margin
(PPL ratio 1.05964). Operator-aware grouping repairs this tested failure. The
SDK does not select those layouts automatically.

A stronger four-element native control achieves lower operator MSE at equal
scheduled observations, with additional elements and coarse control information.
K1 is not a universal accuracy or efficiency winner. Finite-controller collisions
also exclude lossless numerical BF16 conversion for the tested format.

The practical use of this package is to explore and measure these tradeoffs.
Claims about broad model conversion, deployment efficiency, or physical energy
savings require additional benchmarks and device measurements.
