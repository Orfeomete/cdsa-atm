# Federated Reinforcement Learning Methodology

## Overview

CDSA-ATM implements **Multi-Agent Federated Proximal Policy
Optimization (MA-FedPPO)**, modelling each Air Navigation Service
Provider (ANSP) as a separate agent under non-IID data conditions.

## Architecture

```
                    Federated Coordinator
                       (FedAvg / FedProx)
                              ▲
              ┌───────────────┼───────────────┐
              │               │               │
        Local PPO       Local PPO       Local PPO
         (DHMİ)          (DFS)         (ENAIRE)
              ▲               ▲               ▲
        Local data      Local data      Local data
        (synthetic +    (synthetic +    (synthetic +
         open ADS-B)     open ADS-B)     open ADS-B)
```

## State-Action-Reward Formulation

**State space `s ∈ S`:**
- Aircraft density vector (per sector)
- Sector occupancy indicators
- Instantaneous ATS occurrence signals (one-hot per 15 classes)
- Cyber-safety alert flags (10-bit vector)

**Action space `a ∈ A`:**
- Separation decision
- Rerouting
- Speed restriction
- Holding pattern activation
- Default (no intervention)

**Reward function `R_t`:**
```
R_t = w1 · (1 - violation) + w2 · efficiency - w3 · ATCO_workload
```

## Algorithm 1: MA-FedPPO

```
Input: N ANSPs, K federated rounds, E local epochs, batch B,
       learning rate α, PPO clipping ε, FedProx μ (optional)
Output: Global policy weights θ_global

1. Initialize global weights randomly: θ_global ← init()
2. for round k = 1, 2, ..., K do
3.   for each ANSP i ∈ {1, ..., N} in parallel do
4.     θ_i ← θ_global  // load global weights
5.     for epoch e = 1, ..., E do
6.       D_i ← local ATS occurrences + open ADS-B stream
7.       Compute advantage A(s,a) via GAE
8.       Minimize PPO clipped loss (+ proximal term if FedProx)
9.       θ_i ← θ_i - α ∇L(θ_i)
10.    end for
11.    Send θ_i to federated coordinator
12.  end for
13.  θ_global ← FedAvg({θ_1, ..., θ_N}) or FedProx({θ_1, ..., θ_N})
14. end for
15. return θ_global
```

## Hyperparameters

| Parameter | Value |
|-----------|-------|
| Federated agents N | 3 simulated ANSPs |
| Federated rounds K | 50 |
| Local epochs per round | 5 |
| Batch size | 64 |
| Learning rate α | 3e-4 |
| PPO clipping ε | 0.2 |
| Discount factor γ | 0.99 |
| FedProx μ | 0.01 |

## FedAvg vs FedProx

**FedAvg** [McMahan et al., 2017]: Data-weighted arithmetic mean of
local weights.

**FedProx** [Li et al., 2020]: Adds a proximal term to mitigate
performance loss under heterogeneous (non-IID) data distributions:

```
L_FedProx = L_PPO(θ_i) + (μ/2) · ||θ_i - θ_global||²
```

Both algorithms are compared in the experiments (see Section 4 of
the companion manuscript).

## References

- McMahan, B., et al. (2017). Communication-Efficient Learning of Deep
  Networks from Decentralized Data. AISTATS.
- Li, T., et al. (2020). Federated Optimization in Heterogeneous
  Networks. MLSys.
- Schulman, J., et al. (2017). Proximal Policy Optimization
  Algorithms. arXiv:1707.06347.
