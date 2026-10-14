"""E13 kosucusu. On kayit E13_ON_KAYIT_11102026.md."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import numpy as np
from scipy import stats
import gymnasium as gym

HERE = Path(__file__).resolve().parent
sys.path.insert(0, '/home/claude/kk')
import gecis_bagimliligi_testi as gt

K, M, ALFA = gt.K, gt.M, gt.ALFA
ORTAMLAR = ["CartPole-v1", "MountainCar-v0", "Acrobot-v1",
            "FrozenLake-v1", "Taxi-v3", "CliffWalking-v0"]


def ozet(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def durum_al(env):
    u = env.unwrapped
    if hasattr(u, 'state') and u.state is not None:
        return np.array(u.state, dtype=float).copy()
    return np.array([int(u.s)], dtype=float)


def durum_ata(env, s):
    u = env.unwrapped
    if hasattr(u, 'state') and getattr(u, 'state', None) is not None:
        u.state = np.array(s, dtype=float).copy()
        if hasattr(u, 'steps_beyond_terminated'):
            u.steps_beyond_terminated = None
    else:
        u.s = int(s[0])


def durumlar(ad):
    env = gym.make(ad)
    env.reset(seed=7)
    rng = np.random.default_rng(7)
    out, t = [], 0
    while len(out) < K:
        if t % 3 == 0:
            out.append(durum_al(env))
        _, _, te, tr, _ = env.step(int(rng.integers(env.action_space.n)))
        t += 1
        if te or tr:
            env.reset(seed=int(rng.integers(1_000_000)))
    env.close()
    return out


def sonraki(ad, s, a, tohum):
    env = gym.make(ad)
    env.reset(seed=tohum)
    durum_ata(env, s)
    obs, *_ = env.unwrapped.step(int(a))
    env.close()
    return np.atleast_1d(np.asarray(obs, dtype=float))


def kos(ad):
    n_a = gym.make(ad).action_space.n
    S = durumlar(ad)
    # S1
    fark = karsi = 0
    for i, s in enumerate(S):
        ss = [sonraki(ad, s, a, 10_000 + i) for a in range(n_a)]
        for a in range(1, n_a):
            karsi += 1
            fark += int(not np.array_equal(ss[0], ss[a]))
    # S2
    boyut = len(sonraki(ad, S[0], 0, 1))
    esik = ALFA / (len(S) * boyut)
    red_ozgun, red_genis, p_min = 0, 0, 1.0
    for i, s in enumerate(S):
        A = [np.array([sonraki(ad, s, a, (i + 1) * 1_000_003 + a * 7919 + m) for m in range(M)])
             for a in range(n_a)]
        for d in range(boyut):
            kolon = [x[:, d] for x in A]
            if all(np.ptp(k) == 0 for k in kolon):
                if len({float(k[0]) for k in kolon}) > 1:
                    red_genis += 1
                continue
            try:
                _, p = stats.kruskal(*kolon)
            except ValueError:
                continue
            p_min = min(p_min, float(p))
            if p < esik:
                red_ozgun += 1; red_genis += 1
    saptandi = (fark > 0) or (red_genis > 0)
    r = {'ortam': ad, 'n_eylem': int(n_a), 'gozlem_boyutu': int(boyut), 'K': K, 'M': M,
         's1_karsilastirma': karsi, 's1_farkli': fark,
         's2_bonferroni_esik': esik, 's2_en_kucuk_p': p_min,
         's2_ozgun_reddedilen': red_ozgun, 's2_genis_reddedilen': red_genis,
         'bagimlilik_saptandi': bool(saptandi)}
    print(ad, r['s1_farkli'], '/', karsi, 'S2 ozgun', red_ozgun, 'genis', red_genis,
          'p_min %.3g' % p_min, '->', saptandi)
    return r


if __name__ == '__main__':
    sonuc = {'on_kayit_sha256': ozet(HERE / 'E13_ON_KAYIT_11102026.md'),
             'kosucu_sha256': ozet(__file__),
             'test_kodu_sha256': ozet('/home/claude/kk/gecis_bagimliligi_testi.py'),
             'gymnasium': gym.__version__, 'ortamlar': [kos(o) for o in ORTAMLAR]}
    sonuc['hepsinde_saptandi'] = all(o['bagimlilik_saptandi'] for o in sonuc['ortamlar'])
    (HERE / 'e13_sonuc.json').write_text(json.dumps(sonuc, indent=1))
    print('hepsinde saptandi', sonuc['hepsinde_saptandi'])
