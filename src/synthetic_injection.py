#!/usr/bin/env python3
"""
Synthetic ATS Occurrence Injection Engine — v1 stub.

In v1.1, this module will implement the full deterministic
template-based synthetic occurrence engine parameterised over the
15-class typology with ESARR 2 distribution parameters.
"""

import random
import uuid
from datetime import datetime, timezone
from .ats_taxonomy import get_all_classes

ANSPS = ["DHMI", "DFS", "ENAIRE"]

def generate_occurrence(seed=None):
    """Generate a single synthetic ATS occurrence (stub)."""
    if seed is not None:
        random.seed(seed)
    cls = random.choice(get_all_classes())
    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "occurrence_class": cls["id"],
        "severity": cls["esarr2"],
        "ansp": random.choice(ANSPS),
        "sector": f"sector_{random.randint(1, 5)}",
        "synthetic": True,
        "mitre_attack_id": cls["mitre"]
    }

def generate_batch(n=100, seed=42):
    """Generate a batch of n synthetic occurrences (deterministic)."""
    random.seed(seed)
    return [generate_occurrence() for _ in range(n)]
