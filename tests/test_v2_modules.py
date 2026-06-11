"""Unit tests for the CDSA-ATM v2 modules (Faz A implementation)."""

import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.federated.fedavg import FedAvgAggregator
from src.federated.fedprox import FedProxAggregator
from src.multimodal.encoders import (ANSPCoordEncoder, ATSEventEncoder,
                                     TrajectoryEncoder)
from src.multimodal.fusion import CrossModalAttentionFusion
from src.rl_agents.ppo_actor_critic import PPOActorCritic
from src.rl_environment.env import ATMFlowEnv
from src.xai.counterfactual import CounterfactualExplainer
from src.xai.lime_explainer import LIMEExplainer
from src.xai.shap_explainer import SHAPModalityExplainer

RNG = np.random.default_rng(0)
L = 64


def _toy(scale):
    return {"W": np.full((2, 2), float(scale))}


def test_fedavg_and_fedprox():
    agg = FedAvgAggregator()
    out = agg.aggregate([_toy(0), _toy(1)], [1, 3])
    assert np.allclose(out["W"], 0.75)
    prox = FedProxAggregator(mu=0.5)
    assert np.isclose(prox.proximal_penalty(_toy(2), _toy(0)), 0.5 * 0.5 * 16)


def test_encoders_and_fusion():
    h_t = TrajectoryEncoder(seed=1).forward(RNG.normal(size=(25, 6)))
    h_a = ATSEventEncoder(seed=1).forward(RNG.normal(size=(8, 18)))
    h_k = ANSPCoordEncoder(seed=1).forward(RNG.normal(size=(10, 6)))
    for h in (h_t, h_a, h_k):
        assert h.shape == (L,) and np.all(np.isfinite(h))
    fus = CrossModalAttentionFusion(seed=2)
    out, gates = fus.forward(h_t, h_a, h_k, return_gates=True)
    assert out.shape == (L,)
    assert set(gates) == {"trajectory", "ats", "coord"}


def test_env_api_and_reward_rules():
    env = ATMFlowEnv(seed=7, max_steps=5)
    s, _ = env.reset()
    assert s.shape == (12,)
    # force a known state: widespread cyber -> action 4 expected
    env._state = np.array([.5, .5, .5, .5, .5, .5, .2, .9, .8, .1, .1, .1])
    _, r, _, _, info = env.step(4)
    assert r == 10.0 and info["appropriate_action"] == 4
    env._state = np.array([.5, .5, .5, .5, .5, .5, .9, .1, .9, .1, .1, .1])
    _, r2, _, _, _ = env.step(0)   # missed critical (holding expected)
    assert r2 < -20.0


def test_ppo_shapes_and_param_roundtrip():
    agent = PPOActorCritic(fused_dim=12, n_actions=5, seed=3)
    s = RNG.normal(size=12)
    p = agent.policy(s)
    assert p.shape == (5,) and np.isclose(p.sum(), 1.0)
    a, logp, v = agent.act(s)
    assert 0 <= a < 5 and np.isfinite(logp) and np.isfinite(v)
    other = PPOActorCritic(fused_dim=12, n_actions=5, seed=99)
    other.set_params(agent.params())
    assert np.allclose(other.policy(s), p)


def test_ppo_learns_on_env():
    """Mean reward after training must beat the random policy baseline."""
    env = ATMFlowEnv(seed=11, max_steps=10_000)
    agent = PPOActorCritic(fused_dim=12, n_actions=5, hidden=64,
                           lr=0.05, reward_scale=0.05, seed=11)

    def rollout(policy_random=False):
        s, _ = env.reset(seed=123)
        S, A, LP, Rw, V, D = [], [], [], [], [], []
        for _ in range(128):
            if policy_random:
                a = int(RNG.integers(5)); logp = np.log(0.2); v = 0.0
            else:
                a, logp, v = agent.act(s)
            s2, r, term, trunc, _ = env.step(a)
            S.append(s); A.append(a); LP.append(logp)
            Rw.append(r); V.append(v); D.append(term or trunc)
            s = s2
        return S, A, LP, Rw, V, D

    base = np.mean(rollout(policy_random=True)[3])
    for _ in range(160):
        S, A, LP, Rw, V, D = rollout()
        adv, ret = agent.compute_gae(Rw, V, D)
        agent.update(S, A, LP, adv, ret, epochs=3)
    trained = np.mean(rollout()[3])
    assert trained > base + 1.0, f"trained={trained:.2f} base={base:.2f}"


def test_xai_suite():
    def head(h_t, h_a, h_k):
        f = np.array([h_t.mean(), h_a.mean(), h_k.mean()])
        W = np.array([[1.0, .1, .2], [.2, 1.2, .1], [.1, 1.8, .1],
                      [.3, .4, 1.5], [.1, 2.0, .3]])
        return W @ f
    lat = {"trajectory": np.full(L, .3), "ats": np.full(L, 2.0),
           "coord": np.full(L, .2)}
    shap = SHAPModalityExplainer(head)
    pct = shap.contribution_percentages(lat)
    assert max(pct, key=pct.get) == "ats"
    cf = CounterfactualExplainer(head, action_labels=list("abcde"))
    res = cf.counterfactual(lat, "ats")
    assert res["decision_changed"] is True
    lime = LIMEExplainer(lambda x: np.array([2.5 * x[0], 0.0]),
                         n_samples=300, seed=4)
    assert lime.explain(np.ones(3), action=0)["top_features"][0]["index"] == 0
