"""
ATMFlowEnv — NumPy reference implementation (v2).

A Gymnasium-style synthetic ATM flow environment for the CDSA-ATM agent.

State  s (12-dim, normalised [0,1]): aircraft density (3), sector
       occupancy (3), ATS occurrence signal (3: operational, cyber,
       severity), inter-ANSP coordination indicators (3).
Action a (5 discrete): standard flow (0), speed restriction (1),
       route change (2), holding pattern (3), sector-wide alert (4).
Reward: correct action +10 · false alert (unneeded 4) -5 ·
        missed critical state -20*(severity+1) · mild mismatch -1.

The hidden "appropriate action" is derived from the state by an
ESARR 2-inspired rule set, so learning progress is measurable while the
environment remains fully synthetic and reproducible (seeded).

Scope note (Faz A): CPU-scale synthetic environment. OpenSky real-scale
validation is planned under TUBITAK 1001 ARDEB Project 4 (Faz B).
"""

from __future__ import annotations

import numpy as np

ACTIONS = ("standard_flow", "speed_restriction", "route_change",
           "holding_pattern", "sector_wide_alert")


class ATMFlowEnv:
    """Synthetic three-modality ATM flow environment (seeded)."""

    N_ACTIONS = 5
    STATE_DIM = 12

    def __init__(self, seed: int = 42, max_steps: int = 200,
                 cyber_rate: float = 0.12):
        self.rng = np.random.default_rng(seed)
        self.max_steps = int(max_steps)
        self.cyber_rate = float(cyber_rate)
        self._t = 0
        self._state = None

    # -- hidden rule set (ESARR 2-inspired) ----------------------------
    def _appropriate_action(self, s: np.ndarray) -> int:
        density = s[0:3].mean()
        occupancy = s[3:6].mean()
        ats_ops, ats_cyber, severity = s[6], s[7], s[8]
        coord_conflict = s[9:12].mean()
        if ats_cyber > 0.7 and severity > 0.6:
            return 4                       # widespread cyber -> sector alert
        if severity > 0.7 and ats_ops > 0.5:
            return 3                       # critical occurrence -> holding
        if density > 0.75 and occupancy > 0.6:
            return 2 if coord_conflict > 0.5 else 1
        if occupancy > 0.7:
            return 1
        return 0

    def _sample_state(self) -> np.ndarray:
        """Class-balanced state sampling.

        Naive uniform sampling makes 'standard flow' ~84% of states and
        drives policies to a degenerate majority-class collapse (verified
        in Faz A runs, 11 Jun 2026). States are therefore sampled from a
        target class mixture; the cyber_rate parameter scales the
        sector-wide-alert (cyber) share, preserving Non-IID heterogeneity
        across consortium clients.
        """
        p4 = min(max(self.cyber_rate, 0.02), 0.5)
        rest = 1.0 - p4
        probs = np.array([0.40, 0.22, 0.14, 0.24]) * rest   # classes 0-3
        probs = np.append(probs, p4)
        target = int(self.rng.choice(5, p=probs / probs.sum()))
        for _ in range(200):
            s = self.rng.uniform(0, 1, self.STATE_DIM)
            if target == 4:
                s[7] = self.rng.uniform(0.72, 1.0)
                s[8] = self.rng.uniform(0.62, 1.0)
            elif target == 3:
                s[7] = self.rng.uniform(0.0, 0.65)
                s[8] = self.rng.uniform(0.72, 1.0)
                s[6] = self.rng.uniform(0.52, 1.0)
            elif target == 2:
                s[0:3] = self.rng.uniform(0.76, 1.0, 3)
                s[3:6] = self.rng.uniform(0.62, 1.0, 3)
                s[9:12] = self.rng.uniform(0.52, 1.0, 3)
                s[7] *= 0.5; s[8] *= 0.5
            elif target == 1:
                s[3:6] = self.rng.uniform(0.72, 1.0, 3)
                s[0:3] = self.rng.uniform(0.0, 0.74, 3)
                s[7] *= 0.4; s[8] *= 0.5
            else:
                s[3:6] *= 0.65
                s[0:3] *= 0.7
                s[7] *= 0.3; s[8] *= 0.5
            if self._appropriate_action(s) == target:
                return s
        return s

    # -- gym-style API ---------------------------------------------------
    def reset(self, seed: int | None = None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self._t = 0
        self._state = self._sample_state()
        return self._state.copy(), {}

    def step(self, action: int):
        if self._state is None:
            raise RuntimeError("call reset() first")
        a_true = self._appropriate_action(self._state)
        severity = float(self._state[8])
        if action == a_true:
            reward = 10.0
        elif action == 4 and a_true != 4:
            reward = -5.0                  # false sector-wide alert
        elif a_true >= 3 and action < a_true:
            reward = -20.0 * (severity + 1.0)   # missed critical state
        else:
            reward = -1.0                  # mild mismatch
        self._t += 1
        terminated = False
        truncated = self._t >= self.max_steps
        self._state = self._sample_state()
        info = {"appropriate_action": a_true,
                "appropriate_label": ACTIONS[a_true]}
        return self._state.copy(), reward, terminated, truncated, info
