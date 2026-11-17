"""Processing-only orchestrator. Acquisition and source adapters are not yet connected."""
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', default='data/staged')
    p.add_argument('--output', default='outputs')
    a = p.parse_args()
    root = Path(__file__).resolve().parent
    inputs, output = root / a.input, root / a.output
    if output.exists() and any(output.iterdir()):
        p.error('Output directory must be new or empty to prevent stale results; choose --output.')
    for source in ['cdc', 'bls', 'acs']:
        if not (inputs / (source + '.csv')).is_file():
            p.error(f'Missing staged input: {source}.csv. See docs/Processing.md.')
    stages = [
        ('assess.py', inputs, output / 'pre_quality.json'),
        ('clean.py', inputs, output / 'cleaned'),
        ('integrate.py', output / 'cleaned', output),
        ('analyze.py', output / 'analysis_sample.csv', output / 'associations.json'),
    ]
    for script, source, destination in stages:
        subprocess.run([sys.executable, str(root / 'scripts' / script), '--input', str(source), '--output', str(destination)], check=True)

if __name__ == '__main__':
    main()
