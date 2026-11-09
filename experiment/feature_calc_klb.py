"""Zachowany obliczacz cech KL-B, niezależny od bibliotek zewnętrznych."""
import math
from statistics import mean, median


def calculate_features(records):
    good, bad = [], 0
    for _, sample in records:
        try:
            if float(sample[4]) != 0.0:
                bad += 1
                continue
            good.append(sample)
        except (IndexError, ValueError, TypeError):
            bad += 1
    def clean(idx):
        out = []
        for sample in good:
            try:
                x = float(sample[idx])
                if math.isfinite(x):
                    out.append(x)
            except (IndexError, ValueError, TypeError):
                pass
        return out
    hr = clean(0)
    eda = clean(1)
    rr = clean(2)
    diffs = [b - a for a, b in zip(rr, rr[1:])]
    return {'mean_hr_bpm': mean(hr) if hr else math.nan,
            'median_eda_us': median(eda) if eda else math.nan,
            'rmssd_ms': math.sqrt(sum(d*d for d in diffs)/len(diffs)) if diffs else math.nan,
            'valid': len(good), 'bad': bad}
