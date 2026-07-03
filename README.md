# CDSA-ATM

**ADS-B-Based Flow Simulation with Federated Reinforcement Learning within the Air Traffic Management Framework**

CDSA-ATM is the third sibling pillar of the **Complementary Diagnostic Safety Approach (CDSA)** framework, complementing CDSA-BlackBox (pilot/incident analysis) and CDSA-MRO (maintenance organisation). It targets the **Air Traffic Management (ATM)** domain through a federated reinforcement learning architecture trained on the real-time fusion of open ADS-B data and synthetic ATS occurrence injection.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA) [![Live Demo](https://img.shields.io/badge/Live%20Demo-cdsa.app%2Fatm-success)](https://cdsa.app/atm) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20649856.svg)](https://doi.org/10.5281/zenodo.20649856)

## Author

**Mete Cantekin**
PhD Candidate, Istanbul Beykent University, Department of Computer Engineering
metecantekin@gmail.com

## Overview

Air Traffic Management (ATM) services rely on heterogeneous data sources held by individual Air Navigation Service Providers (ANSPs). Commercial, regulatory, and operational constraints prevent the consolidation of these data into a centralised repository. **CDSA-ATM addresses this barrier through three components**:

1. **Real-time fusion** of open ADS-B data (OpenSky Network) with synthetic ATS occurrence injection
2. **Multi-agent federated PPO architecture** modelling each ANSP as a separate agent under non-IID conditions
3. **Live flow simulation** on the [cdsa.app/atm](https://cdsa.app/atm) platform with `/reproduce/` endpoints for independent verification

## Five-Fold Regulatory Ontology

The regulatory backbone integrates five canonical frameworks:

| # | Framework | Scope |
|---|-----------|-------|
| 1 | ICAO Annex 11 | Air Traffic Services |
| 2 | ICAO Doc 4444 | PANS-ATM operational procedures |
| 3 | EU Regulation 2017/373 | ATM/ANS Common Requirements (SES) |
| 4 | EUROCONTROL ESARR 2 | Occurrences Reporting and Assessment |
| 5 | MITRE ATT&CK | Cyber threat taxonomy |

## Fifteen-Class ATS Occurrence Typology

Five classical operational classes + ten cyber-safety extensions:

**Classical (5):** Loss of Separation, Runway Incursion, Airspace Infringement, Frequency Congestion, TCAS Resolution Advisory
**Cyber-safety (10):** GNSS Spoofing, GNSS Jamming, ADS-B Injection, Datalink Interruption, Surveillance Data Loss, ATM System Intrusion, Voice Channel Spoofing, NOTAM Tampering, Time Sync Attack, Position Falsification

Cross-mapping with ESARR 2 severity and MITRE ATT&CK techniques is provided in `docs/ats_occurrence_taxonomy.md`.

## Multi-Agent Federated PPO (MA-FedPPO)

The proposed federated reinforcement learning method:

- **N ANSPs** as separate agents (default `N=3`: DHMİ, DFS, ENAIRE)
- **Local training**: each ANSP runs PPO on its own data
- **Federated aggregation**: FedAvg (McMahan et al., 2017) or FedProx (Li et al., 2020)
- **Privacy preservation**: only policy parameters are shared, data remains local

See `docs/federated_rl_methodology.md` for details and the algorithm pseudo-code.

## Three-ANSP Simulated Configuration (Senaryo C)

| ANSP | Country | Sectors |
|------|---------|---------|
| DHMİ | Türkiye | Istanbul + Ankara + Izmir |
| DFS | Germany | Frankfurt + Munich |
| ENAIRE | Spain | Madrid + Barcelona |

This configuration captures Türkiye-EU integration within the Single European Sky framework.

---

## Paradigm Context — CDSA Scenario C (v2 update, 22 May 2026)

Following the **CDSA Methodological Unification Decision (Scenario C,
frozen status, 21 May 2026)**, this CDSA-ATM module is positioned
as the **air traffic management pillar** of a three-pillar **Federated
Reinforcement Learning (FRL)** research programme:

| Pillar | Domain | Companion repo | Companion journal article |
|---|---|---|---|
| **CDSA-BB3** | Pilot biometrics | `Orfeomete/cdsa-bb3` | JATM v8 (Q2, in submission) |
| **CDSA-MRO** | Maintenance safety | `Orfeomete/cdsa-mro` | RESS v2 (Q1, in preparation) |
| **CDSA-ATM** | Air traffic management | `Orfeomete/cdsa-atm` | CEAS v2 (Q2, in preparation) |

This **CDSA-ATM** repository implements the air traffic management
pillar with a **Multi-Agent PPO (multi-modal)** policy network operating
over **Trajectory + ATS + ANSP** modalities and a federated layer
designed for a ANSP consortium (DHMI, DFS, ENAIRE (simulated three-ANSP consortium)).
The sibling pillars are CDSA-BB3 (pilot biometrics, JATM Q2 v8 in submission) and the parallel MRO pillar; together they provide convergent
validation across three independent aviation domains.

A paradigm-defining umbrella article (Safety Science Q1, September 2026
submission target) positions the three pillars under a common
diagnostic-safety paradigm with quantitative convergent validation
evidence across the three domains.

The current `src/` layout retains the v1.0.0 modules and adds
**scaffolded FRL modules** for the paradigm extension. The v2 modules
are **scaffolds**: `__init__.py` + placeholder docstrings documenting
the planned interface. Full implementations are deferred to
**TÜBİTAK 1001 ARDEB Project 4** (September 2026 application cycle;
2027-2030 execution). Treat v2 modules as **architectural commitments**,
not as runnable code at this scaffold stage.

The four-component action space (or 5-class
for CDSA-ATM) is:
**standard flow, speed restriction, route change, holding pattern, sector-wide alert**.

For the paradigm-defining argument, refer to:
- `docs/scenario_c_paradigm_context.md` (paradigm context summary)
- The CDSA Methodological Unification Decision document (internal,
  cited as `[Cantekin 2026, CDSA Scenario C]`)
- The Safety Science Q1 umbrella article (in preparation,
  September 2026)

---

## Quick Start

```bash
git clone https://github.com/Orfeomete/cdsa-atm.git
cd cdsa-atm
pip install -r requirements.txt
python examples/quick_start.py
```

For OpenSky API integration:

```bash
python examples/fetch_opensky.py --bbox EU --duration 60
```

For federated PPO training:

```bash
python examples/train_federated_ppo.py --algo fedavg --rounds 50 --agents 3
```

## Repository Structure

```
cdsa-atm/
├── README.md                 ← This file
├── LICENSE                   ← MIT (code)
├── LICENSE-DATA              ← CC-BY 4.0 (synthetic datasets)
├── CITATION.cff              ← How to cite this work
├── CHANGELOG.md              ← Version history
├── CONTRIBUTING.md           ← Contribution guidelines
├── .zenodo.json              ← Zenodo DOI metadata
├── .gitignore
├── requirements.txt          ← Python dependencies
├── data/
│   ├── schema.json           ← ATS occurrence schema
│   ├── ats_taxonomy_15.json  ← 15-class typology
│   └── (placeholder for synthetic datasets)
├── docs/
│   ├── INDEX.md
│   ├── federated_rl_methodology.md
│   ├── ads_b_fusion_design.md
│   ├── ats_occurrence_taxonomy.md
│   ├── validation_protocol.md
│   └── cdsa_app_atm_architecture.md
├── examples/
│   ├── quick_start.py
│   ├── fetch_opensky.py
│   ├── train_federated_ppo.py
│   └── reproduce_section_4_2.py
├── src/
│   ├── __init__.py
│   ├── federated_ppo.py
│   ├── synthetic_injection.py
│   └── ats_taxonomy.py
├── tests/
│   ├── test_federated_average.py
│   └── test_synthetic_injection.py
└── figures/
    └── (placeholder for training curves and architecture diagrams)
```

## Live Demonstration Platform

The trained federated global policy runs in real time at [https://cdsa.app/atm](https://cdsa.app/atm). The platform fuses OpenSky Network open ADS-B data with synthetic ATS occurrence injection and visualises the operational decisions of the federated global policy in real time.

Every scenario referenced in the companion manuscript is independently reproducible via `/reproduce/[scenario-id]` endpoints.

> The federated training is conducted offline; the resulting global policy checkpoint is loaded into the live inference server.

## Experiment Phases (Faz A–D)

The `experiments/` folder contains four phases of seeded CPU-scale runs
(seed 42, FedProx unless noted). All outputs live under
`experiments/results/`; the interactive result panels with honesty bands
at **https://cdsa.app/atm/** read those JSONs verbatim.

- **Faz A — seeded reference runs** (`faz_a_staged.py`, `faz_a_run.py`):
  federated baselines (FedAvg / FedProx / FedProx+DP) vs Central PPO.
  Finding: the high critical recall (0.919) is achieved inside the
  over-alert regime characterised in Faz B.
- **Faz B — robustness & confusion matrix** (`faz_b_robustness.py`,
  `faz_b_dynamic_reward.py`): seeded inference-time perturbations plus a
  tempo-aware-reward retraining. Finding: the policy uses only 2 of 5
  actions and every benign state receives a critical prediction — an
  over-alert regime; the tempo-aware reward does not improve on the
  static baseline.
- **Faz C — ε sweep & entropy-targeted exploration**
  (`faz_c_dp_sweep.py`, `faz_c_entropy.py`): DP ε ∈ {0.5, 2.0} and
  entropy ∈ {0.01, 0.05} retrainings. Finding: the ε sweep is two-sided
  (ε = 2.0 matches the undefended baseline, ε = 0.5 collapses the policy
  to a single action); a 0.05 entropy bonus recovers all five actions,
  but critical recall falls from 0.927 to 0.878.
- **Faz D — decoy attribution & gated exploration** (`faz_d_decoy.py`,
  `faz_d_gated_entropy.py`): two irrelevant U(0,1) channels with
  group-Shapley attribution; entropy active only above a 0.90
  critical-recall floor. Finding: decoy attribution stays below the 25%
  uniform share (mean 15.3%); gated exploration preserves recall (0.928)
  but the policy remains two-action.

### How to reproduce

```bash
cd experiments
python faz_b_robustness.py
python faz_b_dynamic_reward.py
python faz_c_dp_sweep.py
python faz_c_entropy.py
python faz_d_decoy.py
python faz_d_gated_entropy.py
```

Each script is seeded and writes its results JSON into
`experiments/results/`.

## Companion Publications

- **PhD Thesis (preliminary draft v1)**: *"ADS-B-Based Flow Simulation with Federated Reinforcement Learning within the Air Traffic Management Framework"*, Istanbul Beykent University, May 2026.
- **Journal article (under preparation, target Q2)**: CEAS Aeronautical Journal (Springer), target submission 30 June 2026.
- **arXiv preprint v1**: cs.LG (primary), cs.CR (secondary), cs.SY (cross-list). arXiv ID forthcoming.
- **TÜBİTAK 1001 Project 4 (planned)**: Federated RL for ATM Safety Prediction, target submission September 2027.

## CDSA Framework — Sibling Repositories

CDSA-ATM is part of a three-pillar CDSA framework:

- [cdsa-blackbox](https://github.com/Orfeomete/cdsa-blackbox) — Pilot/incident analysis
- [cdsa-mro](https://github.com/Orfeomete/cdsa-mro) — Maintenance organisation
- **cdsa-atm** (this repository) — Air Traffic Management

Each pillar provides convergent validation of the same paradigm: **federated reinforcement learning + synthetic data + cyber-safety + data locality** across three independent aviation domains.

## Citation

If you use this work, please cite:

```bibtex
@software{cantekin2026cdsaatm,
  author = {Cantekin, Mete},
  title = {CDSA-ATM: ADS-B-Based Flow Simulation with Federated
           Reinforcement Learning within the Air Traffic Management
           Framework},
  year = {2026},
  publisher = {Zenodo},
  version = {2.2.0},
  doi = {10.5281/zenodo.20649856}
}
```

See `CITATION.cff` for the full citation metadata.

## Licence

- **Code**: MIT Licence (see `LICENSE`)
- **Synthetic datasets and figures**: Creative Commons Attribution 4.0 International — CC-BY 4.0 (see `LICENSE-DATA`)

## Acknowledgements

The author thanks the **OpenSky Network** team for providing open ADS-B data access under academic licence, and **EUROCONTROL** for the ESARR 2 occurrence classification framework that informs the regulatory ontology of this work.

## Contact

**Mete Cantekin** · metecantekin@gmail.com
PhD Candidate, Istanbul Beykent University

For questions, issues, or contributions, please open an issue on GitHub or contact via email.

---

*CDSA-ATM v1.0.0 — May 2026 · The third pillar of the CDSA framework.*
