"""Faz A / A6 run configuration — CDSA-ATM pillar."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.rl_environment.env import ATMFlowEnv, ACTIONS

PILLAR = "CDSA-ATM"
N_ACTIONS = 5
STATE_DIM = 12
NEW_STEP_API = True
INFO_TRUE_KEY = "appropriate_action"
ACTION_LABELS = list(ACTIONS)
MODALITY_GROUPS = {"trajectory": np.r_[0:6], "ats": np.r_[6:9],
                   "coord": np.r_[9:12]}

# Non-IID heterojenlik: istemci basina farkli siber olay orani
_CLIENT_CYBER_RATES = (0.05, 0.12, 0.25)   # DHMI, DFS, ENAIRE (sim)


def make_env(seed: int):
    return ATMFlowEnv(seed=seed, max_steps=10_000)


def make_client_envs(seed: int):
    return [ATMFlowEnv(seed=seed + i, max_steps=10_000, cyber_rate=r)
            for i, r in enumerate(_CLIENT_CYBER_RATES)]

CRITICAL_ACTIONS = set((3, 4))
