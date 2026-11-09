"""Encode numerical weights as programmable probabilities."""
from .encodings.single_pbit import SinglePBit, SinglePBitWeights
from .program import FinitePBitProgram, Reconstruction

__version__ = "0.1.0a2.dev3"
encode = FinitePBitProgram.encode

__all__ = [
    "encode", "FinitePBitProgram", "Reconstruction",
    "SinglePBit", "SinglePBitWeights", "NativeProbabilityBank",
]


def __getattr__(name):
    if name == "NativeProbabilityBank":
        from .native import NativeProbabilityBank
        return NativeProbabilityBank
    raise AttributeError(name)
