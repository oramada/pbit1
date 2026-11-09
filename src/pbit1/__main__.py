"""Run a small, reproducible single-p-bit weight demonstration."""

import argparse
import json

import numpy as np

from . import __version__
from .program import FinitePBitProgram


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def nonnegative_int(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be a nonnegative integer")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=f"pbit1 {__version__}")
    parser.add_argument(
        "--backend", choices=("numpy", "thrml"), default="numpy",
        help="numpy: independent-count reconstruction (default); thrml: official sampler",
    )
    parser.add_argument("--samples", type=positive_int, default=256,
                        help="observations per weight and chain (default: 256)")
    parser.add_argument("--chains", type=positive_int, default=4,
                        help="independent draws to average (default: 4)")
    parser.add_argument("--seed", type=nonnegative_int, default=7,
                        help="reproducible random seed (default: 7)")
    options = parser.parse_args(argv)
    if options.samples > 2**32 - 1:
        parser.error("--samples must be at most 4294967295")

    weights = np.array([0., .125, .25, .5, .75, .875, 1.])
    inputs = np.array([1., -.5, .25, 1., -.25, .5, 1.])
    result = {
        "version": __version__,
        "backend": options.backend,
        "weights": weights.tolist(),
        "samples_per_chain": options.samples,
        "independent_chains": options.chains,
        "seed": options.seed,
        "expected_dot_product": float(weights @ inputs),
    }

    if options.backend == "numpy":
        program = FinitePBitProgram.encode(weights, group_size=weights.size)
        estimates = np.stack([
            program.reconstruct(options.samples, seed=options.seed,
                                parameter_index=chain).weights
            for chain in range(options.chains)
        ])
        result.update({
            "controls": program.storage(),
            "finite_controller_mean_weights": program.expectation().tolist(),
            "reconstructed_weights": estimates.mean(axis=0).tolist(),
            "sampled_output_mean": float((estimates @ inputs).mean()),
            "scope": "NumPy independent-binomial reconstruction with finite 12-bit "
                     "commands and shared ranges. No THRML or physical device execution. "
                     "Control storage and decoded weights remain additional costs.",
        })
    else:
        try:
            from .native import NativeProbabilityBank
        except ImportError:
            parser.exit(2, "The THRML backend requires the optional [thrml] extra.\n"
                        "Install: python -m pip install 'pbit1[thrml] @ "
                        "git+https://github.com/oramada/pbit1.git@main'\n")
        bank = NativeProbabilityBank(weights)
        states = bank.sample(options.seed, options.samples, options.chains)
        result.update({
            "controls": bank.controls(),
            "realized_probabilities_from_float32_controls": bank.realized_probabilities.tolist(),
            "sample_means": states.mean(axis=(0, 1)).tolist(),
            "sampled_output_mean": float((states.astype(np.float64) @ inputs).mean()),
            "scope": "Official THRML CPU simulator. One logical p-bit per probability "
                     "weight, with programmable controls and clamped endpoints. "
                     "No physical hardware or BF16-equivalence claim.",
        })
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
