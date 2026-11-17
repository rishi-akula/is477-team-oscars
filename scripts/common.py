"""Shared CSV contract; source-specific acquisition remains a separate stage."""
import csv
import json
import math
from pathlib import Path

SOURCES = {
    'cdc': ['mental_distress_pct'],
    'bls': ['unemployment_pct'],
    'acs': ['median_household_income', 'bachelors_pct'],
}
MISSING = {'', 'na', 'n/a', 'null', 'none', '*', '**', '-', '(x)'}

def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)

def write_csv(path, fields, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')

def fips(value):
    value = value.strip()
    if not value.isascii() or not value.isdigit() or not 1 <= len(value) <= 5:
        raise ValueError('FIPS must contain 1–5 ASCII digits')
    value = value.zfill(5)
    if value[:2] == '00' or value[2:] == '000':
        raise ValueError('Aggregate/invalid FIPS')
    return value

def number(value, variable):
    value = value.strip()
    if value.lower() in MISSING:
        return None
    result = float(value.replace(',', ''))
    if not math.isfinite(result) or result < 0 or (variable.endswith('_pct') and result > 100):
        raise ValueError('Out-of-range or non-finite value')
    return result

def load_source(directory, source):
    fields, rows = read_csv(Path(directory) / (source + '.csv'))
    required = ['fips', 'period_start', 'period_end'] + SOURCES[source]
    missing = set(required) - set(fields)
    if missing:
        raise ValueError(f'{source}: missing columns {sorted(missing)}')
    return required, rows

def period(row, source):
    expected = (2019, 2023) if source == 'acs' else (2023, 2023)
    observed = (int(row['period_start']), int(row['period_end']))
    if observed != expected:
        raise ValueError(f'{source}: expected reference period {expected}, got {observed}')
    return observed
