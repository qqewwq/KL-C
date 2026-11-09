#!/usr/bin/env python3
"""Ocena z prawdą symulatora po seq; scenario NIE jest używane w eksperymencie."""
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

# Mapowanie symulacyjnych etykiet na cztery etykiety estymatora P3.
TARGET = {'spokoj': 'spoczynkowy',
          'stres': 'pobudzenie_podwyzszone',
          'skupienie': 'zaangazowanie_wzrokowe',
          'zmeczenie': 'nieznany'}
LABELS = ['poprawny', 'zaszumiony', 'utracony']


def load_xdf_range(path, seconds=360):
    import pyxdf
    streams, _ = pyxdf.load_xdf(str(path))
    found = {s['info']['name'][0]: s for s in streams}
    if 'LBK_Sim' not in found or 'LBK_Markers' not in found:
        raise RuntimeError('XDF musi zawierać LBK_Sim i LBK_Markers')
    sim = found['LBK_Sim']
    timestamps = sim['time_stamps']
    if len(timestamps) < 2:
        raise RuntimeError('Za mało próbek w LBK_Sim')
    first = float(timestamps[0])
    last = float(timestamps[-1])
    length = last - first
    if length < seconds - 1.0:
        raise RuntimeError(f'Nagranie ma tylko {length:.1f} s, wymagane ok. {seconds} s')
    if len(sim['time_series'][0]) < 12:
        raise RuntimeError('Zły most LSL: brak kanałów seq i t (nowa wersja KL-C)')
    marker_stream = found['LBK_Markers']
    state_markers = [str(x[0]) for x in marker_stream['time_series'] if str(x[0]).startswith('state:')]
    return first, min(first + seconds, last), length, state_markers


def read_truth(path):
    labels = {}
    for line in Path(path).read_text(encoding='utf8').splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        labels[int(obj['seq'])] = TARGET[obj['scenario']]
    return labels


def read_status(path, begin, stop):
    with open(path, newline='', encoding='utf-8') as fp:
        rows = list(csv.DictReader(fp))
    if not rows:
        raise ValueError('Pusty plik statusu')
    out = []
    for r in rows:
        try:
            if begin <= float(r['t_lsl']) <= stop:
                out.append(r)
        except (ValueError, KeyError):
            continue
    if not out:
        raise ValueError('Plik statusu nie zawiera tego zakresu czasu LSL: wybierz status z tej sesji')
    return out


def compare(rows, truth, markers):
    after = [r for r in rows if r['baseline_eda'] not in ('', 'nan', 'NaN', 'None')]
    pairs = []
    for r in after:
        try:
            seq = int(r['seq'])
        except (ValueError, TypeError):
            continue
        if seq in truth:
            pairs.append((r, truth[seq]))
    pct = (100 * sum(r['state'] == expected for r, expected in pairs)/len(pairs)) if pairs else math.nan
    reliable = [(r, e) for r, e in pairs if r['gaze_quality'] == 'poprawny' and r['eda_quality'] == 'poprawny']
    good_pct = (100 * sum(r['state'] == e for r, e in reliable)/len(reliable)) if reliable else math.nan
    # Procent czasu przy próbkowaniu statusu ~1 Hz.
    quality = {}
    for source in ('gaze_quality', 'eda_quality'):
        counts = Counter(r[source] for r in rows)
        quality[source] = {name: round(100*counts[name]/len(rows), 2) for name in LABELS}
    switches = sum(a['state'] != b['state'] for a,b in zip(rows,rows[1:]))
    return {'zgodnosc_pct': pct, 'zgodnosc_dobra_jakosc_pct': good_pct,
            'zmiany_stanu': switches, 'markery_state_n': len(markers),
            'odczyty_statusu': len(rows), 'ocenione_probki_statusu': len(pairs),
            'gaze': quality['gaze_quality'], 'eda': quality['eda_quality']}


def write_reports(label, results, output):
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / f'wyniki_{label}.csv'
    data = {'nagranie':label, 'zgodnosc_pct':results['zgodnosc_pct'],
            'zgodnosc_dobra_jakosc_pct':results['zgodnosc_dobra_jakosc_pct'],
            'zmiany_stanu':results['zmiany_stanu'],
            'markery_state_n':results['markery_state_n'],
            'status_n':results['odczyty_statusu'], 'porownane_n':results['ocenione_probki_statusu']}
    for which in ('gaze', 'eda'):
        for state in LABELS:
            data[f'{which}_{state}_pct'] = results[which][state]
    with open(csv_path, 'w', newline='', encoding='utf8') as fp:
        writer = csv.DictWriter(fp, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
    md = output / f'wyniki_{label}.md'
    def fmt(value):
        return 'brak' if not math.isfinite(float(value)) else f'{value:.1f}%'
    md.write_text(
        f'# Wyniki KL-C: {label}\n\n'
        f'- Zgodność ogólna po kalibracji: **{fmt(results["zgodnosc_pct"])}**\n'
        f'- Zgodność przy obu sygnałach poprawnych: **{fmt(results["zgodnosc_dobra_jakosc_pct"])}**\n'
        f'- Zmiany stanu: **{results["zmiany_stanu"]}**; markery state w XDF: **{results["markery_state_n"]}**\n'
        f'- Punkty statusu: **{results["odczyty_statusu"]}**, sparowane przez seq: **{results["ocenione_probki_statusu"]}**\n\n'
        '| Jakość | poprawny | zaszumiony | utracony |\n|---|---:|---:|---:|\n'
        + ''.join(f'| {signal} | '+ ' | '.join(f'{results[signal][q]:.1f}%' for q in LABELS) + ' |\n' for signal in ('gaze', 'eda'))
        + '\n**Uwaga:** symulatorowe scenario jest etykietą testową, a nie diagnozą. Stan `nieznany` obejmuje także fazę `zmeczenie`, której KL-C P3 osobno nie wykrywa.\n', encoding='utf8')
    print('Zapisano:', csv_path, md)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--xdf', required=True)
    p.add_argument('--status', required=True)
    p.add_argument('--truth', required=True)
    p.add_argument('--label', choices=['clean','noisy'], required=True)
    p.add_argument('--outdir', default='reports')
    p.add_argument('--seconds', type=float, default=360)
    a = p.parse_args()
    start, stop, dur, markers = load_xdf_range(a.xdf, a.seconds)
    print(f'XDF: {dur:.1f} s, wybrany zakres {stop-start:.1f} s, markery state: {len(markers)}')
    status = read_status(a.status, start, stop)
    truth = read_truth(a.truth)
    result = compare(status, truth, markers)
    write_reports(a.label, result, Path(a.outdir))

if __name__ == '__main__':
    main()
