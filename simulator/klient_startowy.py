#!/usr/bin/env python3
"""
Klient startowy (szkielet) – laboratorium KCK. Odbiera strumień NDJSON z symulatora
(tryb tcp) i wypisuje średnią kroczącą HR oraz RMSSD. Uzupełnij miejsca oznaczone TODO.
Uruchom najpierw:  python symulator_biosygnalow.py --mode tcp --scenario mix
"""
import json, socket, math
from collections import deque

WINDOW = 20  # liczba próbek w oknie (przy 4 Hz = 5 s)


def rmssd(rr):
    d = [b - a for a, b in zip(rr, list(rr)[1:])]
    return math.sqrt(sum(x * x for x in d) / len(d)) if d else None


def main(host="127.0.0.1", port=5555):
    hr_win, rr_win = deque(maxlen=WINDOW), deque(maxlen=WINDOW)
    with socket.create_connection((host, port)) as s, s.makefile("r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec["quality"] != "ok":      # TODO (L3): lepsza obsługa artefaktów i braków
                continue
            hr_win.append(rec["hr"]); rr_win.append(rec["rr_ms"])
            mean_hr = sum(hr_win) / len(hr_win)
            r = rmssd(rr_win)
            # TODO (L3): estymacja stanu (kalibracja linii bazowej, progi z histerezą)
            # TODO (L4): wywołanie modułu adaptacji interfejsu
            print(f"t={rec['t']:7.2f}s  HR~{mean_hr:5.1f}  RMSSD={r if r is None else round(r,1)}  EDA={rec['eda_us']}")


if __name__ == "__main__":
    main()
