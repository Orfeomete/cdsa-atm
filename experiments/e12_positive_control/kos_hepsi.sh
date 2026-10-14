#!/bin/bash
cd /home/claude/kk/e12
for var in D1 D2; do for kol in merkezi fedavg; do for t in 42 43 44 45 46; do
  python3 -B e12_kos.py ppo $var $kol $t >> sonuclar/ppo_gunluk.txt 2>&1
done; done; done
echo BITTI >> sonuclar/ppo_gunluk.txt
