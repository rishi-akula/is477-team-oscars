"""Synthetic fixtures test software behavior, not actual county findings."""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from common import SOURCES, fips, number, write_csv
from clean import clean
from integrate import integrate
from analyze import pearson

class ProcessingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inputs = self.root / 'inputs'
        for source, variables in SOURCES.items():
            rows = []
            for index, key in enumerate(['1001', '01003', '01005']):
                row = {'fips': key, 'period_start': 2019 if source == 'acs' else 2023, 'period_end': 2023}
                row.update({v: (40000 + index * 1000 if v == 'median_household_income' else 10 + index * 2) for v in variables})
                rows.append(row)
            write_csv(self.inputs / (source + '.csv'), list(rows[0]), rows)

    def tearDown(self):
        self.temp.cleanup()

    def edit(self, source, change):
        path = self.inputs / (source + '.csv')
        with path.open() as f:
            reader = csv.DictReader(f)
            fields, rows = reader.fieldnames, list(reader)
        change(rows)
        write_csv(path, fields, rows)

    def test_fips_normalization_and_aggregate_rejection(self):
        self.assertEqual(fips(' 1001 '), '01001')
        for bad in ['01000', '00001', '01001.0', '123456', 'abc']:
            with self.assertRaises(ValueError):
                fips(bad)

    def test_numeric_missing_and_invalid(self):
        self.assertIsNone(number('NA', 'bachelors_pct'))
        self.assertEqual(number('40,000', 'median_household_income'), 40000)
        for bad in ['NaN', 'inf', '-666666666', '101']:
            with self.assertRaises(ValueError):
                number(bad, 'bachelors_pct')

    def test_duplicate_keys_fail(self):
        self.edit('cdc', lambda rows: rows.append(dict(rows[0])))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            clean(self.inputs, self.root / 'clean')

    def test_wrong_period_fails(self):
        self.edit('cdc', lambda rows: rows[0].update(period_start='2022'))
        with self.assertRaisesRegex(ValueError, 'reference period'):
            clean(self.inputs, self.root / 'clean')

    def test_outer_join_and_complete_case_audit(self):
        self.edit('bls', lambda rows: rows.pop())
        self.edit('acs', lambda rows: rows[0].update(bachelors_pct='NA'))
        clean(self.inputs, self.root / 'clean')
        integrate(self.root / 'clean', self.root / 'out')
        report = json.loads((self.root / 'out/post_quality.json').read_text())
        self.assertEqual(report['completeness']['union_counties'], 3)
        self.assertEqual(report['completeness']['matched_all_sources'], 2)
        self.assertEqual(report['completeness']['complete_case_counties'], 1)
        self.assertEqual(report['completeness']['missing_from_source']['bls'], ['01005'])

    def test_correlations_and_undefined_cases(self):
        self.assertAlmostEqual(pearson([1, 2, 3], [6, 4, 2]), -1)
        self.assertIsNone(pearson([1, 1, 1], [2, 3, 4]))
        self.assertIsNone(pearson([1, 2], [2, 4]))

    def test_orchestrator_end_to_end_and_stale_output_guard(self):
        output = self.root / 'out'
        command = [sys.executable, str(ROOT / 'run_processing.py'), '--input', str(self.inputs), '--output', str(output)]
        first = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        report = json.loads((output / 'associations.json').read_text())
        self.assertEqual(report['n_counties'], 3)
        self.assertAlmostEqual(report['pearson_r']['unemployment_pct'], 1)
        second = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn('stale results', second.stderr)

    def test_missing_input_fails_without_creating_output(self):
        (self.inputs / 'cdc.csv').unlink()
        output = self.root / 'out'
        run = subprocess.run([sys.executable, str(ROOT / 'run_processing.py'), '--input', str(self.inputs), '--output', str(output)], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('Missing staged input', run.stderr)
        self.assertFalse(output.exists())

if __name__ == '__main__':
    unittest.main()
