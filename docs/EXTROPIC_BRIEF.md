# Technical brief

## Research question

Can one programmable probabilistic element per learned scalar preserve useful
neural-network task quality when precision is supplied by temporal sampling and
shared local ranges?

The concept is stationary-probability encoding, with signed weights mapped as
`w = center + radius * (2p - 1)`. Probability encoding is established stochastic
computing; this project investigates finite controls, pretrained-model sensitivity,
and the resource tradeoff.

## Current evidence

The complete DGX Spark study converted all learned parameters of GPT-2,
DistilBERT, and LFM3-1.7B, including biases and normalization parameters. With
selected grouping, 12-bit probability controls, and 32,768 samples per scalar,
all three passed the frozen task-quality criteria on their evaluated datasets.

| Check | Result |
|---|---|
| GPT-2, 283,225 WikiText-2 targets | PPL ratio 1.00659; MC95 [0.99927, 1.01397] |
| DistilBERT, 25,000 IMDb reviews | Accuracy 87.4944% versus 87.512%; upper MC95 decline 0.08383 percentage points |
| LFM3, 294,442 WikiText-2 targets | PPL ratio 1.00259; MC95 [0.98751, 1.01790] |
| Reduced-work GPT-2 policy | 41.7% fewer nominal observations; upper MC95 PPL ratio 1.01660 |

These are five-seed, fixed-dataset quality results. The datasets had been inspected
previously. Full-model execution reconstructs sampled weights with independent
binomial counts, then uses ordinary BF16 neural operators.

## Mechanism and counterexamples

Original-layout GPT-2 fails at the same sampling budget. Restoring its output-head
use largely removes the failure, and operator-aware range orientation repairs the
full-model result. The appropriate layout differs between operators and models.

A stronger native four-element control achieves lower operator error than K1 at
equal scheduled observations, using additional elements and coarse information.
Finite-control collisions also rule out universal lossless BF16 conversion for
the tested format. Controller storage, ranges, and reconstructed arrays must be
counted alongside logical p-bit states.

## Relationship to Extropic

PBit1's optional native adapter uses the official THRML factors and Gibbs sampler,
pinned to commit `2d54cd8404df85bb65703d7e8b4e84e48c1b72a9`. Native tests are at
operator scale. The large-model independent-count simulator is our own code;
no physical Extropic hardware was used.

Useful next hardware measurements include probability calibration, temporal and
cross-device correlation, retained programming state, readout/accumulation costs,
and matched-quality comparisons with an agreed native representation. GPU
simulation and logical device counts do not establish an energy or latency advantage.

## Resources

- [Detailed current verification](SPARK_VERIFICATION.md)
- [Public benchmark summary](../benchmarks/spark_cross_model_20261106.json)
- [Package API](API.md)
- [Historical experiments](HISTORY.md)
- [Complete research and manuscript](https://github.com/oramada/pbit1-research) — private, access required

Independent research; no affiliation with or endorsement by Extropic or Liquid AI.
