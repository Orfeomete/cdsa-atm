#!/usr/bin/env python3
"""
ATS Occurrence Taxonomy — 15-class typology loader and utilities.
"""

import json
from pathlib import Path

TAXONOMY_PATH = Path(__file__).parent.parent / "data" / "ats_taxonomy_15.json"

def load_taxonomy():
    """Load the 15-class typology from data/ats_taxonomy_15.json."""
    with open(TAXONOMY_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_all_classes():
    """Return a flat list of all 15 occurrence classes."""
    tax = load_taxonomy()
    return tax["classical_classes"] + tax["cyber_safety_classes"]

def get_class_by_id(occ_id):
    """Look up a class by its id (e.g., 'gnss_spoofing')."""
    for c in get_all_classes():
        if c["id"] == occ_id:
            return c
    raise KeyError(f"Unknown occurrence class: {occ_id}")

def classify_by_severity(severity):
    """Return all classes with the given ESARR 2 severity (A/B/C)."""
    return [c for c in get_all_classes() if c["esarr2"] == severity]
