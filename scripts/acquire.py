"""Download and stage three county sources; keep source bytes and provenance."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from datetime import datetime, timezone

from common import write_csv, write_json

CDC = 'https://data.cdc.gov/resource/swc5-untb.json'
BLS = 'https://www.bls.gov/lau/laucnty23.xlsx'
CENSUS_INCOME = 'https://api.census.gov/data/2023/acs/acs5'
CENSUS_EDUCATION = 'https://api.census.gov/data/2023/acs/acs5/profile'

def get(url):
    with urlopen(Request(url, headers={'User-Agent': 'IS477-Team-Oscars/1.0 (academic data curation)'}), timeout=60) as response:
        data = response.read()
        if response.url.endswith('/missing_key.html') or b'<html' in data[:100].lower():
            raise ValueError(f'Unexpected HTML/access page from {url}; no data was staged')
        return data

def save(raw, name, data, url, provenance):
    path = raw / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    provenance[name] = {'url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

def cdc(raw, staged, provenance):
    query = urlencode({'$select': 'year,locationid,measureid,datavaluetypeid,data_value,low_confidence_limit,high_confidence_limit', '$where': "year='2023' AND measureid='MHLTH' AND datavaluetypeid='AgeAdjPrv'", '$limit': '10000'})
    url = CDC + '?' + query
    data = get(url)
    save(raw, 'cdc_mhlth_2023.json', data, url, provenance)
    records = json.loads(data)
    if not records or len(records) >= 10000:
        raise ValueError('CDC query empty or limit reached; verify pagination')
    # Socrata response can include non-county aggregate IDs (observed: "59").
    # Preserve those in the raw response; stage only five-digit county IDs.
    result = [{'fips': row['locationid'], 'period_start': 2023, 'period_end': 2023, 'mental_distress_pct': row.get('data_value', '')} for row in records if len(row.get('locationid', '')) == 5 and row['locationid'].isascii() and row['locationid'].isdigit()]
    if len(result) != len({r['fips'] for r in result}):
        raise ValueError('CDC has duplicate county IDs')
    write_csv(staged / 'cdc.csv', ['fips', 'period_start', 'period_end', 'mental_distress_pct'], result)
    return len(result)

def bls(raw, staged, provenance):
    from openpyxl import load_workbook
    data = get(BLS)
    save(raw, 'laucnty23.xlsx', data, BLS, provenance)
    sheet = load_workbook(io.BytesIO(data), read_only=True, data_only=True).active
    rows = []
    for row in list(sheet.values)[2:]:
        if not row[0] or not str(row[0]).startswith('CN'):
            continue
        if str(row[4]) != '2023':
            raise ValueError('Unexpected BLS year')
        rows.append({'fips': str(row[1]).zfill(2) + str(row[2]).zfill(3), 'period_start': 2023, 'period_end': 2023, 'unemployment_pct': row[8]})
    write_csv(staged / 'bls.csv', ['fips', 'period_start', 'period_end', 'unemployment_pct'], rows)
    return len(rows)

def census(raw, staged, provenance):
    # Separate ACS detailed and profile endpoints intentionally retain both source responses.
    urls = [
        (CENSUS_INCOME + '?' + urlencode({'get':'B19013_001E','for':'county:*'}), 'acs_income_2023.json'),
        (CENSUS_EDUCATION + '?' + urlencode({'get':'DP02_0068PE','for':'county:*'}), 'acs_education_2023.json'),
    ]
    tables = []
    for url, name in urls:
        data = get(url)
        save(raw, name, data, url, provenance)
        table = json.loads(data)
        if len(table) < 101:
            raise ValueError('ACS response has fewer than 100 records')
        tables.append({r[-2] + r[-1]: r[0] for r in table[1:]})
    if set(tables[0]) != set(tables[1]):
        raise ValueError('ACS income and education geographies differ; inspect before staging')
    rows = [{'fips': key, 'period_start': 2019, 'period_end': 2023, 'median_household_income': tables[0][key], 'bachelors_pct': tables[1][key]} for key in sorted(tables[0])]
    write_csv(staged / 'acs.csv', ['fips', 'period_start', 'period_end', 'median_household_income', 'bachelors_pct'], rows)
    return len(rows)

def acquire(root):
    root = Path(root)
    raw, staged = root / 'data/raw', root / 'data/staged'
    if staged.exists() and any(staged.iterdir()):
        raise ValueError('Staged directory is not empty; use a fresh output root')
    provenance, counts = {}, {}
    try:
        for name, func in [('cdc', cdc), ('bls', bls), ('acs', census)]:
            counts[name] = func(raw, staged, provenance)
    finally:
        write_json(root / 'data/acquisition_status.json', {'source_files': provenance, 'staged_counts': counts, 'complete': len(counts) == 3})
    return counts

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='.')
    a = p.parse_args()
    print(acquire(a.root))
