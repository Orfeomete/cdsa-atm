"""
CDSA-ATM src.rl_environment — State-Action-Reward Environment Scaffold
============================================================================

Scaffold for the Gymnasium-compatible environment wrapping the
multi-modal data stream (ADS-B trajectory + ATS occurrence + ANSP coordination) as a Markov decision process
for PPO training.

Status: scaffolded (v2). Full implementation is planned under
TÜBİTAK 1001 ARDEB Project 4.
"""

from .env import ATMFlowEnv  # noqa: F401

__all__ = ["ATMFlowEnv"]
