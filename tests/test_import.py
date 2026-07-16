"""
Basic import tests to ensure the package structure is correct.
"""
import pytest
import sys
from pathlib import Path

# Ensure src is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

def test_import_core():
    from core import mapping, objective, kb_builder, piano_builder
    assert mapping is not None
    assert objective is not None
    assert kb_builder is not None
    assert piano_builder is not None

def test_import_optimiser():
    from core.optimiser import simulated_annealing, neighbourhood
    assert simulated_annealing is not None
    assert neighbourhood is not None

def test_import_cli():
    from cli import main
    assert main is not None

def test_import_evaluation():
    from evaluation import metrics, plots
    assert metrics is not None
    assert plots is not None

def test_import_calibration():
    from calibration import run_calibration
    assert run_calibration is not None