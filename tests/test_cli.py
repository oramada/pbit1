"""User-facing CLI contracts; the default must not need optional simulators."""
import json
import sys

import pytest
from pbit1 import __version__
from pbit1.__main__ import main


def test_default_demo_without_optional_backend(monkeypatch, capsys):
    monkeypatch.setitem(sys.modules, "pbit1.native", None)
    main(["--samples", "32", "--chains", "2", "--seed", "11"])
    result = json.loads(capsys.readouterr().out)
    assert result["backend"] == "numpy"
    assert result["version"] == __version__
    assert result["controls"]["logical_pbits"] == len(result["weights"])
    assert result["controls"]["controller_storage_bytes"] == 14
    assert result["expected_dot_product"] == 1.75
    assert result["samples_per_chain"] == 32
    assert result["independent_chains"] == 2


def test_cli_is_reproducible(capsys):
    args = ["--samples", "128", "--chains", "3", "--seed", "19"]
    main(args)
    first = capsys.readouterr().out
    main(args)
    assert capsys.readouterr().out == first


def test_version_does_not_import_optional_backend(monkeypatch, capsys):
    monkeypatch.setitem(sys.modules, "pbit1.native", None)
    with pytest.raises(SystemExit) as error:
        main(["--version"])
    assert error.value.code == 0
    assert capsys.readouterr().out.strip() == f"pbit1 {__version__}"


@pytest.mark.parametrize("args", [
    ["--samples", "0"], ["--chains", "-1"], ["--seed", "-1"],
    ["--samples", "4294967296"], ["--samples", "1.5"],
])
def test_invalid_arguments_show_usage(args, capsys):
    with pytest.raises(SystemExit) as error:
        main(args)
    assert error.value.code == 2
    assert "error:" in capsys.readouterr().err


def test_missing_optional_backend_has_actionable_message(monkeypatch, capsys):
    monkeypatch.setitem(sys.modules, "pbit1.native", None)
    with pytest.raises(SystemExit) as error:
        main(["--backend", "thrml"])
    assert error.value.code == 2
    assert "[thrml]" in capsys.readouterr().err
