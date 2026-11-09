"""KL-C: kontrola jakości i estymacja stanu. Moduł niezależny od PsychoPy/LSL."""
from collections import deque
from statistics import median
import math

QUALITY_OK = 0.0
WINDOW_GAZE = 2.0
WINDOW_EDA = 5.0
BASELINE_SECONDS = 30.0
HYSTERESIS_SECONDS = 6.0


def is_num(value):
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def valid_physio(sample):
    """Sprawdza kompletność, flagę quality i zakresy fizjologiczne."""
    if len(sample) < 5 or not is_num(sample[4]) or float(sample[4]) != QUALITY_OK:
        return False
    if not (is_num(sample[0]) and 35 <= float(sample[0]) <= 200):
        return False
    if not (is_num(sample[1]) and float(sample[1]) > 0):
        return False
    if not (is_num(sample[2]) and 300 <= float(sample[2]) <= 2000):
        return False
    return True


def status_from_share(valid, total):
    """Trzy poziomy jakości na podstawie udziału poprawnych próbek."""
    share = valid / total if total else 0.0
    label = 'poprawny' if share >= 0.90 else ('zaszumiony' if share >= 0.60 else 'utracony')
    return label, round(100 * share, 2)


class StateEstimator:
    """Przetwarza stan na zegarze LSL; nie zna pola scenario."""
    def __init__(self):
        self.physio = deque()
        self.gaze = deque()
        self.baseline_start = None
        self.baseline_hr = math.nan
        self.baseline_eda = math.nan
        self.baseline_done = False
        self.rest_samples = []
        self.state = 'nieznany'
        self.candidate = None
        self.candidate_since = None
        self.changes = 0
        self.invalid_total = 0
        self.last_seq = None
        self.last_sim_t = None

    def start_baseline(self, now):
        self.baseline_start = float(now)
        self.rest_samples = []
        self.baseline_done = False

    def add_physio(self, stamp, sample):
        ok = valid_physio(sample)
        self.physio.append((float(stamp), sample, ok))
        if not ok:
            self.invalid_total += 1
        if len(sample) >= 12:
            if is_num(sample[10]):
                self.last_seq = int(sample[10])
            if is_num(sample[11]):
                self.last_sim_t = float(sample[11])
        if self.baseline_start is not None and not self.baseline_done and ok:
            if self.baseline_start <= stamp < self.baseline_start + BASELINE_SECONDS:
                self.rest_samples.append((float(sample[0]), float(sample[1])))
        self.trim(stamp)

    def add_gaze(self, stamp, valid):
        self.gaze.append((float(stamp), bool(valid)))
        self.trim(stamp)

    def trim(self, now):
        while self.physio and self.physio[0][0] < now - 60.0:
            self.physio.popleft()
        while self.gaze and self.gaze[0][0] < now - 10.0:
            self.gaze.popleft()

    def finish_baseline(self):
        """Brak danych nie może być zamieniony na pozornie poprawną linię bazową."""
        self.baseline_done = True
        if len(self.rest_samples) >= 40:
            self.baseline_hr = median([v[0] for v in self.rest_samples])
            self.baseline_eda = median([v[1] for v in self.rest_samples])
        return len(self.rest_samples)

    def evaluate(self, now):
        self.trim(now)
        ep = [r for r in self.physio if now - WINDOW_EDA <= r[0] <= now]
        gp = [r for r in self.gaze if now - WINDOW_GAZE <= r[0] <= now]
        e_label, e_pct = status_from_share(sum(r[2] for r in ep), len(ep))
        g_label, g_pct = status_from_share(sum(r[1] for r in gp), len(gp))
        v = [r[1] for r in ep if r[2]]
        hr = median([float(s[0]) for s in v]) if v else math.nan
        eda = median([float(s[1]) for s in v]) if v else math.nan
        foc = median([float(s[3]) for s in v if is_num(s[3])]) if any(is_num(s[3]) for s in v) else math.nan
        candidate = self.classify(hr, eda, foc, e_label, g_label)
        changed = self.advance(candidate, now)
        return {'t_lsl': now, 'gaze_quality': g_label, 'gaze_pct': g_pct,
                'eda_quality': e_label, 'eda_pct': e_pct,
                'state': self.state, 'candidate': candidate, 'changed': changed,
                'hr_med_bpm': hr, 'eda_med_us': eda, 'focus_med': foc,
                'baseline_hr': self.baseline_hr, 'baseline_eda': self.baseline_eda,
                'bad_total': self.invalid_total,
                'seq': self.last_seq, 'sim_t': self.last_sim_t}

    def classify(self, hr, eda, focus, eda_quality, gaze_quality):
        # P3: stan szczególny 'zaangazowanie_wzrokowe' to jedynie symulacyjny wskaźnik.
        if not (self.baseline_done and is_num(self.baseline_hr) and is_num(self.baseline_eda)):
            return 'nieznany'
        if eda_quality != 'poprawny' or gaze_quality == 'utracony':
            return 'nieznany'
        if not (is_num(hr) and is_num(eda)):
            return 'nieznany'
        de = eda - self.baseline_eda
        dh = hr - self.baseline_hr
        if de >= 1.2 and dh >= 7.0:
            return 'pobudzenie_podwyzszone'
        if gaze_quality == 'poprawny' and is_num(focus) and focus >= 0.67 and de < 1.2:
            return 'zaangazowanie_wzrokowe'
        if abs(de) <= 0.55 and abs(dh) <= 9.0:
            return 'spoczynkowy'
        return 'nieznany'

    def advance(self, next_state, now):
        # Histereza czasowa: 6 s jednej kandydatury, nie 6 kolejnych klatek.
        if next_state == self.state:
            self.candidate = None
            self.candidate_since = None
            return False
        if next_state != self.candidate:
            self.candidate = next_state
            self.candidate_since = float(now)
            return False
        if now - self.candidate_since >= HYSTERESIS_SECONDS:
            self.state = next_state
            self.changes += 1
            self.candidate = None
            self.candidate_since = None
            return True
        return False
