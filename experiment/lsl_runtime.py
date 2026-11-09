"""KL-C: console dla eksperymentatora + LSL markers + plik statusu co 1 s."""
from pathlib import Path
from datetime import datetime
import csv
import math
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_byprop, local_clock
from state_estimation import StateEstimator
from feature_calc_klb import calculate_features

FIELDS = ['t_lsl', 't_rel', 'seq', 'sim_t', 'gaze_pct', 'gaze_quality',
          'eda_pct', 'eda_quality', 'state', 'candidate',
          'baseline_eda', 'baseline_hr', 'eda_med_us', 'hr_med_bpm',
          'focus_med', 'bad_total']


class LBKMonitor:
    def __init__(self, participant='TEST-01'):
        self.est = StateEstimator()
        self.last_report = local_clock()
        self.start_t = self.last_report
        self.inlet = None
        self.last_seen_gaze = None
        self.last_seen_gaze_t = -1.0
        self.participant = ''.join(x for x in str(participant) if x.isalnum() or x in '-_') or 'TEST-01'
        self.status_dir = Path(__file__).resolve().parent.parent / 'sample_data'
        self.status_dir.mkdir(parents=True, exist_ok=True)
        filename = 'KL-C_STATUS_' + self.participant + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
        self.csv_path = self.status_dir / filename
        self.csv_file = open(self.csv_path, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csv_file, fieldnames=FIELDS)
        self.writer.writeheader()
        info = StreamInfo('LBK_Markers', 'Markers', 1, 0, 'string', 'lbk-p3-klc-markers-v1')
        self.markers = StreamOutlet(info)
        print('KL-C: status:', self.csv_path)
        self.connect(0.2)

    def connect(self, timeout):
        try:
            found = resolve_byprop('name', 'LBK_Sim', timeout=timeout)
            if found:
                self.inlet = StreamInlet(found[0], max_buflen=80)
                print('KL-C: LBK_Sim polaczony')
        except Exception as exc:
            print('KL-C: blad polaczenia:', exc)

    def marker(self, value):
        value = str(value)
        self.markers.push_sample([value], timestamp=local_clock())
        print('MARKER', value)

    def start_baseline(self):
        self.est.start_baseline(local_clock())
        self.marker('calib:start|phase=rest30')

    def finish_baseline(self):
        n = self.est.finish_baseline()
        self.marker('calib:end|phase=rest30|accepted=' + str(n))
        print('KL-C BASELINE: HR=', self.est.baseline_hr,
              'EDA=', self.est.baseline_eda, 'valid=', n)

    def sample_gaze(self, tracker, now):
        # MouseGaze: status 0 jest poprawny, 2 oznacza symulowane mrugniecie.
        ok = False
        if tracker is not None:
            try:
                sample = tracker.getLastSample()
                if sample is not None:
                    st = getattr(sample, 'time', None)
                    if st != self.last_seen_gaze:
                        self.last_seen_gaze = st
                        self.last_seen_gaze_t = now
                    x, y = getattr(sample, 'gaze_x', None), getattr(sample, 'gaze_y', None)
                    ok = (getattr(sample, 'status', -1) == 0 and
                          x is not None and y is not None and
                          math.isfinite(float(x)) and math.isfinite(float(y)) and
                          now - self.last_seen_gaze_t < 0.15)
            except (TypeError, ValueError, AttributeError):
                pass
        self.est.add_gaze(now, ok)

    def poll(self, tracker=None):
        now = local_clock()
        if self.inlet is None:
            if now - self.last_report >= 1.0:
                self.connect(0.0)
        else:
            try:
                chunk, stamps = self.inlet.pull_chunk(timeout=0.0, max_samples=128)
                for sample, stamp in zip(chunk, stamps):
                    self.est.add_physio(stamp, sample)
            except Exception as exc:
                print('KL-C: zerwany strumien:', exc)
                self.inlet = None
        self.sample_gaze(tracker, now)
        if now - self.last_report >= 1.0:
            state = self.est.evaluate(now)
            if state['changed']:
                self.marker('state:' + state['state'])
            row = {k: (now - self.start_t if k == 't_rel' else state.get(k)) for k in FIELDS}
            self.writer.writerow(row)
            self.csv_file.flush()
            print('KL-C | GAZE', state['gaze_quality'], f"{state['gaze_pct']:.0f}%",
                  '| EDA', state['eda_quality'], f"{state['eda_pct']:.0f}%",
                  '| STAN', state['state'], '| odrzucone', state['bad_total'])
            self.last_report = now

    def close(self):
        try:
            self.csv_file.flush()
            self.csv_file.close()
        except Exception:
            pass
