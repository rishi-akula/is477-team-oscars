"""Exploratory Pearson associations on a shared complete-case county sample."""
import argparse
import math
from common import read_csv, write_json

def pearson(x, y):
    if len(x) < 3:
        return None
    mx, my = sum(x) / len(x), sum(y) / len(y)
    cross = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return max(-1.0, min(1.0, cross / den)) if den else None

def analyze(path):
    _, rows = read_csv(path)
    predictors = ['unemployment_pct', 'median_household_income', 'bachelors_pct']
    y = [float(r['mental_distress_pct']) for r in rows]
    correlations = {v: pearson([float(r[v]) for r in rows], y) for v in predictors}
    defined = {v: r for v, r in correlations.items() if r is not None}
    best = max((abs(v) for v in defined.values()), default=None)
    return {'n_counties': len(rows), 'method': 'Unweighted Pearson correlation; shared complete-case sample', 'pearson_r': correlations, 'largest_absolute_association': [k for k, v in defined.items() if math.isclose(abs(v), best)], 'limitations': 'Exploratory county-level associations only; no causal, individual-level, or adjusted effects. No significance claims. Null means fewer than three observations or a constant variable.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    write_json(a.output, analyze(a.input))
