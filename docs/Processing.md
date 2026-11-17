# County data processing: Milestone 3 handoff

This implements the processing work shared by Rishi in the project plan. It is **not yet an acquisition-to-analysis workflow**. No real datasets were present in the repository when this contribution was prepared. Tests create tiny synthetic fixtures in temporary directories; they are not research data, do not meet the 100-record requirement, and must not be reported as findings.

## Reproduce the software checks

Use Python 3.10 or newer; the scripts require only the Python standard library. From the repository root:

```bash
python -m unittest discover -s tests -v
```

After acquisition and source-specific staging have been implemented:

```bash
python run_processing.py --input data/staged --output outputs
```

The output directory must be absent or empty. For another run, choose a new directory, for example `--output outputs-review`. Paths are resolved from the repository root; no machine-specific paths are committed. If a stage fails, do not interpret any partial output as a completed run.

## Required staging contract

The acquisition owners must preserve original files under `data/raw/` and implement reproducible adapters that generate these CSVs under `data/staged/`. This is a proposed interface, **not a claim that the source files already use these columns**. Do not manually rename files and call acquisition automated.

| File | Required columns | Reference period |
|---|---|---|
| `cdc.csv` | `fips`, `period_start`, `period_end`, `mental_distress_pct` | 2023–2023, conditional on source verification |
| `bls.csv` | `fips`, `period_start`, `period_end`, `unemployment_pct` | 2023–2023 annual averages |
| `acs.csv` | `fips`, `period_start`, `period_end`, `median_household_income`, `bachelors_pct` | 2019–2023 pooled estimates |

Each file must contain one row per county after selecting the intended measure, geography, estimate type, and period. Use UTF-8 CSV. Percentages use the 0–100 scale; income is the ACS estimate in dollars with the source's dollar-year definition recorded. Confirm the educational population denominator with source documentation. Record the precise CDC mental-distress definition and whether the selected estimate is crude or age-adjusted. The source release year must not be substituted for its observation/reference year. If a verified CDC period differs, the team must revise the scope and the validation rule together.

Keep FIPS as five-character text. The cleaner can restore leading zeros but cannot establish that an identifier is an officially valid county. Supply a reviewed county/county-equivalent universe and document exclusions, geographic changes, and territory treatment before final analysis. Raw Census sentinel values require documented adapter handling; negative numerical values currently stop processing rather than silently becoming zeros.

## Stages and outputs

1. [`assess.py`](../scripts/assess.py) records input SHA-256 checksums, missing counts, invalid values, duplicate keys, reference-period checks, and whether each input has at least 100 rows. The row threshold is reported rather than enforced so small software fixtures can run. Real research inputs must satisfy the course requirement.
2. [`clean.py`](../scripts/clean.py) normalizes identifiers, numerical formatting, and explicit missing markers. It fails on duplicates, invalid values, or unexpected periods. It writes cleaned CSVs and an operation log without altering source inputs. No imputation or outlier deletion is performed.
3. [`integrate.py`](../scripts/integrate.py) validates one-to-one keys and creates `integrated.csv` using the union of county identifiers. Source-presence flags and unmatched-county lists preserve evidence of coverage loss. `analysis_sample.csv` contains only counties present in all sources with all four analytical variables observed. `post_quality.json` records the join checks under the four quality dimensions.
4. [`analyze.py`](../scripts/analyze.py) writes unweighted Pearson correlations on the same complete-case sample. The largest absolute coefficient is an exploratory comparison; ties are retained. Fewer than three observations or constant variables produce null correlations. It does not adjust for confounders, calculate significance, or imply causation. This provisional method needs Josh's review. Visualizations remain to be implemented.

[`run_processing.py`](../run_processing.py) calls these stages in order and stops on errors. It contains orchestration rather than processing logic.

## Quality interpretation and remaining handoff

- **Accuracy:** Range/format checks and preservation of supplied values are limited proxies. Compare selected observations to official publications, verify measure definitions, and evaluate available uncertainty information. These steps have not been completed on real data.
- **Completeness:** Inspect missing-value counts, excluded complete cases, and unmatched counties. Compare exclusions with the intended geography to assess selection bias.
- **Timeliness:** Preserve reference periods and obtain release/retrieval dates in the acquisition provenance record. ACS pooling remains a limitation even when the end year matches.
- **Consistency:** Check uniqueness, units, identifiers, and period selection. Matching strings alone do not prove geographic equivalence.

Nithin and Tito's acquisition work must supply raw files, verified source metadata and permissions, and staging adapters before real-data execution. Hashes here describe the staged files received; they do not prove authenticity or replace raw-download integrity checks. Retain raw-file hashes and provenance separately. Final acceptance also requires source citations, licenses, machine-readable metadata, a full data dictionary, a visualization, and a fresh-clone run starting with acquisition. No data redistribution license is inferred from public accessibility.
