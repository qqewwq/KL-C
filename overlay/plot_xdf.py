#!/usr/bin/env python3
"""Wykres EDA i znaczników z PRAWDZIWEGO pliku XDF z LabRecorder."""
import argparse
from pathlib import Path
import math


def plot_xdf(path, out):
    import matplotlib.pyplot as plt
    import pyxdf
    streams, _ = pyxdf.load_xdf(str(path))
    def by_name(name):
        return next((s for s in streams if s['info']['name'][0] == name), None)
    eda, markers = by_name('LBK_Sim'), by_name('LBK_Markers')
    if eda is None or markers is None:
        raise RuntimeError('W XDF muszą być LBK_Sim i LBK_Markers. Sprawdź LabRecorder.')
    # Odszukaj kanał EDA po etykiecie, nie tylko po pozycji
    names = []
    try:
        names = [d['label'][0] for d in eda['info']['desc'][0]['channels'][0]['channel']]
    except (KeyError, IndexError, TypeError):
        pass
    idx = names.index('eda_us') if 'eda_us' in names else 1
    x = eda['time_stamps']
    ys = eda['time_series']
    y = [float(row[idx]) for row in ys]
    t0 = float(x[0])
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot([(float(t)-t0) for t in x], y, lw=1.3, label='EDA (uS)')
    count = 0
    for tick, row in zip(markers['time_stamps'], markers['time_series']):
        value = row[0] if hasattr(row, '__getitem__') else row
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        value = str(value)
        # Wykres czytelniejszy przy etykietowaniu głównych znaczników
        if value.startswith(('stim:onset', 'exp:start', 'exp:end')):
            pos = float(tick)-t0
            ax.axvline(pos, linestyle='--', alpha=0.5)
            if count < 20:
                ax.text(pos, ax.get_ylim()[1], value.split('|')[0], rotation=90,
                        fontsize=7, va='top', ha='right')
            count += 1
    ax.set(xlabel='Czas wspólny LSL od początku zapisu (s)', ylabel='EDA (uS)',
           title='P3: sygnał EDA i znaczniki z XDF')
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(out, dpi=170)
    plt.close(fig)
    print(f'Zapisano {out}; strumienie: {[s["info"]["name"][0] for s in streams]}')
    print(f'Probek EDA: {len(x)}, markery widoczne: {len(markers["time_stamps"])}')
    if float(x[-1])-float(x[0]) < 115:
        print('UWAGA: sygnal EDA ma mniej niz okolo 2 min; sprawdz czas nagrania')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('xdf', type=Path)
    parser.add_argument('--out', type=Path, default=Path('docs/img/eda_markery.png'))
    a = parser.parse_args()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    plot_xdf(a.xdf, a.out)
