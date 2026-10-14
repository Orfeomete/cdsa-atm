import json, hashlib, statistics as st
from pathlib import Path
H = Path(__file__).parent; S = H / 'sonuclar'
def oz(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
K = json.loads((S / 'e12_karsilastiricilar.json').read_text())
on = json.loads((S / 'e12_on_kosul.json').read_text())
out = {'on_kayit_sha256': oz(H / 'E12_ON_KAYIT_11102026.md'), 'ortam_sha256': oz(H / 'atm_dinamik.py'),
       'kosucu_sha256': oz(H / 'e12_kos.py'), 'test_kodu_sha256': on['test_kodu_sha256'],
       'on_kosul': {o['ortam']: {'s1_farkli': o['s1']['farkli'], 's1_karsilastirma': o['s1']['karsilastirma'],
                                 's2_bagimsiz_kalir': o['s2']['bagimsiz_kalir'], 's2_en_kucuk_p': o['s2']['en_kucuk_p']}
                    for o in on['ortamlar']}, 'varyantlar': {}}
T = [42, 43, 44, 45, 46]
def ozetle(vals):
    return {'ort': round(st.mean(vals), 4), 'ss': round(st.stdev(vals), 4), 'tohumlar': vals}
for var in ('D1', 'D2'):
    v = {}
    for kol in ('merkezi', 'fedavg'):
        rs = [json.loads((S / f'e12_{var}_ppo_{kol}_t{t}.json').read_text()) for t in T]
        v['ppo_' + kol] = {'odul': ozetle([r['ort_odul'] for r in rs]), 'makro_f1': ozetle([r['makro_f1_destekli'] for r in rs]),
                           'kritik_durum_payi': ozetle([r['kritik_durum_payi'] for r in rs]),
                           'tek_eylem_kosu': sum(len(r['kullanilan_eylem']) == 1 for r in rs),
                           'kullanilan_eylemler': [r['kullanilan_eylem'] for r in rs]}
    for kol in ('maliyet_lojistik', 'karar_agaci_d4', 'sabit_cogunluk'):
        rs = [K[f'{var}_{kol}_t{t}'] for t in T]
        v[kol] = {'odul': ozetle([r['ort_odul'] for r in rs]), 'makro_f1': ozetle([r['makro_f1_destekli'] for r in rs]),
                  'kritik_durum_payi': ozetle([r['kritik_durum_payi'] for r in rs])}
    for kol in ('etiket_kurali', 'rastgele', 'onleyici_sezgisel'):
        r = K[f'{var}_{kol}']
        v[kol] = {'odul': r['ort_odul'], 'makro_f1': r['makro_f1_destekli'], 'kritik_durum_payi': r['kritik_durum_payi'], 'ort_baski': r['ort_baski']}
    eniyi = max(('ppo_merkezi', 'ppo_fedavg'), key=lambda k: v[k]['odul']['ort'])
    ref_o, ref_f = v['maliyet_lojistik']['odul']['ort'], v['maliyet_lojistik']['makro_f1']['ort']
    fo = v[eniyi]['odul']['ort'] - ref_o; ff = v[eniyi]['makro_f1']['ort'] - ref_f
    v['kurallar'] = {
        'en_iyi_ppo_kolu': eniyi,
        'E12_0b_tavan_payi': (None if var == 'D1' else round((v['onleyici_sezgisel']['odul'] - v['etiket_kurali']['odul']) / abs(v['etiket_kurali']['odul']), 4)),
        'E12_0b_saglandi': (None if var == 'D1' else (v['onleyici_sezgisel']['odul'] - v['etiket_kurali']['odul']) >= 0.05 * abs(v['etiket_kurali']['odul'])),
        'E12_1_fark_makro_f1': round(ff, 4),
        'E12_1_hukum': 'PPO maliyet-duyarli siniflandiriciyi 0,05 gecti' if ff > 0.05 else 'DRL yontem secimi bu gorevde gerekcelendirilemedi',
        'E12_2_fark_odul': round(fo, 4), 'E12_2_esik': round(0.05 * abs(ref_o), 4),
        'E12_2_hukum': 'DRL yontem secimi bu varyantta ve bu butcede desteklendi' if fo > 0.05 * abs(ref_o) else 'DRL yontem secimi bu varyantta gerekcelendirilemedi'}
    out['varyantlar'][var] = v
    print(var, json.dumps(v['kurallar'], ensure_ascii=False))
    for k in ('ppo_merkezi', 'ppo_fedavg', 'maliyet_lojistik', 'karar_agaci_d4', 'sabit_cogunluk'):
        print('  ', k, v[k]['odul']['ort'], v[k]['odul']['ss'], 'F1', v[k]['makro_f1']['ort'], 'krit', v[k]['kritik_durum_payi']['ort'], v[k].get('tek_eylem_kosu', ''))
    for k in ('etiket_kurali', 'rastgele', 'onleyici_sezgisel'):
        print('  ', k, v[k])
(S / 'e12_sonuc.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
