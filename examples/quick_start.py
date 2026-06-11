#!/usr/bin/env python3
"""
CDSA-ATM Quick Start example.

Demonstrates loading the 15-class ATS occurrence taxonomy and
generating a small batch of synthetic occurrences.

Run:
    python examples/quick_start.py
"""

import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent

def load_taxonomy():
    """Load the 15-class ATS occurrence taxonomy."""
    with open(ROOT / "data" / "ats_taxonomy_15.json", encoding="utf-8") as f:
        return json.load(f)

def generate_synthetic_batch(n=10, seed=42):
    """Generate a small synthetic occurrence batch for demonstration."""
    random.seed(seed)
    tax = load_taxonomy()
    all_classes = tax["classical_classes"] + tax["cyber_safety_classes"]
    ansps = ["DHMI", "DFS", "ENAIRE"]
    batch = []
    for i in range(n):
        cls = random.choice(all_classes)
        batch.append({
            "id": f"occ_{i:04d}",
            "occurrence_class": cls["id"],
            "label": cls["label"],
            "severity": cls["esarr2"],
            "ansp": random.choice(ansps),
            "mitre_attack_id": cls["mitre"],
            "synthetic": True
        })
    return batch

def main():
    print("CDSA-ATM Quick Start")
    print("====================")
    print()
    tax = load_taxonomy()
    print(f"Taxonomy version: {tax['version']}")
    print(f"Classical classes: {len(tax['classical_classes'])}")
    print(f"Cyber-safety classes: {len(tax['cyber_safety_classes'])}")
    print()
    print("Sample synthetic batch (n=10, seed=42):")
    print("-" * 70)
    for occ in generate_synthetic_batch(n=10, seed=42):
        print(f"  [{occ['id']}] {occ['label']:32s} ANSP={occ['ansp']:8s} "
              f"sev={occ['severity']}  mitre={occ['mitre_attack_id']}")
    print()
    print("Next steps:")
    print("  python examples/fetch_opensky.py")
    print("  python examples/train_federated_ppo.py --algo fedavg --rounds 50")

if __name__ == "__main__":
    main()
