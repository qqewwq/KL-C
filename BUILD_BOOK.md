# BUILD BOOK – P3 „Obraz, ocena, pobudzenie”

**Etap:** KL-A + KL-B + KL-C · **Ostatnia aktualizacja:** 2026-11-09 · **Tag repozytorium:** `KL-C`
**Rozdziały w tej wersji:** 0, 1 (KL-A), 3, 4, 6 (KL-B), **5, 7 (KL-C)**, 14, 15.

**Pliki etapów:** rozdz. 3, 4 i 6 opisują eksperyment z etapu KL-B (`P3_KL_B.psyexp`, nagranie `P3_KL-B_TEST-01_S001.xdf`, wykres `eda_markery.png`, `docs/petla_biofeedback.py`) – wersja z repozytorium https://github.com/qqewwq/KL-B (tag `KL-B`); nagranie, wykres i schemat z KL-B są też w tym katalogu (`sample_data/`, `docs/img/`, `docs/`). W KL-C eksperyment rozbudowano do `experiment/P3_KL_C-2.psyexp` (rozdz. 7.1).

**Czytelnik docelowy:** osoba znająca Pythona, ale nie PsychoPy, LSL ani tego projektu, przy czystym komputerze z Windows (stanowisko LBK). Polecenia podajemy w dwóch wariantach: **Windows** (`py -3 …`, PowerShell) i **macOS** (`python3 …`, Terminal). Wszystkie polecenia uruchamiamy **z katalogu głównego repozytorium** (tam, gdzie leży ten plik).

**Oznaczenia autorów:** DK – Diana Kalinina, OS – Oleksandr Shamak. Przy każdym kroku: **wykonanie** – kto zrobił dany krok na komputerze; **opis** – kto napisał i zredagował opis kroku w Build Booku; data.

---

## 0. Metryczka

| Pole | Wartość |
|---|---|
| Pakiet | P3 – Obraz, ocena, pobudzenie |
| Badanie budowane w KL-B | główne: „Qualia, barwa i subiektywne doświadczenie” |
| Badanie drugie | „Reklama spod ręki człowieka czy algorytmu?” (poza KL-B) |
| Protokół | `Badania_EyeTracking.pptx` z folderu kursu „Pakiet P3 – materiały badań LBK” (pobrany 2026-11-08; slajdy 6, 8, 13, 22). Plik **nie** jest w repozytorium – pobiera się go z kursu. |
| Zespół | DK – Diana Kalinina, OS – Oleksandr Shamak |
| Repozytorium | https://github.com/qqewwq/KL-C · tag `KL-C` (etap KL-B: https://github.com/qqewwq/KL-B, tag `KL-B`) |
| Komputer testowy | MacBook Air, Apple Silicon, macOS 27 (najnowsza wersja, listopad 2026) |
| PsychoPy | Standalone **2025.2.4** (okno pokazuje `v2025.2.4beta`), Python 3.10.11, uruchamiany przez Rosetta 2 |
| Python poza PsychoPy | `.venv` z Pythonem 3.9 (most, testy, wykres) |
| pylsl / liblsl | pylsl **1.18.2** w `.venv`; universal liblsl x86_64/arm64 w `/Library/Frameworks/lsl.framework/Versions/A/lsl` dla PsychoPy (zmienna `PYLSL_LIB`) |
| LabRecorder | **1.18.0** (macOS, Homebrew) |
| pyxdf, matplotlib | w `.venv` (wersje: `.venv/bin/python -m pip show pyxdf matplotlib`) |
| Ekran w eksperymencie | okno 1920×1080 px, jednostki `pix`, monitor `testMonitor` (tymczasowo); częstotliwość odświeżania i wymiary monitora LBK – do wpisania na stanowisku |
| Aparatura LBK | EyeLogic (wzrok), GSR/EDA; wersje sterowników i nazwy strumieni – do wpisania na sesji w LBK (pyt. 14.4) |

**Jak sprawdzić:** PsychoPy → *Help → About* pokazuje tę samą wersję; w repozytorium istnieje tag `KL-B`.

---

## 1. Instalacja od zera

> Rozdział z KL-A (instalacja PsychoPy, demo, symulator). Instalacja pylsl i LabRecorder potrzebna w KL-B jest w kroku **6.1**.

### Krok 1.1 – Instalacja PsychoPy · autor: DK · 2026-10-12

- **Cel:** zainstalować PsychoPy w wersji uzgodnionej w zespole.
- **Gdzie:** https://www.psychopy.org/download.html → wersja Standalone **2025.2.4**. Windows: instalator `.exe`, domyślna ścieżka. macOS: `StandalonePsychoPy-2025.2.4-macOS-3.10.dmg` → przeciągnąć do `/Applications`; przy pierwszym uruchomieniu zgodzić się na instalację Rosetta 2.
- **Jak sprawdzić:** PsychoPy otwiera okna Builder, Coder i Runner bez komunikatu o błędzie; *Help → About* pokazuje 2025.2.4.
- **Typowe problemy:** wersja 2026.x na macOS zgłaszała `wx._core.wxAssertionError` (locale) – zainstalować 2025.2.4. Przy `Launch error (py2app)` sprawdzić `~/.psychopy3/last_app_load.log`.
- **Zrzut:** `docs/img/1-1-psychopy.png`

### Krok 1.2 – Test demo · autor: DK · 2026-10-12

- **Cel:** sprawdzić, że PsychoPy wyświetla bodźce.
- **Gdzie:** Coder → *Demos → basic → hello_world.py* → **Run**.
- **Jak sprawdzić:** otwiera się okno z napisami `Hello world!` i `¡Hola mundo!`.
- **Zrzut:** `docs/img/1-2-demo.png`

### Krok 1.3 – Symulator biosygnałów · autor: DK · 2026-10-12

- **Cel:** sprawdzić symulator, który na własnym komputerze zastępuje czujniki LBK.
- **Gdzie:** `simulator/symulator_biosygnalow.py` (z archiwum kursu „Kod do laboratorium – symulator i klient startowy”; tylko biblioteka standardowa Pythona 3.8+).
- **Polecenie testowe:** Windows `py -3 simulator/symulator_biosygnalow.py --mode stdout --scenario stres --duration 5` · macOS `python3 simulator/symulator_biosygnalow.py --mode stdout --scenario stres --duration 5`
- **Jak sprawdzić:** w konsoli pojawiają się linie JSON co 0,25 s (4 Hz) z polami `t, seq, hr, rr_ms, eda_us, focus, quality, scenario`; część linii ma `quality="noisy"` lub `"lost"` (przy `lost` pola sygnałów mają wartość `null`).

| Pole | Znaczenie | Jednostka |
|---|---|---|
| `t` | czas od startu symulacji | s |
| `seq` | numer próbki | – |
| `hr` | tętno | bpm |
| `rr_ms` | odstęp R–R | ms |
| `eda_us` | przewodnictwo skóry | µS |
| `focus` | umowny wskaźnik „skupienia” (nie jest pomiarem wzroku) | 0–1 |
| `quality` | jakość próbki | `ok` / `noisy` / `lost` |
| `scenario` | etykieta „prawdy” symulatora – **nie wolno** jej używać do sterowania | tekst |

Symulator **nie** wysyła `gaze_x`, `gaze_y`, `gaze_valid`, `pupil_mm`, `resp`.

---

## 3. Budowa eksperymentu krok po kroku (KL-B)

**Wynik końcowy rozdziału:** plik `experiment/P3_KL_B.psyexp` – instrukcja → pętla 4 prób z pliku CSV (krzyż 0,5 s → obraz 4 s → szary ekran 1 s) → jedno pytanie 1–9 → koniec, z MouseGaze, Eyetracker Record i integracją LSL.
**Gotowy plik jest w repozytorium** – wystarczy go otworzyć (krok 3.1). Kroki 3.2–3.12 opisują każde ustawienie tak, żeby dało się go odtworzyć ręcznie w pustym Builderze albo sprawdzić, czy nic się nie zmieniło.

**Przebieg czasowy jednej próby** (przy 60 Hz):

| Element | Czas | Klatki przy 60 Hz | Źródło |
|---|---|---|---|
| krzyż fiksacyjny | 500 ms | 30 | **roboczo** – protokół go nie określa (pyt. 14.6) |
| obraz | 4000 ms | 240 | protokół P3 (niezmienny) |
| szary ekran | 1000 ms | 60 | protokół P3 (niezmienny) |

Czasy w Builderze są ustawione w sekundach (`duration (s)`); pomiar dokładności w klatkach – rozdział 9 (KL-E).

### Krok 3.1 – Otwarcie eksperymentu i Flow · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** otworzyć szkielet badania i zobaczyć kolejność ekranów.
- **Gdzie:** PsychoPy → Builder → *File → Open* → `experiment/P3_KL_B.psyexp`.
- **Ustawienia (Flow, od lewej):** `intro` → pętla `trials` wokół `fixation` → `stimulus` → `gray` → `rating` → `end`. Pętla obejmuje **tylko** trzy środkowe routines; `rating` jest **po** pętli (jedno pytanie po bloku).
- **Zrzut:** `docs/img/3-1-flow.png`
- **Jak sprawdzić:** widać 6 zakładek routines (`intro, fixation, stimulus, gray, rating, end`) i pętlę `trials` z czasami 0.50 s, 4.00 s, 1.00 s.
- **Typowe problemy:** ostrzeżenie o innej wersji pliku – plik zapisano w formacie 2025.x; otwierać w PsychoPy 2025.2.4.

### Krok 3.2 – Ustawienia eksperymentu (Basic, Screen, Data) · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** ustawić okno, jednostki i dane wyjściowe zgodnie z konwencją LBK.
- **Gdzie:** Builder → ikona zębatki (*Experiment settings*).
- **Ustawienia:**

| Zakładka | Pole | Wartość |
|---|---|---|
| Basic | Experiment name | `P3_KL_B` |
| Basic | Experiment info | `{'participant':'TEST-01','session':'S001'}` – **tylko pseudonim**, nigdy imię i nazwisko |
| Basic | Show info dialog | włączone |
| Screen | Window size | `[1920, 1080]` |
| Screen | Full-screen | wyłączone na komputerze testowym; **na stanowisku LBK włączyć** |
| Screen | Units | `pix` |
| Screen | Monitor | `testMonitor` (tymczasowo; na LBK – profil z Monitor Center) |
| Screen | Background | `black` |
| Data | Data filename | `u'data' + os.sep + 'P3_glowne_%s_%s_%s' % (expInfo['participant'], expInfo['session'], data.getDateStr(format='%Y-%m-%d_%H%M'))` |
| Data | Save csv / excel / psydat / log / hdf5 | włączone |

- **Zrzut:** — (wszystkie wartości w tabeli powyżej; zakładka *Eyetracking* – `docs/img/3-5-mousegaze.png`).
- **Jak sprawdzić:** po przebiegu w `experiment/data/` powstaje m.in. `P3_glowne_TEST-01_S001_2026-11-08_1720.csv` (format `{pakiet}_{badanie}_{kod}_{sesja}_{RRRR-MM-DD_GGMM}`).
- **Typowe problemy:** na laptopie z ekranem mniejszym niż 1920×1080 okno wychodzi poza ekran i PsychoPy pokazuje `dropped frames` – to dopuszczalne w teście technicznym, nie na stanowisku LBK.

### Krok 3.3 – Eyetracking: MouseGaze · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** symulować wzrok myszą; w LBK zmienia się tylko to jedno ustawienie na EyeLogic.
- **Gdzie:** Experiment settings → zakładka **Eyetracking**.
- **Ustawienia:** `Eyetracker device = MouseGaze`; `Move button = CONTINUOUS`; `Blink button = MIDDLE_BUTTON`; `Saccade threshold = 0.5`.
- **Zrzut:** `docs/img/3-5-mousegaze.png`
- **Jak sprawdzić:** po przebiegu w `experiment/data/` jest plik `.hdf5` z próbkami pozycji myszy z czasu wyświetlania obrazów.
- **Typowe problemy:** MouseGaze zapisuje dane lokalnie (HDF5) i **nie tworzy strumienia LSL** – w LabRecorder są tylko 2 strumienie.

### Krok 3.4 – Routine `intro` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** instrukcja; uruchomienie LSL; znacznik `exp:start` po naciśnięciu spacji.
- **Gdzie:** zakładka routine `intro`. Komponenty (kolejność od góry): `lsl_intro` (Code), `instrukcja` (Text), `start_key` (Keyboard).
- **Ustawienia:**
  - `instrukcja`: start 0 s, czas pusty (do końca routine), wysokość 38 px, wrap 1500 px, font Arial, kolor white. Tekst (Enter = nowa linia):
    *Za chwilę zobaczysz kilka obrazów. / Oglądaj je swobodnie. / Po obejrzeniu wszystkich obrazów ocenisz, jak silne pobudzenie odczuwałaś/odczuwałeś (skala 1–9). / Naciśnij SPACJĘ, aby rozpocząć.*
  - `start_key`: Allowed keys `'space'`, Force end of Routine ✔, Store `last key`.
  - `lsl_intro` (Code Type `Py`):

```python
# --- Begin Experiment ---
# Importuje moduł z experiment/lsl_runtime.py (ten sam katalog co .psyexp).
# Tworzy strumień LBK_Markers i łączy się z LBK_Sim (most musi już działać).
from lsl_runtime import LBKMonitor
lbk = LBKMonitor(window_seconds=5.0)

# --- Each Frame ---
lbk.poll()          # odbiór LBK_Sim bez blokowania + raport co 1 s w konsoli

# --- End Routine ---
# exp:start dopiero po spacji – eksperymentator zdąży włączyć LabRecorder na ekranie instrukcji
lbk.marker('exp:start|study=P3|list=L1_LBK_4obrazy_test|session=' + str(expInfo['session']))
```

- **Zrzut:** `docs/img/3-1-flow.png` (widok routine `intro`).
- **Jak sprawdzić:** w konsoli Runnera najpierw `LBK_Sim: polaczony`, a po spacji `MARKER exp:start|study=P3|…`.
- **Typowe problemy:** `LBK_Sim: BRAK - uruchom symulator i most przed PsychoPy` – patrz 6.4. `ModuleNotFoundError: lsl_runtime` – plik `lsl_runtime.py` musi leżeć obok `.psyexp`. **Instrukcja pokazuje dosłowne `\n`** – w polu tekstu nowe linie wpisuje się Enterem, nie znakami `\n` (błąd z wersji z 2026-11-08, poprawiony – rozdz. 15).

### Krok 3.5 – Pętla `trials` z pliku warunków · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** jedna pętla prezentuje wszystkie próby bloku w kolejności z pliku CSV.
- **Gdzie:** Flow → *Insert Loop* – początek przed `fixation`, koniec za `gray`.
- **Ustawienia:** Name `trials`; loopType `sequential`; nReps `1`; Conditions `conditions/L1_LBK_4obrazy_test.csv` (ścieżka względem `.psyexp`); Selected rows – puste; random seed – puste; Is trials ✔.
- **Zrzut:** `docs/img/3-1-flow.png` (pętla `trials` na Flow; ustawienia pętli – lista powyżej).
- **Jak sprawdzić:** okno pętli pokazuje *4 conditions, with 7 parameters [trial_id, stimulus_id, image_file, block, condition, stim_width, stim_height]*; wynikowy CSV ma 4 wiersze prób, `stimulus_id` w kolejności A, B, C, D.
- **Typowe problemy:** „Could not find conditions file” – ścieżka liczona od katalogu `experiment/`.

### Krok 3.6 – Routine `fixation` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** krzyż przed obrazem i znacznik początku próby.
- **Gdzie:** routine `fixation`: `lsl_fix` (Code), `krzyzyk` (Text).
- **Ustawienia:** `krzyzyk`: tekst `+`, start 0 s, czas **0.5 s**, wysokość 80 px, pos (0,0), white.

```python
# lsl_fix – Begin Routine: początek próby (trial_id z pliku warunków)
lbk.marker('trial:start|trial=' + str(trial_id))
# lsl_fix – Each Frame
lbk.poll()
```

- **Zrzut:** — (widok w `docs/img/3-1-flow.png`).
- **Jak sprawdzić:** w konsoli `MARKER trial:start|trial=1` … `trial=4`.

### Krok 3.7 – Routine `stimulus`: obraz, Eyetracker Record, `stim:onset` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** pokazać obraz z protokołu przez 4 s, nagrywać wzrok i wysłać znacznik dokładnie w chwili pojawienia się obrazu.
- **Gdzie:** routine `stimulus`: `lsl_stim` (Code), `obraz` (Image), `etRecord` (Eyetracker Record – w panelu *Components → Eyetracking*).
- **Ustawienia:**
  - `obraz`: Image `$image_file` (*set every repeat*); Size `$[stim_width, stim_height]` (*set every repeat*) – obrazy w natywnym rozmiarze, bez skalowania; pos (0,0); start 0 s; czas **4.0 s**.
  - `etRecord`: Action `Start and Stop`; start 0 s; czas **4.0 s**.
  - `lsl_stim`:

```python
# --- Begin Routine ---
# callOnFlip: znacznik zostanie wysłany w chwili odświeżenia ekranu,
# na którym obraz pojawia się po raz pierwszy (nie w chwili wejścia w routine).
win.callOnFlip(lbk.marker, 'stim:onset|stim=' + str(stimulus_id))
# --- Each Frame ---
lbk.poll()
# --- End Routine ---
lbk.marker('stim:offset|stim=' + str(stimulus_id))
```

- **Zrzut:** `docs/img/3-3-stimulus.png`
- **Jak sprawdzić:** każdy z 4 obrazów widać ok. 4 s; w XDF odstęp `stim:onset` → `stim:offset` wynosi ok. 3,96–3,98 s (zmierzone 2026-11-08: 3,957 / 3,973 / 3,976 / 3,979 s; ~40 ms różnicy względem 4,000 s to moment wysłania `stim:offset` w End Routine – dokładny pomiar w KL-E).
- **Typowe problemy:** `Could not find image` – ścieżki w CSV są względne względem `experiment/`, nazwy plików zawierają spację (`Bodziec A.PNG`) i wielkie litery rozszerzenia – na Windows bez znaczenia, na macOS/Linux wielkość liter musi się zgadzać.

### Krok 3.8 – Routine `gray` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** szary ekran 1 s po obrazie (z protokołu).
- **Gdzie:** routine `gray` → *Routine settings*: kolor tła `0` (rgb, szary); komponent `szary_ekran` (Text, tekst = spacja, start 0 s, czas **1.0 s** – wyznacza długość routine); `lsl_gray` (Each Frame: `lbk.poll()`).
- **Zrzut:** — (widok w `docs/img/3-1-flow.png`).
- **Jak sprawdzić:** w XDF odstęp `stim:offset` → następny `trial:start` = 1,00 s.
- **Uwaga:** to jest miejsce na przyszłą adaptację (KL-D: dłuższa przerwa / ekran neutralny). Czasów obrazu i szarego ekranu nie wolno zmieniać.

### Krok 3.9 – Routine `rating`: jedno pytanie po bloku · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** jedna odpowiedź uczestnika (robocza ocena pobudzenia 1–9).
- **Gdzie:** routine `rating`: `lsl_rating` (Code), `pytanie` (Text), `rating_resp` (Keyboard).
- **Ustawienia:** `pytanie`: wysokość 37 px, tekst *Jak silne pobudzenie odczuwałaś/odczuwałeś podczas oglądania obrazów? / 1 = bardzo słabe … 9 = bardzo silne / Naciśnij klawisz od 1 do 9.*; `rating_resp`: Allowed keys `'1','2','3','4','5','6','7','8','9'`, Force end ✔, Store `last key`.

```python
# lsl_rating – Each Frame
lbk.poll()
# lsl_rating – End Routine: znacznik odpowiedzi z klawiszem i czasem reakcji [s]
if rating_resp.keys:
    rt_value = rating_resp.rt if rating_resp.rt is not None else -1.0
    lbk.marker('resp|q=SAM_AROUSAL_ROBOCZE|key=' + str(rating_resp.keys)
               + '|rt=' + str(round(float(rt_value), 3)))
```

- **Zrzut:** — (widok w `docs/img/3-1-flow.png`).
- **Jak sprawdzić:** w CSV kolumny `rating_resp.keys` i `rating_resp.rt`; w XDF `resp|q=SAM_AROUSAL_ROBOCZE|key=…|rt=…`.
- **Odstępstwo:** to **nie** jest pełna ankieta SAM (walencja, pobudzenie, dominacja, slajd 13). Wersja robocza do czasu decyzji LBK (pyt. 14.6).

### Krok 3.10 – Routine `end` · wykonanie: DK · opis: OS · 2026-11-08

- **Gdzie:** routine `end`: `koniec` (Text „Dziękujemy! To już koniec.”, 42 px, start 0 s, czas **2 s**), `lsl_end` (Code).

```python
# lsl_end – Begin Routine
lbk.marker('exp:end')
# lsl_end – Each Frame
lbk.poll()
# lsl_end – End Experiment: podsumowanie odebranych i odrzuconych próbek
lbk.summary()
```

- **Jak sprawdzić:** ostatnie linie konsoli: `MARKER exp:end` i `LBK_Sim: odebrano N probek, odrzucono (quality != ok) M`.

### Krok 3.11 – Moduł `experiment/lsl_runtime.py` · kod: DK, poprawki: OS · opis: OS · 2026-11-08

- **Cel:** cała logika LSL w jednym pliku Pythona zamiast w polach Code Components.
- **Gdzie:** `experiment/lsl_runtime.py` (obok `.psyexp`; Builder importuje go w kroku 3.4).
- **Zawartość:**

| Element | Co robi |
|---|---|
| `LBKMonitor.__init__` | tworzy `LBK_Markers` (Markers, 1 kanał string, 0 Hz); szuka `LBK_Sim` przez 0,5 s; uruchamia `ContinuousResolver` do nieblokującego ponownego połączenia |
| `marker(tekst)` | `push_sample([tekst], local_clock())` + wydruk `MARKER …` |
| `poll()` | w każdej klatce: `pull_chunk(timeout=0.0, max_samples=128)`, dopisanie próbek do okna, usunięcie starszych niż 5 s (zegar LSL), co 1 s wydruk cech |
| `calculate_features()` | średnie HR, RMSSD, mediana EDA z próbek `quality = ok`; liczba poprawnych i odrzuconych |
| `summary()` | podsumowanie na końcu |

- **Jak sprawdzić:** test jednostkowy (bez LSL i PsychoPy): Windows `py -3 tests/test_features.py` · macOS `python3 tests/test_features.py` → `OK: HR, RMSSD z sasiednich roznic RR, mediana EDA, odrzucenie noisy/lost/NaN`.

### Krok 3.12 – Dane wyjściowe PsychoPy · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** wiedzieć, jakie pliki powstają po jednym przebiegu.
- **Gdzie:** `experiment/data/` (katalog jest w `.gitignore` – danych z sesji nie wrzucamy do repozytorium).
- **Pliki:** `P3_glowne_<kod>_<sesja>_<data>.csv` (jedna linia = jedna próba + wiersz odpowiedzi), `.xlsx`, `.psydat`, `.log`, `.hdf5` (MouseGaze). Kluczowe kolumny CSV: `trial_id`, `stimulus_id`, `image_file`, `condition`, `obraz.started`, `obraz.stopped`, `rating_resp.keys`, `rating_resp.rt`, `participant`, `session`.
- **Zrzut:** — (lista plików powyżej).
- **Jak sprawdzić:** CSV ma 4 wiersze z `trial_id` = 1–4 i jeden wiersz z `rating_resp.keys`.

**Sprawdzenie rozdziału 3 (jak poznać, że działa):** przy działającym symulatorze i moście (6.4) uruchom eksperyment z `participant=TEST-01`, `session=S001`. Oczekiwane: 4 obrazy A–D po 4 s z szarym ekranem 1 s, jedno pytanie 1–9, ekran końcowy; w konsoli co ~1 s linia `5s | HR= … bpm | RMSSD= … ms | EDA med= … uS | valid= … bad_window= … bad_total= …` oraz kolejno znaczniki: `exp:start`, 4 × (`trial:start`, `stim:onset`, `stim:offset`), `resp`, `exp:end`; w `experiment/data/` pliki z kroku 3.12.

---

## 4. Pliki warunków, listy, randomizacja (KL-B)

### Krok 4.1 – Plik warunków bloku testowego · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** oddzielić listę bodźców i ich parametry od konfiguracji Buildera.
- **Gdzie:** `experiment/conditions/L1_LBK_4obrazy_test.csv` (UTF-8, separator przecinek, pierwszy wiersz = nagłówki); czyta go pętla `trials` (krok 3.5).
- **Kolumny:**

| Kolumna | Typ | Znaczenie | Przykład |
|---|---|---|---|
| `trial_id` | int | numer próby w bloku (trafia do znacznika `trial:start`) | `1` |
| `stimulus_id` | tekst | kod bodźca (trafia do `stim:onset`/`stim:offset`) | `BODZIEC_A` |
| `image_file` | tekst | ścieżka do obrazu względem `experiment/` | `stimuli/Bodziec A.PNG` |
| `block` | int | numer bloku | `1` |
| `condition` | tekst | kategoria obrazu (treść × barwa) – roboczy opis zespołu | `pejzaz_ciepla` |
| `stim_width` | int, px | szerokość wyświetlania = natywna szerokość pliku | `716` |
| `stim_height` | int, px | wysokość wyświetlania = natywna wysokość pliku | `476` |

- **Pełna zawartość pliku:**

```csv
trial_id,stimulus_id,image_file,block,condition,stim_width,stim_height
1,BODZIEC_A,stimuli/Bodziec A.PNG,1,pejzaz_ciepla,716,476
2,BODZIEC_B,stimuli/Bodziec B.PNG,1,pejzaz_zimna,715,477
3,BODZIEC_C,stimuli/Bodziec C.PNG,1,twarz_ciepla,594,476
4,BODZIEC_D,stimuli/Bodziec D.PNG,1,twarz_zimna,595,476
```

- **Zrzut:** — (pełna zawartość pliku powyżej).
- **Jak sprawdzić:** patrz 4.3.
- **Typowe problemy:** Excel przy zapisie potrafi zmienić separator na średnik i kodowanie – edytować w edytorze tekstu albo zapisać jako „CSV UTF-8 (rozdzielany przecinkami)”.

### Krok 4.2 – Bodźce · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** użyć oryginalnych obrazów z pakietu P3.
- **Gdzie:** `experiment/stimuli/Bodziec A.PNG` … `Bodziec D.PNG` – skopiowane 1:1 z folderu kursu „Pakiet P3 – materiały badań LBK” (slajd 8 protokołu). PNG RGBA: A 716×476, B 715×477, C 594×476, D 595×476 px.
- **Zasada:** materiały LBK tylko w **prywatnym** repozytorium. Jeśli repozytorium miałoby być publiczne – usunąć `experiment/stimuli/Bodziec*.PNG` i pobrać je z kursu do tego samego folderu.
- **Jak sprawdzić:** 4.3.

### Krok 4.3 – Kontrola spójności pliku warunków · wykonanie i opis: OS · 2026-11-08

- **Cel:** przed uruchomieniem sprawdzić, że każdy plik istnieje i ma rozmiar zgodny z CSV.
- **Polecenie** (wymaga Pillow: `py -3 -m pip install pillow` / `python3 -m pip install pillow`):

```bash
python3 -c "import csv;from PIL import Image;r=list(csv.DictReader(open('experiment/conditions/L1_LBK_4obrazy_test.csv',encoding='utf-8')));[print(x['trial_id'],x['image_file'],Image.open('experiment/'+x['image_file']).size==(int(x['stim_width']),int(x['stim_height']))) for x in r];print(len(r),'wierszy')"
```

  (Windows: zamienić `python3` na `py -3`.)
- **Jak sprawdzić:** 4 linie zakończone `True` i `4 wierszy`.

### Krok 4.4 – Wybór listy, kolejność, ziarno · wykonanie: DK · opis: OS · 2026-11-08

- **Stan KL-B:** jedna lista `L1_LBK_4obrazy_test`, kolejność **stała** A → B → C → D (`sequential`), **bez losowania i bez ziarna**. To kolejność techniczna, nie zatwierdzony plan badania.
- **Dlaczego nie więcej:** protokół (slajd 6) wspomina 30 prób, a w materiałach są 4 obrazy; liczby prób i kontrbalansowania nie ustalamy sami (pyt. 14.1). Prowadzący (e-mail) potwierdził, że w KL-B wystarcza jeden blok z oryginalnymi bodźcami.
- **Plan po decyzji LBK (M2):** pliki `L1…Ln` w `experiment/conditions/`, wybór listy w oknie startowym (pole `list` w *Experiment info*, Conditions = `$'conditions/' + expInfo['list'] + '.csv'`), skrypt generujący listy z zapisanym ziarnem w rozdziale 4.
- **Jak sprawdzić:** znacznik `exp:start` zawiera `list=L1_LBK_4obrazy_test`.

**Sprawdzenie rozdziału 4:** polecenie z 4.3 zwraca 4 × `True`; po przebiegu kolumna `stimulus_id` w CSV wyników ma kolejność BODZIEC_A, B, C, D.

---

## 5. Wzrok: MouseGaze i EyeLogic (KL-C)

**Co jest potwierdzone, a co nie:** MouseGaze – skonfigurowany i sprawdzony na komputerze testowym (sesje 2026-11-08). EyeLogic – **niepotwierdzony**, wymaga sesji w LBK (tabela w kroku 5.4).

### Krok 5.1 – Ustawienia MouseGaze · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** symulować wzrok myszą; w LBK zmienia się tylko urządzenie na EyeLogic.
- **Gdzie:** Builder → `experiment/P3_KL_C-2.psyexp` → *Experiment settings* → zakładka **Eyetracking**.
- **Ustawienia:** `Eyetracker device = MouseGaze`; `Move button = CONTINUOUS`; `Blink button = MIDDLE_BUTTON`; `Saccade threshold = 0.5`. Ekran: jednostki `pix`, okno 1920×1080, `Full-screen = False` (na stanowisku LBK włączyć – PsychoPy ostrzega `launchHubServer: If using the iohub mouse or eyetracker devices, fullScr should be True`).
- **Zrzut:** `docs/img/3-5-mousegaze.png`
- **Jak sprawdzić:** eksperyment startuje bez błędu; w `experiment/data/` powstaje plik `.hdf5` z próbkami pozycji kursora.

### Krok 5.2 – Zapis wzroku przez całą sesję · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** nagrywać wzrok od linii bazowej do końca sesji, a nie tylko w czasie obrazu.
- **Gdzie:** routine `baseline` – komponent `etRecord` (Eyetracker Record); routine `end` – komponent `etStop`.
- **Ustawienia:** `etRecord`: *Action type* = `Start Only`, start 0 s; `etStop`: *Action type* = `Stop Only`, start 0 s.
- **Jak sprawdzić:** próbki wzroku w pliku `.hdf5` obejmują czas od znacznika `calib:start` do `exp:end` (≈ 400 s).

### Krok 5.3 – Wskaźnik jakości wzroku i symulacja utraty śledzenia · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** w każdej sekundzie wiedzieć, czy wzrok z ostatnich 2 s nadaje się do analizy.
- **Gdzie:** Code Component `lsl_intro` → *Begin Experiment* (klasa `KLCPointerGaze`), `experiment/lsl_runtime.py` (metoda `sample_gaze`), `experiment/state_estimation.py` (`status_from_share`).
- **Jak działa:**
  - w każdej klatce (*Each Frame* każdej routine: `lbk.poll(tracker=klc_gaze_source)`) odczytywana jest pozycja kursora (`psychopy.event.Mouse`) i stan przycisków;
  - odczyt jest **ważny** (`status = 0`), gdy kursor jest wewnątrz okna (−960 ≤ x ≤ 960, −540 ≤ y ≤ 540 px) i żaden przycisk myszy nie jest wciśnięty; w przeciwnym razie `status = 2` (jak „mrugnięcie” w MouseGaze). Odczyt starszy niż 0,15 s też jest nieważny;
  - dlaczego nie `getLastSample()` z ioHub: poza aktywnym nagrywaniem MouseGaze zwraca `None`, więc jakość byłaby „utracona” mimo poprawnego kursora. `KLCPointerGaze` daje ciągły odczyt przez całą sesję. To **symulacja wzroku**, nie pomiar oka;
  - jakość = odsetek ważnych odczytów w oknie kroczącym **2 s** (przy 60 Hz ≈ 120 odczytów).
- **Progi (te same dla wzroku i EDA, kod: `status_from_share`):**

| Stan sygnału | Warunek | Uzasadnienie dla wzroku |
|---|---|---|
| `poprawny` | ≥ 90 % ważnych odczytów | dopuszcza ≈ 0,2 s braków na 2 s – pojedyncze mrugnięcie (100–400 ms) nie psuje okna |
| `zaszumiony` | 60 – < 90 % | 0,2–0,8 s braków: serie mrugnięć, chwilowe zgubienie – dane tylko z ostrożnością |
| `utracony` | < 60 % lub brak odczytów | ponad 0,8 s z 2 s bez śledzenia – okna nie interpretujemy |

- **Symulacja utraty śledzenia:** (a) przytrzymać dowolny przycisk myszy (np. środkowy = „mrugnięcie”) przez ≥ 2 s albo (b) wyprowadzić kursor poza okno PsychoPy na ≥ 2 s. W sesji clean wzrok był `utracony` przez 0,56 %, a `zaszumiony` przez 2,79 % analizowanego czasu.
- **Zrzut:** `docs/img/7-3-jakosc-gaze-eda.png` (konsola: `KL-C | GAZE poprawny 100% | EDA poprawny 100% | STAN …`).
- **Jak sprawdzić:** w konsoli Runnera po ok. 1 s od wciśnięcia przycisku pojawia się `GAZE zaszumiony …%`, po 2 s `GAZE utracony 0%`; po puszczeniu przycisku w ciągu 2 s wraca `poprawny`.
- **Typowe problemy:** brak środkowego przycisku na trackpadzie – użyć wariantu (b); okno PsychoPy musi być aktywne (na pierwszym planie).

### Krok 5.4 – EyeLogic w LBK: kalibracja i walidacja · odpowiedzialna osoba: OS · do wykonania na sesji w LBK

- **Cel:** zastąpić MouseGaze prawdziwym eye-trackerem bez zmian w pozostałej części eksperymentu.
- **Plan czynności w LBK:**
  1. *Tools → Plugins/Packages Manager* → wtyczka `psychopy-eyetracker-eyelogic`; uruchomić EyeLogic Server.
  2. *Experiment settings → Eyetracking* → urządzenie EyeLogic.
  3. Przed routine `baseline` dodać kalibrację i walidację (komponenty *Calibration*, *Validation* z panelu *Eyetracking*); wynik walidacji wysłać znacznikiem `calib:end|err_deg=…`.
  4. W `lsl_intro` (*Begin Experiment*) zamiast `klc_gaze_source = KLCPointerGaze(win)` przekazać obiekt eye-trackera ioHub (w skrypcie Buildera zmienna `eyetracker`) – `lsl_runtime.sample_gaze` korzysta wtedy z jego `getLastSample()` i statusu próbki.

| Element | MouseGaze (komputer testowy) | EyeLogic (LBK) |
|---|---|---|
| Urządzenie i wtyczka | MouseGaze, wbudowany w PsychoPy 2025.2.4 – **potwierdzone** | wersja wtyczki i EyeLogic Server – **do wpisania** |
| Częstotliwość odczytu | ≈ częstotliwość klatek (60 Hz) – **potwierdzone** | **do wpisania** |
| Kalibracja | nie dotyczy (kursor) | liczba i układ punktów – **do ustalenia z LBK** |
| Walidacja – kryterium akceptacji | nie dotyczy | **propozycja zespołu:** średni błąd ≤ 1,0°, maks. ≤ 1,5°; przy przekroczeniu – ponowna kalibracja (do potwierdzenia, pyt. 14.4) |
| Ważność próbki | kursor w oknie i brak przycisku | flaga ważności / status próbki z EyeLogic – **do sprawdzenia** |
| Okno i progi jakości | 2 s; 90 % / 60 % – **sprawdzone w teście** | te same, do weryfikacji na danych z EyeLogic |
| Strumień LSL wzroku | brak (MouseGaze nie publikuje LSL) | nazwa / typ / częstotliwość – **do odczytu w LabRecorder** |
| ROI/AOI | nieużywane w KL-C | współrzędne AOI z pakietu P3 – w kolejnych etapach |

- **Jak sprawdzić (w LBK):** walidacja mieści się w kryterium; konsola pokazuje `GAZE poprawny` przy patrzeniu na ekran i `GAZE utracony` po zamknięciu oczu na ≥ 2 s.

**Sprawdzenie rozdziału 5:** na komputerze testowym konsola pokazuje `GAZE poprawny 100%` przy kursorze w oknie i `GAZE utracony` po przytrzymaniu przycisku myszy ≥ 2 s; plik `.hdf5` obejmuje całą sesję. Część EyeLogic pozostaje otwarta do sesji w LBK.

## 6. LSL i GSR (KL-B)

**Architektura na własnym komputerze:** `symulator (TCP 127.0.0.1:5555, NDJSON 4 Hz)` → `lsl/sim_to_lsl.py` → strumień **LBK_Sim** → PsychoPy (odbiór, okno 5 s) + PsychoPy wysyła **LBK_Markers** → **LabRecorder** zapisuje oba do jednego XDF. W LBK zamiast symulatora i mostu jest strumień urządzenia GSR/EDA (krok 6.10).

### Krok 6.1 – Instalacja pylsl i LabRecorder · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** biblioteka LSL w dwóch środowiskach (Python terminalowy dla mostu i Python wbudowany w PsychoPy) oraz program do nagrywania.
- **Ustawienia / czynności:**
  1. **Python terminalowy (most, testy, wykres).** Windows: `py -3 -m pip install pylsl pyxdf matplotlib`. macOS (zalecane środowisko wirtualne):
     ```bash
     python3 -m venv .venv
     .venv/bin/python -m pip install pylsl -r overlay/requirements.txt
     ```
  2. **PsychoPy:** *Tools → Plugins/Packages Manager → zakładka Packages* → wpisać `pylsl` → *Install* → zrestartować PsychoPy. Sprawdzenie: Coder → *Shell* → `import pylsl; print(pylsl.__version__)`.
  3. **LabRecorder:** Windows – pobrać archiwum z https://github.com/labstreaminglayer/App-LabRecorder/releases, rozpakować, uruchomić `LabRecorder.exe`. macOS – `brew install labstreaminglayer/tap/labrecorder` (zainstalowano 1.18.0). Wersję wpisać do metryczki.
- **macOS + PsychoPy przez Rosetta (tylko Mac):** pylsl w PsychoPy (x86_64) potrzebuje universal `liblsl`. Zainstalowano `lsl.framework` w `/Library/Frameworks/` i uruchamiano PsychoPy z Terminala ze zmienną:
  ```bash
  PYLSL_LIB=/Library/Frameworks/lsl.framework/Versions/A/lsl /Applications/PsychoPy.app/Contents/MacOS/PsychoPy
  ```
  (`open -a` nie przekazuje zmiennych środowiskowych – trzeba uruchomić plik binarny jak wyżej.)
- **Jak sprawdzić:** `import pylsl` działa w obu środowiskach bez błędu; LabRecorder się otwiera.
- **Typowe problemy:** `RuntimeError: LSL binary library file was not found` – brak lub zła architektura `liblsl` (patrz wyżej). Menedżer pakietów PsychoPy na macOS zgłaszał `TypeError: NoneType`, mimo że pakiet był już dostępny – sprawdzać przez `import pylsl` w Shell.

### Krok 6.2 – Strumienie LSL · wykonanie: DK · opis: OS · 2026-11-08

| Strumień | Typ | Kanały | Format | Częstotliwość | source_id | Kto wysyła |
|---|---|---|---|---|---|---|
| `LBK_Sim` | `Physio` | 10 (tabela niżej) | float32 | 0 (nieregularny; faktycznie ~4 Hz) | `lbk-p3-sim-v1` | `lsl/sim_to_lsl.py` |
| `LBK_Markers` | `Markers` | 1 | string | 0 (nieregularny) | `lbk-p3-markers-v1` | PsychoPy (`lsl_runtime.py`) |
| GSR/EDA LBK | [do odczytu w LabRecorder w LBK] | | | | | urządzenie LBK |
| EyeLogic (jeśli jest) | [do odczytu w LBK] | | | | | EyeLogic Server |

**Kanały `LBK_Sim` (kolejność stała, zapisana też w metadanych strumienia):**

| # | Kanał | Jednostka | Uwagi |
|---|---|---|---|
| 0 | `hr` | bpm | |
| 1 | `eda_us` | µS | |
| 2 | `rr_ms` | ms | |
| 3 | `focus` | a.u. 0–1 | sztuczny wskaźnik symulatora |
| 4 | `quality` | kod | `0=ok`, `1=noisy`, `2=lost`, brak pola = `NaN` |
| 5–6 | `gaze_x`, `gaze_y` | px | symulator ich nie wysyła → zawsze `NaN` |
| 7 | `gaze_valid` | 0/1 | → `NaN` |
| 8 | `pupil_mm` | mm | → `NaN` |
| 9 | `resp` | a.u. | → `NaN` |

- **Znacznik czasu:** most nadaje każdej próbce `local_clock()` w chwili odebrania linii z TCP (pole `t` symulatora nie jest używane jako czas).
- **Jak sprawdzić:** LabRecorder → *Update* pokazuje `LBK_Sim (<nazwa komputera>)` i – po starcie PsychoPy – `LBK_Markers (<nazwa komputera>)`.

### Krok 6.3 – Słownik znaczników · wykonanie: DK · opis: OS · 2026-11-08

Format LBK: `kategoria:zdarzenie|klucz=wartość|…`

| Znacznik | Kiedy jest wysyłany | Gdzie w kodzie |
|---|---|---|
| `exp:start\|study=P3\|list=L1_LBK_4obrazy_test\|session=S001` | naciśnięcie spacji na ekranie instrukcji (początek części właściwej) | `lsl_intro`, End Routine |
| `trial:start\|trial=N` | początek routine `fixation` (N = `trial_id`) | `lsl_fix`, Begin Routine |
| `stim:onset\|stim=ID` | pierwsze odświeżenie ekranu z obrazem (`win.callOnFlip`) | `lsl_stim`, Begin Routine |
| `stim:offset\|stim=ID` | koniec routine `stimulus` | `lsl_stim`, End Routine |
| `resp\|q=SAM_AROUSAL_ROBOCZE\|key=K\|rt=S` | po naciśnięciu klawisza 1–9 (`rt` w sekundach, 3 miejsca) | `lsl_rating`, End Routine |
| `exp:end` | początek ekranu końcowego | `lsl_end`, Begin Routine |

Zarezerwowane na kolejne karty (nie są jeszcze wysyłane): `block:start|block=N`, `state:…`, `adaptation:…|rule=…`, `artifact:tracking_loss`, `calib:end|err_deg=…`.

- **Jak sprawdzić:** po wczytaniu XDF (6.8) lista znaczników zawiera wszystkie 6 typów w kolejności z tabeli; skrypt wykresu wypisze `UWAGA: brak wymaganych znacznikow`, jeśli któregoś z `exp:start, trial:start, stim:onset, resp, exp:end` brakuje.

### Krok 6.4 – Symulator i most `sim_to_lsl.py` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** publikować dane symulatora jako `LBK_Sim`.
- **Gdzie:** dwa osobne okna terminala (PowerShell / Terminal), oba w katalogu głównym repozytorium. Kolejność: **najpierw symulator, potem most, na końcu PsychoPy.**
- **Okno 1 – symulator** (zostawić otwarte):
  ```bash
  py -3 simulator/symulator_biosygnalow.py --mode tcp --scenario mix --port 5555        # Windows
  python3 simulator/symulator_biosygnalow.py --mode tcp --scenario mix --port 5555      # macOS
  ```
  Oczekiwane: `Czekam na klienta na 127.0.0.1:5555 ...`
- **Okno 2 – most** (zostawić otwarte):
  ```bash
  py -3 lsl/sim_to_lsl.py            # Windows
  .venv/bin/python lsl/sim_to_lsl.py # macOS
  ```
  Opcje: `--host 127.0.0.1 --port 5555` (domyślne).
- **Jak działa (najważniejsze w kodzie):**
  - czyta TCP linia po linii, każda linia to jeden obiekt JSON (`parse_line`);
  - dla każdego z 10 kanałów: brak pola, `null`, wartość nieliczbowa lub nieskończona → `NaN` (`number()`); `quality` tekstowe → kod 0/1/2, nieznane → `NaN`;
  - linia, która nie jest poprawnym JSON-em, jest **pomijana** z komunikatem `Pominieto niepoprawna linie` – most działa dalej;
  - po rozłączeniu TCP czeka 2 s i łączy się ponownie; strumień LSL pozostaje ten sam;
  - pole `scenario` jest ignorowane.
- **Zrzut:** `docs/img/6-1-bridge.png`
- **Jak sprawdzić:** w oknie 2 kolejno: `LSL: LBK_Sim (Physio), 10 kanalow; quality 0=ok 1=noisy 2=lost`, `Laczenie z symulatorem TCP 127.0.0.1:5555 ...`, `Polaczono z symulatorem 127.0.0.1:5555; publikuje LBK_Sim`.
- **Typowe problemy:** `Brak TCP / rozlaczenie … kolejna proba za 2 s` w kółko – symulator nie działa albo port jest inny. Symulator obsługuje **jednego** klienta: nie uruchamiać jednocześnie `klient_startowy.py`.

### Krok 6.5 – Test mostu na dwóch liniach · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** udowodnić, że brakujące pola dają `NaN`, a nie zatrzymanie programu.
- **Gdzie:** `tests/two_lines.jsonl`, `tests/test_bridge.py`.
- **Linie testowe:**
  ```json
  {"t":0,"hr":70,"eda_us":2.4,"rr_ms":850,"focus":0.6,"quality":"ok","gaze_x":400,"gaze_y":300,"gaze_valid":1,"pupil_mm":3.1,"resp":0.4}
  {"t":0.25,"hr":74,"eda_us":null,"rr_ms":810,"focus":0.5,"quality":"lost"}
  ```
  Linia 1 ma pola wzroku i oddechu; linia 2 ich nie ma, a `eda_us` = `null`.
- **Polecenie:** `py -3 tests/test_bridge.py` / `python3 tests/test_bridge.py` (nie wymaga pylsl).
- **Zrzut:** `docs/img/6-2-test.png`
- **Jak sprawdzić:** `OK: 2 linie, brakujace pola = NaN, quality zakodowane poprawnie`. Test sprawdza: linia 1 → 10 liczb, `quality=0`, `gaze_x=400`, `pupil_mm=3.1`, `resp=0.4`; linia 2 → `hr=74`, `quality=2`, kanały 5–9 = `NaN`.

### Krok 6.6 – Odbiór w PsychoPy i cechy w oknie 5 s · wykonanie: DK, poprawka RMSSD: OS · opis: OS · 2026-11-08

- **Cel:** w trakcie eksperymentu liczyć podstawowe cechy, bez blokowania klatek i bez pokazywania ich uczestnikowi.
- **Gdzie:** `experiment/lsl_runtime.py` (`poll`, `calculate_features`), wywoływane w Each Frame każdej routine (krok 3.4–3.10).
- **Ustawienia:**
  - odbiór: `pull_chunk(timeout=0.0, max_samples=128)` w każdej klatce (przy 60 Hz co 16,7 ms) – `timeout=0.0` oznacza „weź to, co już przyszło, nie czekaj”;
  - okno: próbki z ostatnich **5,0 s** czasu LSL; raport: co **1,0 s** przez `print` → konsola Runnera (eksperymentator), nie ekran;
  - **odrzucanie:** próbka liczy się tylko, gdy `quality == 0` (ok). `noisy`, `lost` i brak `quality` (`NaN`) są pomijane i liczone: `bad_window` (w bieżącym oknie) i `bad_total` (od początku);
  - `NaN` w poszczególnych kanałach poprawnej próbki są pomijane.
- **Wzory:**
  - `HR [bpm] = mean(hr)`
  - `RMSSD [ms] = sqrt( mean( (RR[i+1] − RR[i])² ) )` – różnice **tylko między sąsiednimi poprawnymi próbkami**; próbka odrzucona przerywa ciąg (nie liczymy różnicy „ponad” artefaktem). Mniej niż 2 kolejne RR → `NA`.
  - `EDA [µS] = median(eda_us)`
- **Jak sprawdzić:**
  1. Test: `py -3 tests/test_features.py` / `python3 tests/test_features.py` → `OK: HR, RMSSD z sasiednich roznic RR, mediana EDA, odrzucenie noisy/lost/NaN`. Test zawiera przypadek z artefaktem: RR 800, 820, 790, *noisy*, *lost*, 760, 780 → różnice 20, −30, 20 → RMSSD = 23,8 ms.
  2. Na żywo (eksperyment + most): w konsoli co ok. 1 s np. `5s | HR= 71.03 bpm | RMSSD= 48.00 ms | EDA med= 2.43 uS | valid= 18 bad_window= 2 bad_total= 3`. Przy 4 Hz `valid + bad_window` ≈ 20.
- **Zrzut:** — (przykładowa linia konsoli w „Jak sprawdzić”).
- **Ograniczenie:** RR z symulatora to wartości syntetyczne (1 RR na próbkę 4 Hz, a nie na uderzenie serca) – RMSSD sprawdza poprawność obliczeń, nie jest fizjologiczną miarą HRV.

### Krok 6.7 – Nagranie 2 min w LabRecorder · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** zapisać `LBK_Sim` i `LBK_Markers` w jednym pliku XDF na wspólnej osi czasu.
- **Kolejność (ważna – inaczej `exp:start` nie trafi do pliku):**
  1. Uruchomić symulator i most (6.4).
  2. Uruchomić eksperyment w PsychoPy, wpisać `participant = TEST-01`, `session = S001`. **Zatrzymać się na ekranie instrukcji – nie naciskać spacji.** (Strumień `LBK_Markers` powstaje dopiero przy starcie eksperymentu.)
  3. W LabRecorder: *Update* → zaznaczyć `LBK_Sim` i `LBK_Markers`. Study Root: `<repozytorium>/sample_data`; File Name/Template: `P3_KL-B_TEST-01_S001.xdf`. Kliknąć **Start**.
  4. Odczekać ok. 70 s na ekranie instrukcji (blok trwa tylko ok. 22 s + odpowiedź, a nagranie musi mieć ≥ 120 s; czasów bodźców nie zmieniamy).
  5. Nacisnąć spację → 4 obrazy → odpowiedź 1–9 → ekran końcowy.
  6. Zatrzymać nagranie (**Stop**), gdy od Start minęło ≥ 125 s.
- **Zasady:** w `sample_data/` wyłącznie nagrania z symulatora i MouseGaze; nigdy nagrania z aparatury LBK. Tylko pseudonim.
- **Zrzut:** `docs/img/6-5-labrecorder.png`
- **Jak sprawdzić:** LabRecorder pokazuje oba strumienie zaznaczone na zielono; po Stop w `sample_data/` jest plik `.xdf` (ok. 35–40 kB na 2 min).
- **Typowe problemy:** brak `LBK_Markers` na liście – PsychoPy jeszcze nie wystartował albo trzeba kliknąć *Update*. Zaznaczenie strumieni i Start **po** spacji → w pliku brak `exp:start` (tak było w nagraniu z 2026-11-08, wersja z `exp:start` w Begin Routine – rozdz. 15).

### Krok 6.8 – Wczytanie XDF i wykres EDA ze znacznikami · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** dowód wspólnej osi czasu.
- **Polecenie:**
  ```bash
  py -3 overlay/plot_xdf.py sample_data/P3_KL-B_TEST-01_S001.xdf --out docs/img/eda_markery.png              # Windows
  .venv/bin/python overlay/plot_xdf.py sample_data/P3_KL-B_TEST-01_S001.xdf --out docs/img/eda_markery.png   # macOS
  ```
- **Co robi skrypt:** `pyxdf.load_xdf` → wybiera strumienie po nazwie → kanał `eda_us` po etykiecie z metadanych → próbki `quality ≠ ok` jako przerwy w linii → pionowe linie dla wszystkich znaczników (kolor wg kategorii) → wypisuje listę znaczników z czasem i ostrzeżenia (brak wymaganych znaczników, nagranie < 120 s).
- **Zrzut / wynik:** `docs/img/eda_markery.png`
- **Jak sprawdzić:** w konsoli `strumienie: ['LBK_Sim', 'LBK_Markers']`, `LBK_Sim: ~500 probek, ≥120 s`, lista 15 znaczników (`exp:start`, 4 × 3 dla prób, `resp`, `exp:end`) i **brak** linii `UWAGA`. Na wykresie: linia EDA przez ≥ 120 s, czerwone przerywane linie `stim:onset` co ok. 5,5 s, czarne linie `exp:start` i `exp:end`.
- **Wynik nagrania z 2026-11-08 (wersja przed poprawką `exp:start`):** `LBK_Sim` 504 próbki, 125,8 s (488 ok, 9 noisy, 7 lost); `LBK_Markers` 14 znaczników; skrypt zgłasza `UWAGA: brak wymaganych znacznikow: exp:start`. **Nagranie należy powtórzyć według 6.7** i podmienić plik oraz wykres.

### Krok 6.9 – Schemat pętli biofeedbacku · schemat: DK, OS · opis: OS · 2026-11-08

- **Cel:** pokazać drogę sygnału i miejsca opóźnień.
- **Gdzie:** `docs/img/petla_biofeedback.png` (generowany skryptem `docs/petla_biofeedback.py`: `python3 docs/petla_biofeedback.py`), wersja tekstowa `docs/PETLA_BIOFEEDBACK.mmd` (Mermaid).
- **Treść:** bodziec → uczestnik → czujnik → most/LSL → PsychoPy (odbiór) → okno 5 s → decyzja → zmiana (tylko między próbami) → następny bodziec. Opóźnienia Δ1–Δ8: percepcja ~0,1–0,3 s; latencja odpowiedzi EDA ~1–3 s; próbkowanie 4 Hz ≤ 250 ms; LSL lokalnie < 10 ms; odbiór ≤ 1 klatka (16,7 ms); okno 5 s (średnia opóźniona ~2,5 s) i raport co 1 s; czekanie na koniec obrazu do 5 s.
- **Wniosek dla P3:** łączne opóźnienie to kilka sekund, więc adaptacja może zadziałać dopiero w przerwie po szarym ekranie – zgodnie z zasadą nienaruszalności (nie zmieniamy 4000 ms obrazu, 1000 ms szarości ani kolejności).
- **Jak sprawdzić:** schemat zawiera wszystkie 7 elementów z polecenia i zamyka się strzałką do bodźca.

### Krok 6.10 – Urządzenie GSR/EDA w LBK · odpowiedzialna osoba: OS · do uzupełnienia na sesji w LBK

- **Cel:** zamienić symulator i most na strumień z aparatury.
- **Do wpisania po sesji:** nazwa i typ strumienia (z LabRecorder), liczba kanałów, częstotliwość, jednostki, wersja sterownika, nazwa komputera. W `lsl_runtime.py` zmienić nazwę wyszukiwanego strumienia z `LBK_Sim` na odczytaną nazwę (oraz indeksy kanałów, jeśli inne).
- **Jak sprawdzić:** w LabRecorder w LBK widać strumień GSR i `LBK_Markers`; konsola PsychoPy pokazuje `… polaczony`.

**Sprawdzenie rozdziału 6 (jak poznać, że działa):** `tests/test_bridge.py` i `tests/test_features.py` → `OK`; w LabRecorder widać 2 strumienie: `LBK_Sim` i `LBK_Markers`; skrypt z 6.8 wypisuje oba strumienie, ≥ 120 s, 15 znaczników i brak ostrzeżeń.

**Karta źródeł** (dokumentacje i wnioski dla kodu): `docs/KARTA_ZRODEL.md`.

---

## 7. Jakość sygnału i stan uczestnika (KL-C)

**Wynik rozdziału:** w trakcie eksperymentu co 1 s liczony jest stan sygnałów (wzrok, EDA: `poprawny / zaszumiony / utracony`) i stan uczestnika względem jego linii bazowej (`spoczynkowy / pobudzenie_podwyzszone / zaangazowanie_wzrokowe / nieznany`), z histerezą 6 s i znacznikiem `state:…` przy każdej zmianie. Wszystko widzi tylko eksperymentator (konsola + plik statusu). Kod: `experiment/state_estimation.py` (logika, bez PsychoPy i LSL – testowalna) i `experiment/lsl_runtime.py` (połączenie z PsychoPy/LSL).

### Krok 7.1 – Zmiany w eksperymencie względem KL-B · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** dodać spoczynek do kalibracji linii bazowej i wydłużyć sesję do ≥ 360 s bez zmiany czasów bodźców.
- **Gdzie:** `experiment/P3_KL_C-2.psyexp` (rozbudowana kopia eksperymentu z rozdz. 3).
- **Flow:** `intro` → **`baseline`** (krzyż, 30 s) → pętla `trials` (`fixation` 0,5 s → `stimulus` 4 s → `gray` 1 s; 4 obrazy A–D) → `rating` → **`monitoring`** (ekran techniczny, 340 s) → `end`.
- **Nowe / zmienione Code Components:**

| Routine | Komponent | Kod (skrót) |
|---|---|---|
| `intro` | `lsl_intro` | *Begin Experiment*: klasa `KLCPointerGaze` (krok 5.3), `lbk = LBKMonitor(participant=expInfo['participant'])`; *Each Frame*: `lbk.poll(tracker=klc_gaze_source)`; *End Routine*: `exp:start|study=P3|list=L1_LBK_4obrazy_test|stage=KL-C` |
| `baseline` | `lsl_baseline` | *Begin Routine*: `lbk.start_baseline()` → znacznik `calib:start|phase=rest30`; *End Routine*: `lbk.finish_baseline()` → `calib:end|phase=rest30|accepted=N` |
| `monitoring` | `lsl_monitoring` | `block:start|block=monitoring_klc` / `block:end|block=monitoring_klc` |
| wszystkie | `lsl_*` | *Each Frame*: `lbk.poll(tracker=klc_gaze_source)` |
| `end` | `lsl_end` | `exp:end`; *End Experiment*: `lbk.close()` (zamknięcie pliku statusu) |

- **Most LSL:** `lsl/sim_to_lsl.py` w KL-C publikuje **12 kanałów** – 10 z rozdz. 6.2 oraz `seq` (indeks 10) i `t` (indeks 11) symulatora, potrzebne wyłącznie do oceny po sesji. Pole `scenario` **nie** jest wysyłane.
- **Uwaga:** routines `baseline` i `monitoring` są techniczne (KL-C), nie są częścią zatwierdzonego protokołu P3. Teksty instrukcji i nazwa pliku danych w `P3_KL_C-2.psyexp` pochodzą z wersji sprzed poprawek z rozdz. 3 (dosłowne `\n` w tekście, plik `data/<kod>_<data>`) – do ujednolicenia w KL-D.
- **Zrzut:** `docs/img/7-1-flow-klc.png`
- **Jak sprawdzić:** Flow zawiera 8 routines w kolejności jak wyżej; `baseline` trwa 30 s, `monitoring` 340 s.

### Krok 7.2 – Uruchomienie sesji (clean / noisy) · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** nagrać 2 sesje ≥ 360 s przy działającym eksperymencie.
- **Kolejność (ważna):**
  1. Zamknąć stare okna symulatora i mostu (Ctrl+C).
  2. Okno 1 – symulator (**uruchomić od nowa przed każdą sesją**, patrz „Typowe problemy”):
     ```bash
     python3 simulator/symulator_biosygnalow.py --mode tcp --scenario mix --noise 0 --dropout 0 --seed 1       # clean
     python3 simulator/symulator_biosygnalow.py --mode tcp --scenario mix --noise 0.6 --dropout 0.4 --seed 1   # noisy
     ```
     (Windows: `py -3` zamiast `python3`; macOS z `.venv`: `.venv/bin/python`.)
  3. Okno 2 – most: `python3 lsl/sim_to_lsl.py` → oczekiwane `LSL: LBK_Sim (Physio), 12 kanalow; …`.
  4. PsychoPy → `experiment/P3_KL_C-2.psyexp` → Run → `participant = TEST-01` → zatrzymać się na ekranie instrukcji.
  5. LabRecorder → *Update* → zaznaczyć `LBK_Sim` i `LBK_Markers` → nazwa pliku → **Start**.
  6. Od razu nacisnąć spację (baseline musi wypaść w pierwszych 40 s symulatora – faza `spokoj` scenariusza `mix`).
  7. Przejść blok A–D, odpowiedzieć 1–9, zostawić `monitoring` do końca; **Stop** w LabRecorder po `exp:end`.
- **Pliki wynikowe (2026-11-08):**

| Sesja | XDF | Plik statusu | Długość XDF |
|---|---|---|---|
| clean | `sample_data/P3_KL-C_clean_fixed_1.xdf` | `sample_data/KL-C_STATUS_TEST-06_20261108_213754.csv` | 427,3 s |
| noisy | `sample_data/P3_KL-C_noisy_360s.xdf` | `sample_data/KL-C_STATUS_TEST-01_20261108_215324.csv` | 411,0 s |

- **Zrzut:** `docs/img/7-2-labrecorder-konfiguracja.png`
- **Jak sprawdzić:** XDF zawiera `LBK_Sim` (12 kanałów, ≥ 360 s) i `LBK_Markers` ze znacznikami `exp:start`, `calib:start`, `calib:end`, 4 × próba, `resp`, `block:start/end`, `exp:end`.
- **Typowe problemy:** jeśli most pokazuje `10 kanalow` – działa stary most z KL-B. **Symulator uruchomiony dużo wcześniej niż sesja** → baseline nie wypada w spoczynku (tak było 2026-11-08 – krok 7.9). Kontrola: kolumna `sim_t` w pliku statusu w chwili `calib:start` powinna być < 10 s.

### Krok 7.3 – Odrzucanie braków, artefaktów i wartości nierealnych · wykonanie: DK · opis: OS · 2026-11-08

- **Gdzie:** `state_estimation.valid_physio(sample)`.
- **Próbka fizjologiczna jest przyjmowana tylko, gdy jednocześnie:** `quality = ok` (kod 0); `35 ≤ HR ≤ 200 bpm`; `EDA > 0 µS`; `300 ≤ RR ≤ 2000 ms`; wszystkie te wartości są liczbami skończonymi (nie `NaN`).
- Próbki odrzucone nie wchodzą do linii bazowej ani do klasyfikacji, ale **liczą się** do wskaźnika jakości (jako złe) i do licznika `bad_total` w konsoli.
- **Jak sprawdzić:** `python3 tests/test_klc.py` → `Ran 5 tests … OK` (test `test_reject_artifacts`: HR 250 i 34, EDA 0 i −1, quality 1 i 2, HR `NaN` → odrzucone).

### Krok 7.4 – Wskaźnik jakości EDA · wykonanie: DK · opis: OS · 2026-11-08

- **Gdzie:** `StateEstimator.evaluate()` – co 1 s.
- **Ustawienia:** odsetek próbek przyjętych (krok 7.3) w oknie kroczącym **5 s** (przy 4 Hz ≈ 20 próbek); progi jak dla wzroku (krok 5.3): `poprawny` ≥ 90 % (≤ 2 złe próbki na 20), `zaszumiony` 60–90 %, `utracony` < 60 % lub puste okno.
- **Uzasadnienie:** 5 s odpowiada oknu cech z KL-B; przy ≥ 12 dobrych próbkach mediana jest jeszcze stabilna, poniżej 60 % okno jest zdominowane przez artefakty.
- **Jak sprawdzić:** w sesji noisy (`--noise 0.6 --dropout 0.4`) konsola pokazuje przeważnie `EDA zaszumiony 75–85%`; w sesji clean – `EDA poprawny 100%`.

### Krok 7.5 – Linia bazowa · wykonanie: DK · opis: OS · 2026-11-08

- **Gdzie:** routine `baseline` (30 s) → `start_baseline()` / `finish_baseline()`.
- **Ustawienia:** mediana HR [bpm] i mediana EDA [µS] z przyjętych próbek w oknie 30 s od znacznika `calib:start`. Wymagane **≥ 40** przyjętych próbek (10 s danych przy 4 Hz); przy mniejszej liczbie linia bazowa = `NaN`, a stan pozostaje `nieznany`.
- **Dlaczego 30 s na początku:** protokół P3 nie przewiduje osobnego okresu spoczynkowego (pyt. 14.8), więc zgodnie z kartą używamy pierwszych 30 s; mediana jest odporna na pojedyncze odpowiedzi fazowe EDA.
- **Jak sprawdzić:** po 30 s w konsoli `KL-C BASELINE: HR= … EDA= … valid= N` oraz znacznik `calib:end|phase=rest30|accepted=N` (clean: N = 120, noisy: N = 96).

### Krok 7.6 – Stany uczestnika względem linii bazowej · wykonanie: DK · opis: OS · 2026-11-08

- **Gdzie:** `StateEstimator.classify()`; wejście: mediany HR, EDA i `focus` z przyjętych próbek w oknie 5 s.
- **Reguły (w tej kolejności):**

| Stan | Warunek | Uzasadnienie |
|---|---|---|
| `nieznany` | brak linii bazowej, EDA ≠ `poprawny`, wzrok `utracony` albo brak wartości | nie zgadujemy przy złym sygnale |
| `pobudzenie_podwyzszone` | EDA − baza ≥ **1,2 µS** **i** HR − baza ≥ **7 bpm** | koniunkcja dwóch sygnałów ogranicza fałszywe alarmy od pojedynczej odpowiedzi EDA lub ruchu |
| `zaangazowanie_wzrokowe` (stan specyficzny P3) | wzrok `poprawny`, `focus` ≥ **0,67**, EDA − baza < 1,2 µS | P3 bada swobodne oglądanie obrazów – istotne, czy osoba „jest przy obrazie” bez silnego pobudzenia |
| `spoczynkowy` | \|EDA − baza\| ≤ **0,55 µS** i \|HR − baza\| ≤ **9 bpm** | wartości bliskie własnej linii bazowej |
| `nieznany` | żaden z powyższych | stan pośredni |

- **Ograniczenie:** `focus` to sztuczny wskaźnik symulatora. W LBK stan `zaangazowanie_wzrokowe` trzeba oprzeć na danych wzroku (np. odsetek czasu w AOI obrazu) – do ustalenia z LBK.
- **Jak sprawdzić:** `tests/test_klc.py`, test `test_state_uses_baseline_not_scenario`.

### Krok 7.7 – Histereza i znaczniki stanu · wykonanie: DK · opis: OS · 2026-11-08

- **Gdzie:** `StateEstimator.advance()`; znacznik w `LBKMonitor.poll()`.
- **Reguła:** nowy stan jest przyjmowany dopiero, gdy ta sama decyzja („kandydat”) utrzymuje się przez **≥ 6 s** czasu LSL (decyzja co 1 s → co najmniej 6 kolejnych zgodnych decyzji). Inna decyzja w międzyczasie zeruje odliczanie.
- **Znaczniki:** po każdej zatwierdzonej zmianie do `LBK_Markers` trafia `state:spoczynkowy`, `state:pobudzenie_podwyzszone`, `state:zaangazowanie_wzrokowe` albo `state:nieznany`.
- **Jak sprawdzić:** `tests/test_klc.py`, test `test_hysteresis_real_six_seconds` (zmiana dopiero przy 6,00 s, nie przy 5,99 s); w XDF clean 9 znaczników `state:*` w 427 s – brak „migotania” (najkrótszy odstęp między zmianami: 7,0 s).

### Krok 7.8 – Widok eksperymentatora i zasada nienaruszalności · wykonanie: DK · opis: OS · 2026-11-08

- **Gdzie wyświetlany jest stan:**
  1. **konsola Runnera** co 1 s: `KL-C | GAZE poprawny 100% | EDA poprawny 100% | STAN spoczynkowy | odrzucone 0`;
  2. **plik statusu** `sample_data/KL-C_STATUS_<kod>_<RRRRMMDD_GGMMSS>.csv` – wiersz co 1 s: `t_lsl, t_rel, seq, sim_t, gaze_pct, gaze_quality, eda_pct, eda_quality, state, candidate, baseline_eda, baseline_hr, eda_med_us, hr_med_bpm, focus_med, bad_total`;
  3. znaczniki `state:*` w XDF.
- **Nigdy na ekranie uczestnika.** Uzasadnienie (zasada nienaruszalności badania): informacja o własnym „pobudzeniu” lub „utracie śledzenia” zmieniłaby zachowanie uczestnika (reakcja na komunikat, zmiana sposobu patrzenia) i tym samym mierzone zmienne P3; obraz ma być widoczny dokładnie 4000 ms, szary ekran 1000 ms, w ustalonej kolejności – warstwa jakości/stanu niczego z tego nie zmienia.
- **Zrzuty:** `docs/img/7-3-jakosc-gaze-eda.png`, `docs/img/7-4-rozpoznany-stan.png` (`STAN pobudzenie_podwyzszone`).
- **Jak sprawdzić:** w oknie uczestnika widać tylko instrukcję, krzyż, obrazy, szary ekran, pytanie i ekran techniczny; w XDF odstępy `stim:onset` → `stim:offset` ≈ 4 s jak w KL-B.

### Krok 7.9 – Ewaluacja obu nagrań · wykonanie: DK · analiza i opis: OS · 2026-11-08

- **Cel:** porównać stany z polem `scenario` symulatora (**tylko do oceny**, nigdy w eksperymencie).
- **Dane odniesienia:** `sample_data/ground_truth_clean_extended.jsonl` i `ground_truth_noisy.jsonl` – ten sam symulator w trybie `file` z tym samym ziarnem (`--seed 1`), łączone z nagraniem po `seq`. Mapowanie: `spokoj → spoczynkowy`, `stres → pobudzenie_podwyzszone`, `skupienie → zaangazowanie_wzrokowe`, `zmeczenie → nieznany`. Zgodność danych odniesienia z nagraniem sprawdzono: HR i EDA 1710/1710 próbek (clean) zgodne.
- **Komendy (z katalogu głównego; wymaga `pyxdf`):**
  ```bash
  python3 analysis/evaluate_klc.py --label clean --xdf sample_data/P3_KL-C_clean_fixed_1.xdf --status sample_data/KL-C_STATUS_TEST-06_20261108_213754.csv --truth sample_data/ground_truth_clean_extended.jsonl
  python3 analysis/evaluate_klc.py --label noisy --xdf sample_data/P3_KL-C_noisy_360s.xdf --status sample_data/KL-C_STATUS_TEST-01_20261108_215324.csv --truth sample_data/ground_truth_noisy.jsonl
  python3 analysis/compare_both.py
  ```
  Wynik: `reports/wyniki_clean.csv|md`, `reports/wyniki_noisy.csv|md`, `reports/tabela_klc.csv`. Zakres: pierwsze 360 s `LBK_Sim`; zgodność liczona po zakończeniu linii bazowej.
- **Tabela wyników:**

| Wskaźnik | clean | noisy |
|---|---:|---:|
| Zgodność stanów ze `scenario` | **39,57 %** | **18,40 %** |
| Zgodność, gdy wzrok i EDA `poprawny` | 40,13 % | 6,85 % |
| Liczba zmian stanu (360 s) | **7** | **0** |
| Znaczniki `state:*` w całym XDF | 9 | 0 |
| Wzrok – `poprawny` / `zaszumiony` / `utracony` (% czasu) | 96,65 / 2,79 / 0,56 | 98,04 / 1,96 / 0,00 |
| EDA – `poprawny` / `zaszumiony` / `utracony` (% czasu) | 100,00 / 0,00 / 0,00 | 23,46 / 75,42 / 1,12 |
| Czas w stanie: spoczynkowy / pobudzenie / zaangażowanie / nieznany (%) | 8,3 / 30,7 / 5,5 / 55,5 | 0 / 0 / 0 / 100 |
| Linia bazowa HR / EDA | 75,0 bpm / 3,39 µS | 87,1 bpm / 5,63 µS |
| Porównane punkty statusu | 326 | 326 |

Czas w stanach policzono z kolumny `state` plików statusu (te same 326 punktów po linii bazowej).

- **Wykresy:** `docs/img/7-5-wykres-jakosci.png` (jakość z tabeli), `docs/img/7-6-eda-clean.png`, `docs/img/7-7-eda-noisy.png` (EDA + znaczniki z XDF).
- **Jak sprawdzić:** komendy wypisują `XDF: 427.3 s, wybrany zakres 360.0 s, markery state: 9` (clean) i `XDF: 411.0 s, … markery state: 0` (noisy); `reports/tabela_klc.csv` zawiera wartości z tabeli.

### Krok 7.10 – Analiza: problem → analiza → warianty → wybór → efekt · opis: OS · 2026-11-09

Pełna sekcja analityczna: `docs/KL-C_ANALIZA.md`. Najważniejsze wnioski:

1. **Linia bazowa nie wypadła w spoczynku.** Kolumna `sim_t` w plikach statusu pokazuje, że w chwili `calib:start` symulator działał już ok. **1487 s** (clean) i **72 s** (noisy). Scenariusz `mix` ma cykl 180 s (spokój 40 s → skupienie 40 s → stres 40 s → spokój 30 s → zmęczenie 30 s), więc baseline clean wypadł w fazie `skupienie`, a noisy na przełomie `skupienie`/`stres` (stąd wysokie bazy: EDA 3,39 i 5,63 µS). Większość niskiej zgodności wynika z tego, a nie z samych reguł.
2. **Opóźnienie decyzji.** EDA w symulatorze dochodzi do nowego poziomu ze stałą czasową ~8 s, do tego okno 5 s i histereza 6 s – stan zmienia się ok. 10–20 s po zmianie fazy; przy fazach 30–40 s ogranicza to maksymalną zgodność „sekunda w sekundę”.
3. **Sesja noisy:** przy 75 % czasu EDA `zaszumiony` reguła „klasyfikuj tylko przy `poprawny`” daje stały stan `nieznany` (0 zmian). To zachowanie zachowawcze – bez fałszywych alarmów, ale też bez informacji.
4. **Co dalej (KL-D):** powtórzyć obie sesje z symulatorem uruchomionym tuż przed sesją (krok 7.2), rozważyć klasyfikację z przyjętych próbek także przy jakości `zaszumiony` oraz progi jako stosunek do linii bazowej.

**Sprawdzenie rozdziału 7:** `python3 tests/test_klc.py` → `OK`; komendy z kroku 7.9 odtwarzają `reports/tabela_klc.csv` z wartościami jak w tabeli; w XDF clean są znaczniki `calib:start`, `calib:end` i 9 × `state:*`.

## 14. Odstępstwa i pytania do LBK

Zasada: niespójności zgłaszamy w forum „Pytania do projektu”, decyzję prowadzącego wpisujemy tutaj z datą.

### 14.1 – Liczba prób i kontrbalansowanie · DK · 2026-10-12 · otwarte
Slajd 6 protokołu: 30 prób; w materiałach 4 obrazy A–D. Ile prób, ile powtórzeń obrazu i jaka kolejność / kontrbalansowanie?
**Decyzja częściowa (e-mail prowadzącego, 2026-11-08):** w KL-B wystarczy jeden blok z oryginalnymi bodźcami; liczbę prób i kontrbalansowanie potwierdzić. **Decyzja końcowa:** [brak].

### 14.2 – Powrót EDA do linii bazowej · OS · 2026-10-12 · otwarte
Jak wyznaczać linię bazową EDA, jaki próg „powrotu” i jaki maksymalny czas czekania przed kolejnym bodźcem? **Decyzja:** [brak].

### 14.3 – Utrata śledzenia wzroku · DK · 2026-10-12 · otwarte
Jaki czas utraty sygnału ma wywoływać pauzę? Czy pauza wyłącznie między próbami (żeby zachować 4000 ms)? **Decyzja:** [brak].

### 14.4 – Aparatura i synchronizacja · OS · 2026-10-12 · otwarte
Nazwy, typy i częstotliwości strumieni LSL dla GSR/EDA i EyeLogic na stanowisku; wymagania kalibracji. **Decyzja:** [brak].

### 14.5 – Wersja PsychoPy · DK · 2026-10-12 · otwarte
Instalator 2025.2.4, aplikacja pokazuje „2025.2.4beta”. Jaka wspólna wersja na stanowisku LBK? **Decyzja:** [brak].

### 14.6 – Krzyż fiksacyjny i ankieta SAM · DK · 2026-11-08 · otwarte
Opis P3: obraz 4000 ms → szary ekran 1000 ms; protokół nie wspomina krzyża. W szkielecie jest roboczy krzyż 500 ms. Ocena: w szkielecie jedna skala pobudzenia 1–9 **po bloku**; slajd 13 – SAM (walencja, pobudzenie, dominacja). Czy krzyż ma zostać? Czy SAM po każdym obrazie, czy po bloku? **Decyzja:** [brak].

### 14.7 – Rozdzielczość i monitor · DK · 2026-11-08 · otwarte
1920×1080 px przyjęto roboczo (protokół P3 nie podaje rozdzielczości dla obrazów 594–716 px szerokości). Jaki monitor, odświeżanie i odległość w LBK? **Decyzja:** [brak].

---
### 14.8 – Okres spoczynkowy do linii bazowej · OS · 2026-11-09 · otwarte
Protokół P3 nie przewiduje osobnego okresu spoczynkowego; w KL-C linię bazową liczymy z technicznej routine `baseline` (30 s krzyża po instrukcji). Czy LBK akceptuje 30 s spoczynku na początku sesji, czy woli inny okres (np. dłuższy, przed blokiem)? **Decyzja:** [brak].

### 14.9 – Stan specyficzny dla P3 · DK · 2026-11-09 · otwarte
Jako stan specyficzny przyjęliśmy `zaangazowanie_wzrokowe` (obecnie z sztucznego wskaźnika `focus` symulatora). Jaką miarę wzroku z EyeLogic przyjąć w LBK (np. odsetek czasu w AOI obrazu, czas fiksacji)? **Decyzja:** [brak].

## 15. Dziennik zmian

| Data | Kto | Co | Dlaczego |
|---|---|---|---|
| 2026-10-12 | DK | Instalacja PsychoPy, demo, symulator (rozdz. 1) | KL-A |
| 2026-11-08 | DK | Szkielet P3: `.psyexp`, bodźce A–D, plik warunków, `sim_to_lsl.py`, `lsl_runtime.py`, testy | KL-B |
| 2026-11-08 | DK | Uruchomienie z MouseGaze; pylsl/liblsl, LabRecorder 1.18.0; nagranie XDF (125,8 s, 14 znaczników, brak `exp:start`); wykres | KL-B – wspólna oś czasu |
| 2026-11-08 | OS | **Przegląd i poprawki:** (1) `exp:start` przeniesiony z Begin Routine na End Routine `intro` (po spacji) – wcześniej był wysyłany zanim LabRecorder mógł zasubskrybować `LBK_Markers`; (2) teksty instrukcji/pytania: zamiast dosłownych `\n` prawdziwe nowe linie, polskie znaki; (3) nazwa pliku danych wg konwencji LBK `P3_glowne_{kod}_{sesja}_{RRRR-MM-DD_GGMM}`, sesja `S001`; (4) RMSSD tylko z sąsiednich poprawnych RR + rozszerzony test; (5) ponowne łączenie z `LBK_Sim` przez nieblokujący `ContinuousResolver`; `summary()` na końcu; (6) most wypisuje potwierdzenie połączenia TCP; (7) wykres pomija próbki `quality ≠ ok`, pokazuje wszystkie znaczniki i sprawdza wymagane; (8) nowy schemat pętli z zamkniętą pętlą i Δ1–Δ8; (9) usunięto nieużywane pliki (DEMO, szablony, notatki robocze); (10) przepisane rozdz. 3, 4, 6 | Kryteria KL-B: wymagany `exp:start`, poprawny RMSSD, dane wyjściowe, odtwarzalność |
| 2026-11-08 | DK | KL-C: `state_estimation.py` (filtr, okna jakości 2 s / 5 s, linia bazowa, stany, histereza 6 s), `lsl_runtime.py` (konsola, plik statusu, znaczniki `state:*`), most z kanałami `seq`/`t`, `P3_KL_C-2.psyexp` z `baseline` i `monitoring`, testy | KL-C – implementacja |
| 2026-11-08 | DK | Sesje clean i noisy (XDF 427,3 s i 411,0 s, pliki statusu), zrzuty ekranu 7-1 – 7-4 | KL-C – nagrania |
| 2026-11-09 | OS | Ewaluacja i sekcja analityczna (`docs/KL-C_ANALIZA.md`): wykrycie, że linia bazowa wypadła poza fazą spoczynku (`sim_t` 1487 s / 72 s), analiza opóźnienia i sesji noisy; rozdz. 5 i 7, plan EyeLogic (5.4), pytania 14.8–14.9, karta źródeł KL-C | KL-C – analiza i dokumentacja |
