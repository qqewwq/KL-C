"""Test okna 5 s i RMSSD bez pakietu pylsl."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiment'))
from feature_calc_klb import calculate_features


def test_features():
    records = [
        (1., [60., 2., 800., .5, 0.]),
        (2., [70., 4., 820., .5, 0.]),
        (3., [90., 100., 950., .5, 1.]),  # noisy = pomijamy
        (4., [80., 3., 790., .5, 0.]),
    ]
    f = calculate_features(records)
    assert f['valid'] == 3 and f['bad'] == 1
    assert abs(f['mean_hr_bpm'] - 70.) < 1e-9
    assert f['median_eda_us'] == 3.
    assert abs(f['rmssd_ms'] - math.sqrt((20**2+(-30)**2)/2)) < 1e-9

if __name__ == '__main__':
    test_features()
    print('OK: HR, RMSSD z roznic RR, mediana EDA, odrzucenie noisy')
