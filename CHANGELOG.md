# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-scaffold] — 2026-05-22

### Added (Scenario C paradigm alignment, additive only)
- README.md: new "Paradigm Context — CDSA Scenario C" section
  positioning CDSA-ATM as the air traffic management pillar of the
  three-pillar Federated Reinforcement Learning (FRL) research
  programme.
- `src/rl_agents/` (scaffold)
- `src/rl_environment/` (scaffold)
- `src/multimodal/` (scaffold)
- `src/federated/` (scaffold)
- `src/xai/` (scaffold)
- `docs/scenario_c_paradigm_context.md` — full paradigm context
  reference document.
- `CITATION.cff`: added FRL/multi-modal/XAI/CDSA-paradigm keywords,
  Scenario C decision reference, sibling article references.
- `.zenodo.json`: added paradigm keywords and related-identifier
  entries for the three-pillar sibling repos.

### Not Changed
- v1.0.0 modules byte-identical to the v1.0.0 release. The v1.0.0
  release tag remains valid and reproducible.
- Reference data unchanged.
- Existing tests pass.
- Authorship policy (single-author per the CDSA Authorship Rule)
  unchanged.

### Notes
- The v2 scaffolded modules raise `NotImplementedError` when
  instantiated. Treat them as **architectural commitments**, not
  as runnable code at v2-scaffold stage.
- Full implementations of the scaffolded modules are deferred to
  TÜBİTAK 1001 ARDEB Project 4 (Sept 2026 application cycle;
  2027-2030 execution).
- The v2.0.0 final release is planned for Q4 2026 following
  TÜBİTAK project acceptance.

## [1.0.0] - 2026-05-17

### Added

- Initial public release of CDSA-ATM.
- README documenting the three-component architecture: real-time
  ADS-B and synthetic occurrence fusion, multi-agent federated PPO,
  and live cdsa.app/atm demonstration platform.
- Five-fold regulatory ontology (ICAO Annex 11 + Doc 4444 + EU
  Regulation 2017/373 + EUROCONTROL ESARR 2 + MITRE ATT&CK).
- Fifteen-class ATS occurrence typology with ESARR 2 cross-alignment.
- Three-ANSP simulated configuration: DHMİ + DFS + ENAIRE
  (Senaryo C — Avrupa + Türkiye hibrit).
- Documentation in `docs/`: federated RL methodology, ADS-B fusion
  design, occurrence taxonomy, validation protocol, cdsa.app/atm
  architecture.
- Example scripts in `examples/`: quick start, OpenSky data fetch,
  federated PPO training, reproducible scenario player.
- Unit tests for federated averaging and synthetic injection.
- Citation metadata: CITATION.cff and .zenodo.json.
- Dual licensing: MIT for code, CC-BY 4.0 for data/figures/docs.

### Pending

- Live training results and figures (added in v1.1 after Phase 3
  platform deployment).
- arXiv submission ID (added after upload).
- Zenodo DOI (added after release publication).

## [Unreleased]

### Planned for v1.1

- Federated training results on three simulated ANSPs.
- FedAvg vs FedProx comparative benchmarking on ATM tasks.
- Connection to live cdsa.app/atm demonstration platform.
- /reproduce/[scenario-id] endpoint specification.

### Planned for v2.0

- TÜBİTAK Project 4 field pilot integration with real ANSPs.
- Air Traffic Flow Management (ATFM) extension.
- Hierarchical federated learning structure.

## [2.1.0] — 2026-06-12 (Faz A implementation)
### Added
- `src/federated/`: FedAvgAggregator + FedProxAggregator NumPy reference
  implementations (ANSP consortium aggregation, Laplace DP hook,
  proximal utilities). Replaces v2.0.0-scaffold stubs.
- `src/multimodal/`: TrajectoryEncoder (1D-CNN+LSTM over ADS-B windows),
  ATSEventEncoder (self-attention over 15-class typology),
  ANSPCoordEncoder (LSTM) + CrossModalAttentionFusion (gating +
  scaled dot-product attention), federated param get/set.
- `src/rl_agents/ppo_actor_critic.py`: compact NumPy PPO Actor-Critic
  (clipped surrogate, GAE-lambda, manual gradients, federated params).
- `src/rl_environment/env.py`: ATMFlowEnv — seeded synthetic 12-dim /
  5-action flow environment with ESARR 2-inspired reward rules.
- `src/xai/`: SHAPModalityExplainer (exact Shapley), Counterfactual
  Explainer (auditor JSON), LIMEExplainer (ridge surrogate).
- `tests/test_v2_modules.py`: 6 unit tests incl. PPO learning check
  (trained agent beats random baseline). Total suite: 14/14 green.
### Notes
- Faz A scope: CPU-scale reference implementations (zero server cost).
  Framework-scale training remains under TUBITAK 1001 Project 4 (Faz B).

### Changed (11 Jun 2026, A6 runs)
- ATMFlowEnv: class-balanced state sampling (naive uniform sampling caused
  majority-class policy collapse: 84% accuracy with ZERO critical recall).
- PPOActorCritic: reward_scale + global gradient-norm clipping (critic
  divergence fix). Same robustness patch applied across all three pillars.
- experiments/: faz_a_staged.py + faz_a_config.py + results/ (seeded,
  checkpointed CPU-scale federated runs; see CDSA_FazA_A6 report).
