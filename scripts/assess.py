"""Profile staged inputs before cleaning; validity checks are not proof of accuracy."""
import argparse
import hashlib
from collections import Counter
from pathlib import Path
from common import SOURCES, fips, number, period, load_source, write_json

def assess(directory):
    report = {}
    for source, variables in SOURCES.items():
        _, rows = load_source(directory, source)
        missing = Counter()
        invalid = Counter()
        keys = []
        periods = Counter()
        for row in rows:
            try:
                keys.append(fips(row['fips']))
            except (ValueError, AttributeError):
                invalid['fips'] += 1
            try:
                periods[str(period(row, source))] += 1
            except (ValueError, TypeError):
                invalid['reference_period'] += 1
            for variable in variables:
                try:
                    if number(row[variable], variable) is None:
                        missing[variable] += 1
                except (ValueError, AttributeError):
                    invalid[variable] += 1
        report[source] = {
            'rows': len(rows),
            'sha256': hashlib.sha256((Path(directory) / (source + '.csv')).read_bytes()).hexdigest(),
            'accuracy': {'invalid_value_counts': dict(invalid), 'limitation': 'Range/format checks only. Compare values with source publications before claiming accuracy.'},
            'completeness': {'missing_counts': dict(missing), 'source_at_least_100_rows': len(rows) >= 100},
            'timeliness': {'reference_period_counts': dict(periods), 'limitation': 'Historical coverage; publication and retrieval dates require source provenance.'},
            'consistency': {'duplicate_fips': sorted(k for k, count in Counter(keys).items() if count > 1)},
        }
    return report

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    write_json(a.output, assess(a.input))
