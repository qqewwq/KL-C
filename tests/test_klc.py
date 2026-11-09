"""Automatyczne testy KL-C, bez urządzeń LBK i biblioteki pylsl."""
import sys
import unittest
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiment'))
from state_estimation import StateEstimator, valid_physio, status_from_share


def sample(hr=70., eda=2., rr=850., focus=.5, quality=0., seq=0):
    return [hr,eda,rr,focus,quality,math.nan,math.nan,math.nan,math.nan,math.nan,seq,seq/4]


class TestKL_C(unittest.TestCase):
    def test_quality_thresholds(self):
        self.assertEqual(status_from_share(9,10)[0], 'poprawny')
        self.assertEqual(status_from_share(6,10)[0], 'zaszumiony')
        self.assertEqual(status_from_share(5,10)[0], 'utracony')
        self.assertEqual(status_from_share(0,0)[0], 'utracony')

    def test_reject_artifacts(self):
        self.assertFalse(valid_physio(sample(hr=250)))
        self.assertFalse(valid_physio(sample(hr=34)))
        self.assertFalse(valid_physio(sample(eda=0)))
        self.assertFalse(valid_physio(sample(eda=-1)))
        self.assertFalse(valid_physio(sample(quality=1)))
        self.assertFalse(valid_physio(sample(quality=2)))
        self.assertFalse(valid_physio(sample(hr=math.nan)))
        self.assertTrue(valid_physio(sample()))

    def test_baseline_30s_medians(self):
        obj = StateEstimator()
        obj.start_baseline(100.0)
        for i in range(120):
            s = sample(hr=70,eda=2,seq=i)
            obj.add_physio(100 + .25*i,s)
        n = obj.finish_baseline()
        self.assertEqual(n,120)
        self.assertEqual(obj.baseline_hr,70)
        self.assertEqual(obj.baseline_eda,2)
        self.assertTrue(obj.baseline_done)

    def test_hysteresis_real_six_seconds(self):
        obj = StateEstimator()
        self.assertFalse(obj.advance('pobudzenie_podwyzszone', 10.0))
        self.assertFalse(obj.advance('pobudzenie_podwyzszone', 15.99))
        self.assertEqual(obj.state,'nieznany')
        self.assertTrue(obj.advance('pobudzenie_podwyzszone', 16.0))
        self.assertEqual(obj.state,'pobudzenie_podwyzszone')
        self.assertEqual(obj.changes,1)
        self.assertFalse(obj.advance('spoczynkowy', 17.0))
        self.assertFalse(obj.advance('nieznany', 18.0))
        self.assertFalse(obj.advance('spoczynkowy', 19.0))
        self.assertEqual(obj.changes,1)

    def test_state_uses_baseline_not_scenario(self):
        obj = StateEstimator()
        obj.baseline_hr = 70.0
        obj.baseline_eda = 2.0
        obj.baseline_done = True
        self.assertEqual(obj.classify(97.,6.0,.4,'poprawny','poprawny'),'pobudzenie_podwyzszone')
        self.assertEqual(obj.classify(76.,3.,.80,'poprawny','poprawny'),'zaangazowanie_wzrokowe')
        self.assertEqual(obj.classify(70.,2.,.40,'poprawny','poprawny'),'spoczynkowy')
        self.assertEqual(obj.classify(97.,6.,.4,'utracony','poprawny'),'nieznany')
        self.assertEqual(obj.classify(97.,6.,.4,'poprawny','utracony'),'nieznany')


if __name__ == '__main__':
    unittest.main(verbosity=2)
