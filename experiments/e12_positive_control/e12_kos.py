"""E12 olumlu kontrol kosucusu. On kayit E12_ON_KAYIT_11102026.md.

Kullanim  python3 e12_kos.py on_kosul | ppo <varyant> <kol> <tohum> | karsilastirici | ozet
"""
from __future__ import annotations
import hashlib, json, sys, time
from pathlib import Path
import numpy as np

E12 = Path(__file__).resolve().parent
ROOT = Path('/home/claude/kk/CDSA-ATM/12_GitHub_Repo/cdsa-atm')
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'experiments')); sys.path.insert(0, str(E12))
from src.rl_agents.ppo_actor_critic import PPOActorCritic
from src.federated.fedavg import FedAvgAggregator
import faz_a_staged as fs
from atm_dinamik import ATMDinamikEnv, ACTIONS

SONUC = E12 / 'sonuclar'; SONUC.mkdir(exist_ok=True)
TOHUMLAR = [42, 43, 44, 45, 46]
TUR = 100
SIBER_ORANLARI = (0.05, 0.12, 0.25)
EVAL_REPS, EVAL_STEPS = 3, 600
N_EGITIM = 3000
N_A, DIM = 5, 13
ONLEYICI_ESIK = 0.2


def ozet(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def yeni_ajan(tohum):
    return PPOActorCritic(fused_dim=DIM, n_actions=N_A, hidden=64, lr=0.05,
                          reward_scale=0.05, seed=tohum)


def istemci_ortamlari(var, tohum):
    return [ATMDinamikEnv(seed=tohum + i, max_steps=10_000, cyber_rate=r, varyant=var)
            for i, r in enumerate(SIBER_ORANLARI)]


# ---------------- kapali dongu degerlendirme ----------------
def degerlendir(var, politika, rastgele_tohum=0):
    rng = np.random.default_rng(rastgele_tohum)
    yt, yp, R, krit, rho = [], [], [], [], []
    for rep in range(EVAL_REPS):
        env = ATMDinamikEnv(seed=942 + rep, max_steps=10_000, cyber_rate=0.12, varyant=var)
        s, _ = env.reset(seed=2026 + rep)
        for _ in range(EVAL_STEPS):
            a = int(politika(env, s, rng))
            s2, r, te, tr, info = env.step(a)
            yt.append(int(info['appropriate_action'])); yp.append(a); R.append(float(r))
            krit.append(int(info['appropriate_action'] == 3)); rho.append(float(info['rho']))
            s = s2
    yt, yp = np.array(yt), np.array(yp)
    cm = np.zeros((N_A, N_A), dtype=int)
    for t, p in zip(yt, yp):
        cm[t, p] += 1
    destek = cm.sum(axis=1) > 0
    f1 = []
    for c in range(N_A):
        tp = cm[c, c]; fp = cm[:, c].sum() - tp; fn = cm[c, :].sum() - tp
        pr = tp / (tp + fp) if tp + fp else 0.0; rc = tp / (tp + fn) if tp + fn else 0.0
        f1.append(2 * pr * rc / (pr + rc) if pr + rc else 0.0)
    f1 = np.array(f1)
    return {'ort_odul': round(float(np.mean(R)), 4),
            'makro_f1_destekli': round(float(f1[destek].mean()), 4),
            'makro_f1_bes_sinif': round(float(f1.mean()), 4),
            'dogruluk': round(float((yt == yp).mean()), 4),
            'kritik_durum_payi': round(float(np.mean(krit)), 4),
            'ort_baski': round(float(np.mean(rho)), 4),
            'kullanilan_eylem': sorted(int(x) for x in np.unique(yp)),
            'karisiklik_matrisi': cm.tolist()}


def p_etiket(env, s, rng):
    return env._appropriate_action(s[:12])


def p_onleyici(env, s, rng):
    a = env._appropriate_action(s[:12])
    return 1 if (a == 0 and s[12] > ONLEYICI_ESIK) else a


def p_rastgele(env, s, rng):
    return rng.integers(N_A)


def p_ajan(ajan):
    return lambda env, s, rng: ajan.act(s, deterministic=True)[0]


# ---------------- on kosul testi (E12.0a) ----------------
def on_kosul():
    sys.path.insert(0, '/home/claude/kk')
    import gecis_bagimliligi_testi as gt

    class Sarmal(ATMDinamikEnv):
        pass
    sonuc = {'test_kodu_sha256': ozet('/home/claude/kk/gecis_bagimliligi_testi.py'), 'ortamlar': []}
    print('denetimler')
    neg = gt.kos('negatif denetim', lambda seed=0: gt.NegatifDenetim(seed), 4, 6)
    poz = gt.kos('pozitif denetim 0,10', lambda seed=0: gt.PozitifDenetim(seed, 0.10), 4, 6)
    assert neg['s1']['bit_ayni'] and neg['s2']['bagimsiz_kalir']
    assert (not poz['s1']['bit_ayni']) and (not poz['s2']['bagimsiz_kalir'])
    sonuc['denetimler'] = [neg, poz]
    gt.UP = Path('/home/claude/kk')
    A, Asinif = gt.atm_kur()
    sonuc['ortamlar'].append(gt.kos('yayimlanmis ATM', lambda seed=42: A(seed=seed), 5, 12))
    for var in ('D1', 'D2'):
        sonuc['ortamlar'].append(gt.kos('ATM-' + var,
                                        lambda seed=42, v=var: Sarmal(seed=seed, varyant=v), N_A, DIM))
    (SONUC / 'e12_on_kosul.json').write_text(json.dumps(sonuc, indent=1, ensure_ascii=False))


# ---------------- PPO kollari ----------------
def ppo(var, kol, tohum):
    t0 = time.time()
    envs = istemci_ortamlari(var, tohum)
    if kol == 'merkezi':
        ag = yeni_ajan(tohum)
        for _ in range(TUR):
            for e in envs:
                fs.train_local(e, ag)
        son = ag
    else:
        agg = FedAvgAggregator(seed=tohum)
        cl = [yeni_ajan(tohum + i) for i in range(len(envs))]
        g = cl[0].params()
        for _ in range(TUR):
            for c in cl:
                c.set_params(g)
            for e, c in zip(envs, cl):
                fs.train_local(e, c)
            g = agg.aggregate([c.params() for c in cl])
        son = yeni_ajan(0); son.set_params(g)
    m = degerlendir(var, p_ajan(son))
    m.update({'varyant': var, 'kol': 'ppo_' + kol, 'tohum': tohum, 'tur': TUR,
              'sure_sn': round(time.time() - t0, 1)})
    (SONUC / f'e12_{var}_ppo_{kol}_t{tohum}.json').write_text(json.dumps(m, indent=1))
    (SONUC / f'params_e12_{var}_{kol}_t{tohum}.json').write_text(json.dumps(fs._p2j(son.params())))
    print(var, kol, tohum, m['ort_odul'], m['makro_f1_destekli'], m['kullanilan_eylem'], m['sure_sn'])


# ---------------- siniflandirici karsilastiricilar ----------------
def egitim_kumesi(var, tohum):
    env = ATMDinamikEnv(seed=tohum, max_steps=10_000, varyant=var)
    s, _ = env.reset(seed=tohum)
    rng = np.random.default_rng(tohum + 5000)
    X, y = [], []
    for _ in range(N_EGITIM):
        X.append(s.copy()); y.append(env._appropriate_action(s[:12]))
        s, *_ = env.step(int(rng.integers(N_A)))
    return np.array(X), np.array(y)


def maliyet_matrisi(var, tohum, n=600):
    env = ATMDinamikEnv(seed=tohum, max_steps=10_000, varyant=var)
    s, _ = env.reset(seed=tohum)
    rng = np.random.default_rng(tohum + 6000)
    top = np.zeros((N_A, N_A)); say = np.zeros((N_A, N_A))
    for _ in range(n):
        c = env._appropriate_action(s[:12])
        for a in range(N_A):
            env.durum_ata(s); env._t = 0
            _, r, *_ = env.step(a)
            top[a, c] += r; say[a, c] += 1
        env.durum_ata(s)
        s, *_ = env.step(int(rng.integers(N_A)))
    R = np.where(say > 0, top / np.maximum(say, 1), np.nan)
    K = -R
    if np.isnan(K).any():
        K = np.where(np.isnan(K), np.nanmax(K), K)
    return K


def karsilastirici():
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    sys.path.insert(0, str(ROOT / 'experiments'))
    import faz_e2_karsilastiricilar as e2
    cikti = {}
    for var in ('D1', 'D2'):
        for tohum in TOHUMLAR:
            X, y = egitim_kumesi(var, tohum)
            K = maliyet_matrisi(var, tohum)
            w = e2.sinif_agirliklari(K)
            lr = LogisticRegression(max_iter=2000).fit(X, y, sample_weight=w[y])
            agac = DecisionTreeClassifier(max_depth=4, random_state=0).fit(X, y, sample_weight=w[y])
            def p_lr(env, s, rng, lr=lr, K=K):
                P = np.zeros(N_A); P[lr.classes_] = lr.predict_proba(s.reshape(1, -1))[0]
                return int(np.argmin(K @ P))
            def p_agac(env, s, rng, agac=agac):
                return int(agac.predict(s.reshape(1, -1))[0])
            cog = int(np.bincount(y, minlength=N_A).argmax())
            for ad, pol in (('maliyet_lojistik', p_lr), ('karar_agaci_d4', p_agac),
                            ('sabit_cogunluk', lambda env, s, rng, c=cog: c)):
                m = degerlendir(var, pol)
                m.update({'varyant': var, 'kol': ad, 'tohum': tohum})
                if ad == 'maliyet_lojistik':
                    m['maliyet_matrisi'] = [[round(float(v), 3) for v in r] for r in K]
                cikti[f'{var}_{ad}_t{tohum}'] = m
                print(var, ad, tohum, m['ort_odul'], m['makro_f1_destekli'])
        for ad, pol in (('etiket_kurali', p_etiket), ('rastgele', p_rastgele), ('onleyici_sezgisel', p_onleyici)):
            m = degerlendir(var, pol)
            m.update({'varyant': var, 'kol': ad})
            cikti[f'{var}_{ad}'] = m
            print(var, ad, m['ort_odul'], m['makro_f1_destekli'], m['kritik_durum_payi'], m['ort_baski'])
    (SONUC / 'e12_karsilastiricilar.json').write_text(json.dumps(cikti, indent=1))


if __name__ == '__main__':
    k = sys.argv[1]
    if k == 'on_kosul':
        on_kosul()
    elif k == 'ppo':
        ppo(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif k == 'karsilastirici':
        karsilastirici()
