#!/usr/bin/env python3
"""Kontrola zawartości bez podmieniania ani generowania danych pomiarowych."""
from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parent
FILES=[
 'experiment/P3_KL_C-2.psyexp',
 'experiment/lsl_runtime.py',
 'experiment/state_estimation.py',
 'experiment/conditions/L1_LBK_4obrazy_test.csv',
 'experiment/stimuli/Bodziec A.PNG',
 'experiment/stimuli/Bodziec B.PNG',
 'experiment/stimuli/Bodziec C.PNG',
 'experiment/stimuli/Bodziec D.PNG',
 'lsl/sim_to_lsl.py',
 'simulator/symulator_biosygnalow.py',
 'sample_data/P3_KL-C_clean_fixed_1.xdf',
 'sample_data/P3_KL-C_noisy_360s.xdf',
 'sample_data/KL-C_STATUS_TEST-06_20261108_213754.csv',
 'sample_data/KL-C_STATUS_TEST-01_20261108_215324.csv',
 'sample_data/ground_truth_clean_extended.jsonl',
 'sample_data/ground_truth_noisy.jsonl',
 'reports/wyniki_clean.csv',
 'reports/wyniki_noisy.csv',
 'reports/wyniki_clean.md',
 'reports/wyniki_noisy.md',
 'reports/tabela_klc.csv',
 'BUILD_BOOK.md',
 'docs/img/7-1-flow-klc.png',
 'docs/img/7-2-labrecorder-konfiguracja.png',
 'docs/img/7-3-jakosc-gaze-eda.png',
 'docs/img/7-4-rozpoznany-stan.png',
 'docs/img/7-5-wykres-jakosci.png',
]
missing=[]
for rel in FILES:
 p=ROOT/rel
 if p.is_file() and p.stat().st_size>0:
  print('OK  ',rel)
 else:
  print('BRAK',rel); missing.append(rel)
try:
 with (ROOT/'reports/tabela_klc.csv').open(newline='',encoding='utf-8-sig') as f:
  rows={r['nagranie']:r for r in csv.DictReader(f)}
 if {'clean','noisy'} <= set(rows):
  print('OK   raport clean/noisy, wartości:',round(float(rows['clean']['zgodnosc_pct']),2),round(float(rows['noisy']['zgodnosc_pct']),2))
 else: raise ValueError('brakuje clean/noisy')
except (OSError,KeyError,ValueError) as exc:
 print('BŁĄD RAPORTU:',exc)
 missing.append('reports/tabela_klc.csv')
if missing:
 print('\nDo uzupełnienia:',len(missing),'plik(ów).')
 raise SystemExit(1)
print('\nGOTOWE TECHNICZNIE. Przed wysłaniem: wpisz autorów i prywatne repozytorium w BUILD_BOOK.md; zrzuty KL-C są dołączone; wpisz autorów i repozytorium.')
