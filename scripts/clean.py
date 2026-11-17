"""Normalize staged sources and reject ambiguous keys/periods rather than guess."""
import argparse
from pathlib import Path
from common import SOURCES, fips, number, period, load_source, write_csv, write_json

def clean(directory, output):
    prepared = {}
    log = []
    for source, variables in SOURCES.items():
        fields, rows = load_source(directory, source)
        result, seen = [], set()
        for index, row in enumerate(rows, 2):
            key = fips(row['fips'])
            if key in seen:
                raise ValueError(f'{source}: duplicate county {key}; resolve source selection first')
            seen.add(key)
            start, end = period(row, source)
            record = {'fips': key, 'period_start': start, 'period_end': end}
            if key != row['fips']:
                log.append({'source': source, 'row': index, 'field': 'fips', 'operation': 'strip_and_zero_pad'})
            for variable in variables:
                value = number(row[variable], variable)
                record[variable] = '' if value is None else value
                if str(record[variable]) != row[variable]:
                    log.append({'source': source, 'row': index, 'field': variable, 'operation': 'normalize_numeric_or_missing'})
            result.append(record)
        prepared[source] = (fields, result)
    for source, (fields, rows) in prepared.items():
        write_csv(Path(output) / (source + '.csv'), fields, rows)
    write_json(Path(output) / 'cleaning_log.json', log)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    clean(a.input, a.output)
