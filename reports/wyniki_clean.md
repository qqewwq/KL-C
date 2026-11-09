# Wyniki KL-C: clean

- Zgodność ogólna po kalibracji: **39.6%**
- Zgodność przy obu sygnałach poprawnych: **40.1%**
- Zmiany stanu: **7**; markery state w XDF: **9**
- Punkty statusu: **358**, sparowane przez seq: **326**

| Jakość | poprawny | zaszumiony | utracony |
|---|---:|---:|---:|
| gaze | 96.7% | 2.8% | 0.6% |
| eda | 100.0% | 0.0% | 0.0% |

**Uwaga:** symulatorowe scenario jest etykietą testową, a nie diagnozą. Stan `nieznany` obejmuje także fazę `zmeczenie`, której KL-C P3 osobno nie wykrywa.
