"""ATM-D -- eylemin sonraki durumu degistirdigi ATM varyanti (E12 olumlu kontrol).

Yayimlanmis ATMFlowEnv (cdsa-atm/src/rl_environment/env.py) ile AYNI gozlem
ureteci, AYNI etiket kurali ve AYNI eylem odulu kullanilir. Tek degisiklik
gecistedir. Gozleme 13. kanal olarak trafik baskisi rho eklenir ve rho
eyleme bagli olarak gelisir.

  rho' = clip(rho + SURUKLENME - ETKI[a] + N(0, GURULTU), 0, 1)

Sonraki durumun sinif karisimi rho'ya baglidir. Yuksek baski kritik olay
(sinif 3) ve yogunluk (sinif 2) payini arttirir, standart akis (sinif 0)
payini azaltir. Siber pay (sinif 4) istemci siber oranina bagli kalir.

Iki varyant vardir.
  D1  odul yayimlanmis ortamla ayni (yalniz gecis eyleme bagli)
  D2  D1'e ek olarak kritik olay durumunda bulunmanin eylemden bagimsiz
      bir emniyet maliyeti vardir (KRITIK_DURUM_MALIYETI)
"""
from __future__ import annotations
import numpy as np

ACTIONS = ("standard_flow", "speed_restriction", "route_change",
           "holding_pattern", "sector_wide_alert")

SURUKLENME = 0.01
ETKI = np.array([0.00, 0.08, 0.03, -0.04, 0.00])   # bekleme yigilma yaratir
GURULTU = 0.02
TABAN = np.array([0.40, 0.22, 0.14, 0.24])
AGIRLIK_EGIM = np.array([-1.0, 0.0, 1.0, 2.0])   # w_c(rho) = 1 + egim_c * rho
KRITIK_DURUM_MALIYETI = 8.0


class ATMDinamikEnv:
    N_ACTIONS = 5
    STATE_DIM = 13

    def __init__(self, seed: int = 42, max_steps: int = 200,
                 cyber_rate: float = 0.12, varyant: str = "D1"):
        assert varyant in ("D1", "D2")
        self.rng = np.random.default_rng(seed)
        self.max_steps = int(max_steps)
        self.cyber_rate = float(cyber_rate)
        self.varyant = varyant
        self._t = 0
        self._state = None
        self._rho = 0.3

    # yayimlanmis ortamdaki kuralin birebir kopyasi (12 kanal uzerinde)
    @staticmethod
    def _appropriate_action(s: np.ndarray) -> int:
        density = s[0:3].mean()
        occupancy = s[3:6].mean()
        ats_ops, ats_cyber, severity = s[6], s[7], s[8]
        coord_conflict = s[9:12].mean()
        if ats_cyber > 0.7 and severity > 0.6:
            return 4
        if severity > 0.7 and ats_ops > 0.5:
            return 3
        if density > 0.75 and occupancy > 0.6:
            return 2 if coord_conflict > 0.5 else 1
        if occupancy > 0.7:
            return 1
        return 0

    def _sinif_olasiliklari(self, rho: float) -> np.ndarray:
        p4 = min(max(self.cyber_rate, 0.02), 0.5)
        w = TABAN * np.clip(1.0 + AGIRLIK_EGIM * rho, 0.0, None)
        w = w / w.sum() * (1.0 - p4)
        return np.append(w, p4)

    def _sample_obs(self, rho: float) -> np.ndarray:
        probs = self._sinif_olasiliklari(rho)
        target = int(self.rng.choice(5, p=probs / probs.sum()))
        for _ in range(200):
            s = self.rng.uniform(0, 1, 12)
            if target == 4:
                s[7] = self.rng.uniform(0.72, 1.0); s[8] = self.rng.uniform(0.62, 1.0)
            elif target == 3:
                s[7] = self.rng.uniform(0.0, 0.65); s[8] = self.rng.uniform(0.72, 1.0)
                s[6] = self.rng.uniform(0.52, 1.0)
            elif target == 2:
                s[0:3] = self.rng.uniform(0.76, 1.0, 3); s[3:6] = self.rng.uniform(0.62, 1.0, 3)
                s[9:12] = self.rng.uniform(0.52, 1.0, 3); s[7] *= 0.5; s[8] *= 0.5
            elif target == 1:
                s[3:6] = self.rng.uniform(0.72, 1.0, 3); s[0:3] = self.rng.uniform(0.0, 0.74, 3)
                s[7] *= 0.4; s[8] *= 0.5
            else:
                s[3:6] *= 0.65; s[0:3] *= 0.7; s[7] *= 0.3; s[8] *= 0.5
            if self._appropriate_action(s) == target:
                return s
        return s

    def _gozlem(self):
        return np.append(self._state, self._rho)

    def reset(self, seed: int | None = None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self._t = 0
        self._rho = float(self.rng.uniform(0.2, 0.4))
        self._state = self._sample_obs(self._rho)
        return self._gozlem(), {}

    def durum_ata(self, s13):
        s13 = np.asarray(s13, dtype=float)
        self._state = s13[:12].copy()
        self._rho = float(s13[12])

    def step(self, action: int):
        if self._state is None:
            raise RuntimeError("call reset() first")
        action = int(action)
        a_true = self._appropriate_action(self._state)
        severity = float(self._state[8])
        if action == a_true:
            reward = 10.0
        elif action == 4 and a_true != 4:
            reward = -5.0
        elif a_true >= 3 and action < a_true:
            reward = -20.0 * (severity + 1.0)
        else:
            reward = -1.0
        if self.varyant == "D2" and a_true == 3:
            reward -= KRITIK_DURUM_MALIYETI
        self._t += 1
        truncated = self._t >= self.max_steps
        self._rho = float(np.clip(self._rho + SURUKLENME - ETKI[action]
                                  + self.rng.normal(0.0, GURULTU), 0.0, 1.0))
        self._state = self._sample_obs(self._rho)
        info = {"appropriate_action": a_true, "appropriate_label": ACTIONS[a_true],
                "rho": self._rho}
        return self._gozlem(), reward, False, truncated, info
