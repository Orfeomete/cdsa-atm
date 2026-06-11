"""
CDSA-ATM src.rl_agents — PPO Actor-Critic Agent Scaffold
==================================================================

Scaffold for the PPO Actor-Critic agent. Consumes the fused multi-modal
representation from `src.multimodal` and produces decisions over the
5-class action space:
  standard flow, speed restriction, route change, holding pattern, sector-wide alert

Status: scaffolded (v2). Full implementation is planned under
TÜBİTAK 1001 ARDEB Project 4.
"""

from .ppo_actor_critic import PPOActorCritic  # noqa: F401

__all__ = ["PPOActorCritic"]
