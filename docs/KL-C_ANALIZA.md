# KL-C – Sekcja analityczna (P3)

**Opracowanie:** OS · **Dane i sesje:** DK · **Data:** 2026-11-09
Dane: `sample_data/P3_KL-C_clean_fixed_1.xdf`, `sample_data/P3_KL-C_noisy_360s.xdf`, pliki statusu `sample_data/KL-C_STATUS_*.csv`, wyniki `reports/tabela_klc.csv`. Opis budowy: Build Book, rozdz. 5 i 7.

## 1. Problem

W P3 sygnałem głównym jest EDA, a uczestnik swobodnie ogląda obrazy. Eksperymentator musi w każdej chwili wiedzieć, (a) czy dane z ostatnich sekund w ogóle nadają się do analizy i (b) w jakim stanie jest uczestnik względem własnej linii bazowej – bo na tym będą oparte reguły adaptacji (KL-D). Surowe strumienie są zaszumione: czujnik gubi kontakt (`lost`, wartości `null`), pojawiają się artefakty ruchowe (`noisy`: skoki HR o 25–60 bpm, EDA o 1,5–4 µS), a MouseGaze „gubi wzrok” przy mrugnięciu lub kursorze poza oknem. Klasyfikacja z pojedynczej próbki reagowałaby na każdy taki artefakt i stan by „migotał”.

## 2. Analiza

- **Nagranie noisy** (`--noise 0.6 --dropout 0.4`): 18,4 % próbek LBK_Sim odrzuconych (177 `noisy`, 125 `lost` z 1645). W oknie 5 s to średnio 3–4 złe próbki na 20, więc jakość EDA była `zaszumiona` przez 75,4 % czasu.
- **Wzrok (MouseGaze):** w obu sesjach ≥ 96 % czasu `poprawny`; braki to krótkie, celowe symulacje (przycisk myszy / kursor poza oknem).
- **Linia bazowa:** w plikach statusu kolumna `sim_t` pokazuje, że w chwili `calib:start` symulator działał już **1487 s** (clean) i **72 s** (noisy). Scenariusz `mix` powtarza się co 180 s: spokój 0–40 s, skupienie 40–80 s, stres 80–120 s, spokój 120–150 s, zmęczenie 150–180 s. Baseline clean (`sim_t` 1487–1517 s, czyli 47–77 s cyklu) wypadł więc w fazie *skupienie*, a noisy (72–102 s cyklu) na przełomie *skupienie/stres*. Dlatego linie bazowe są zawyżone (EDA 3,39 µS i 5,63 µS, przy spoczynkowym poziomie symulatora ok. 2 µS) – a wszystkie progi są liczone względem tej bazy.
- **Opóźnienie:** EDA symulatora dochodzi do nowego poziomu ze stałą czasową ok. 8 s; do tego dochodzi okno 5 s i histereza 6 s. Zmiana stanu następuje więc ok. 10–20 s po zmianie fazy, przy fazach trwających 30–40 s.

## 3. Dwa warianty rozwiązania

**Wariant A – decyzja z bieżącej próbki, bez filtrowania i bez histerezy.** Stan liczony z ostatniej próbki HR/EDA, zmiana natychmiast.
+ reaguje od razu, prosty;
− każdy artefakt (`noisy`) daje fałszywe „pobudzenie”, braki (`lost`) – przypadkowe stany; stan zmienia się wielokrotnie na minutę („migotanie”); nie da się na nim oprzeć reguł adaptacji.

**Wariant B – filtrowanie, okna jakości, linia bazowa i histereza.** Odrzucanie próbek (quality ≠ ok, HR poza 35–200, EDA ≤ 0, RR poza 300–2000), wskaźnik jakości z okien 2 s (wzrok) i 5 s (EDA) z progami 90 % / 60 %, mediany w oknie 5 s, progi względem własnej linii bazowej, klasyfikacja tylko przy dobrej jakości EDA i zmiana stanu po ≥ 6 s zgodnych decyzji.
+ odporny na pojedyncze artefakty, stan stabilny, każda zmiana to wiarygodne zdarzenie (znacznik `state:*`);
− reaguje wolniej (10–20 s); przy długotrwale zaszumionym sygnale nie daje informacji (stan `nieznany`).

## 4. Wybór

Wybrano **wariant B**. Stan ma być podstawą reguł adaptacji (KL-D), które w P3 mogą działać tylko między próbami (dłuższa przerwa, ekran neutralny), więc opóźnienie kilku–kilkunastu sekund jest akceptowalne, a fałszywe alarmy – nie. Stan widzi wyłącznie eksperymentator (konsola, plik statusu, znaczniki); czas ekspozycji obrazu (4000 ms), szary ekran (1000 ms) i kolejność obrazów pozostają bez zmian.

## 5. Efekt

| | clean | noisy |
|---|---:|---:|
| Zgodność stanów ze `scenario` | 39,57 % | 18,40 % |
| Zmiany stanu w 360 s | 7 | 0 |
| EDA `poprawny` (% czasu) | 100,00 % | 23,46 % |
| Wzrok `poprawny` (% czasu) | 96,65 % | 98,04 % |

- **Brak migotania:** w sesji clean 9 zmian stanu w 427 s, najkrótszy odstęp między zmianami 7,0 s; w sesji noisy żadna przypadkowa zmiana mimo 302 odrzuconych próbek – cel stabilności osiągnięty.
- **Zgodność jest niska z dwóch powodów technicznych:** (1) linia bazowa z fazy *skupienie/stres* zamiast spoczynku – wysoka baza sprawia, że późniejsze fazy wyglądają na „spoczynek” lub „nieznany”; (2) opóźnienie 10–20 s przy fazach 30–40 s. Nie świadczy to o działaniu klasyfikatora na ludziach – dane są symulowane.
- **Noisy = 0 zmian:** reguła „klasyfikuj tylko przy jakości `poprawny`” przy 75 % czasu `zaszumiony` daje stały stan `nieznany`. Wariant B jest więc bezpieczny, ale przy takim poziomie zakłóceń mało informatywny.

**Wnioski na kolejny etap (KL-D):** (1) przed każdą sesją uruchamiać symulator od nowa i rozpoczynać baseline w ciągu 10 s (kontrola: `sim_t` < 10 s przy `calib:start`) i powtórzyć oba nagrania; (2) rozważyć klasyfikację z przyjętych próbek także przy jakości `zaszumiony` (≥ 60 % dobrych próbek); (3) rozważyć progi jako stosunek do linii bazowej (np. EDA ≥ 1,8 × baza) – poziom EDA różni się między osobami kilkukrotnie; (4) w LBK zastąpić `focus` symulatora miarą z eye-trackera.
