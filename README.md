# KL-C – P3 „Obraz, ocena, pobudzenie”: jakość sygnału i estymacja stanu

Zespół: DK – Diana Kalinina, OS – Oleksandr Shamak.
**Pełna instrukcja odtworzenia: [`BUILD_BOOK.md`](BUILD_BOOK.md)** – rozdz. 5 (wzrok) i 7 (jakość, linia bazowa, stany, histereza, ewaluacja).
**Sekcja analityczna:** [`docs/KL-C_ANALIZA.md`](docs/KL-C_ANALIZA.md).

## Co oddajemy w KL-C

| Ścieżka | Co to jest |
|---|---|
| `experiment/P3_KL_C-2.psyexp` | eksperyment: instrukcja → baseline 30 s → 4 obrazy A–D → pytanie → monitoring 340 s |
| `experiment/state_estimation.py` | filtr artefaktów, wskaźniki jakości (wzrok 2 s, EDA 5 s), linia bazowa, stany, histereza 6 s |
| `experiment/lsl_runtime.py` | konsola eksperymentatora, plik statusu co 1 s, znaczniki `state:*` |
| `lsl/sim_to_lsl.py` | most symulator → LSL `LBK_Sim` (12 kanałów) |
| `sample_data/P3_KL-C_clean_fixed_1.xdf`, `P3_KL-C_noisy_360s.xdf` | nagrania clean i noisy (> 360 s) |
| `sample_data/KL-C_STATUS_*.csv` | pliki statusu z obu sesji |
| `sample_data/ground_truth_*.jsonl` | etykiety `scenario` symulatora – tylko do oceny |
| `analysis/evaluate_klc.py`, `analysis/compare_both.py` | ewaluacja |
| `reports/tabela_klc.csv`, `reports/wyniki_*.md` | tabela wyników |
| `tests/test_klc.py` | testy progów, filtra, linii bazowej i histerezy |

## Wyniki (pierwsze 360 s)

| | clean | noisy |
|---|---:|---:|
| Zgodność ze `scenario` | 39,57 % | 18,40 % |
| Zmiany stanu | 7 | 0 |
| Wzrok poprawny / zaszumiony / utracony | 96,65 / 2,79 / 0,56 % | 98,04 / 1,96 / 0,00 % |
| EDA poprawny / zaszumiony / utracony | 100 / 0 / 0 % | 23,46 / 75,42 / 1,12 % |

Ograniczenia i ich przyczyny (linia bazowa poza fazą spoczynku, opóźnienie, sesja noisy): Build Book 7.10 i sekcja analityczna.

## Szybkie sprawdzenie

```bash
python3 tests/test_klc.py
python3 analysis/evaluate_klc.py --label clean --xdf sample_data/P3_KL-C_clean_fixed_1.xdf --status sample_data/KL-C_STATUS_TEST-06_20261108_213754.csv --truth sample_data/ground_truth_clean_extended.jsonl
python3 analysis/evaluate_klc.py --label noisy --xdf sample_data/P3_KL-C_noisy_360s.xdf --status sample_data/KL-C_STATUS_TEST-01_20261108_215324.csv --truth sample_data/ground_truth_noisy.jsonl
python3 analysis/compare_both.py
```

Windows: `py -3` zamiast `python3`. Wymaga `pyxdf` (`overlay/requirements.txt`).
