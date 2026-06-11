#!/usr/bin/env python3
"""
Unit tests for the synthetic ATS occurrence injection engine.
"""

from src.synthetic_injection import generate_occurrence, generate_batch
from src.ats_taxonomy import get_all_classes

def test_generate_occurrence_returns_required_fields():
    occ = generate_occurrence(seed=42)
    required = {"id", "timestamp", "occurrence_class", "severity", "ansp",
                "sector", "synthetic", "mitre_attack_id"}
    assert required.issubset(occ.keys())

def test_generate_occurrence_class_is_valid():
    occ = generate_occurrence(seed=42)
    all_ids = {c["id"] for c in get_all_classes()}
    assert occ["occurrence_class"] in all_ids

def test_generate_occurrence_severity_valid():
    occ = generate_occurrence(seed=42)
    assert occ["severity"] in {"A", "B", "C"}

def test_generate_batch_size():
    batch = generate_batch(n=25, seed=42)
    assert len(batch) == 25

def test_generate_batch_deterministic():
    b1 = generate_batch(n=10, seed=42)
    b2 = generate_batch(n=10, seed=42)
    # The class assignments should match (timestamps and IDs may differ)
    classes1 = [o["occurrence_class"] for o in b1]
    classes2 = [o["occurrence_class"] for o in b2]
    assert classes1 == classes2
