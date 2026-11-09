# Wyniki KL-C: noisy

- Zgodność ogólna po kalibracji: **18.4%**
- Zgodność przy obu sygnałach poprawnych: **6.8%**
- Zmiany stanu: **0**; markery state w XDF: **0**
- Punkty statusu: **358**, sparowane przez seq: **326**

| Jakość | poprawny | zaszumiony | utracony |
|---|---:|---:|---:|
| gaze | 98.0% | 2.0% | 0.0% |
| eda | 23.5% | 75.4% | 1.1% |

**Uwaga:** symulatorowe scenario jest etykietą testową, a nie diagnozą. Stan `nieznany` obejmuje także fazę `zmeczenie`, której KL-C P3 osobno nie wykrywa.
