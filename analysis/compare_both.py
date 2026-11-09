"""Łączy wyniki dwóch faktycznie nagranych sesji KL-C w tabelę porównawczą."""
import csv
from pathlib import Path
p = Path('reports')
source = [p/'wyniki_clean.csv', p/'wyniki_noisy.csv']
missing = [str(x) for x in source if not x.exists()]
if missing:
    raise SystemExit('Najpierw wykonaj analizę obu XDF: brakuje ' + ', '.join(missing))
rows = []
for path in source:
    with path.open(newline='', encoding='utf8') as f:
        rows.extend(csv.DictReader(f))
out = p/'tabela_klc.csv'
with out.open('w', newline='', encoding='utf8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print('Zapisano:',out)
