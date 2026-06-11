#!/usr/bin/env python3
"""
Unit tests for federated averaging utilities.
"""

import pytest
from src.federated_ppo import fed_avg, fed_prox

def test_fed_avg_basic():
    """FedAvg with three clients should return a placeholder dict."""
    w = [{"a": 1.0}, {"a": 2.0}, {"a": 3.0}]
    sizes = [100, 200, 100]
    result = fed_avg(w, sizes)
    assert result["n_clients"] == 3
    assert result["total_data"] == 400

def test_fed_avg_zero_data():
    """FedAvg should raise ValueError if all data sizes are zero."""
    w = [{"a": 1.0}, {"a": 2.0}]
    with pytest.raises(ValueError):
        fed_avg(w, [0, 0])

def test_fed_prox_includes_mu():
    """FedProx output should include the proximal coefficient mu."""
    w = [{"a": 1.0}, {"a": 2.0}]
    sizes = [100, 100]
    result = fed_prox(w, sizes, global_weights={"a": 0.5}, mu=0.05)
    assert result["mu"] == 0.05
    assert result["n_clients"] == 2
