"""One-to-one full county join with match audit and post-integration checks."""
import argparse
from pathlib import Path
from common import SOURCES, fips, number, period, load_source, write_csv, write_json

def integrate(directory, output):
    tables = {}
    for source in SOURCES:
        _, rows = load_source(directory, source)
        table = {}
        for row in rows:
            key = fips(row['fips'])
            if key in table:
                raise ValueError(f'{source}: duplicate key {key}')
            period(row, source)
            for variable in SOURCES[source]:
                number(row[variable], variable)
            table[key] = row
        tables[source] = table
    union = set().union(*(set(t) for t in tables.values()))
    intersection = set.intersection(*(set(t) for t in tables.values()))
    fields = ['fips']
    for source, variables in SOURCES.items():
        fields += [source + '_present', source + '_period_start', source + '_period_end'] + variables
    result = []
    for key in sorted(union):
        record = {'fips': key}
        for source, variables in SOURCES.items():
            row = tables[source].get(key, {})
            record[source + '_present'] = int(bool(row))
            for name in ['period_start', 'period_end']:
                record[source + '_' + name] = row.get(name, '')
            for name in variables:
                record[name] = row.get(name, '')
        result.append(record)
    variables = sum(SOURCES.values(), [])
    complete = [r for r in result if all(r[s + '_present'] for s in SOURCES) and all(r[v] != '' for v in variables)]
    write_csv(Path(output) / 'integrated.csv', fields, result)
    write_csv(Path(output) / 'analysis_sample.csv', fields, complete)
    write_json(Path(output) / 'post_quality.json', {
        'accuracy': {'source_values_preserved': True, 'limitation': 'No external source-value validation performed by this join.'},
        'completeness': {'union_counties': len(union), 'matched_all_sources': len(intersection), 'complete_case_counties': len(complete), 'missing_from_source': {s: sorted(union - set(t)) for s, t in tables.items()}, 'missing_variables': {v: sum(r[v] == '' for r in result) for v in variables}},
        'timeliness': {'cdc': '2023', 'bls': '2023', 'acs': '2019-2023 pooled estimate; not a single-year observation'},
        'consistency': {'unique_output_keys': len(result) == len(union), 'join': 'one-to-one full outer; no imputation'},
    })

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    integrate(a.input, a.output)
