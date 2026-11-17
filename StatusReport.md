# Milestone 3: Interim Status Report

## Scope and current status

This report records repository-visible progress as of November 16, 2026. It includes Rishi Akula's implementation and status contribution; the other members must add their own progress details and contribution summaries before the group submits the milestone. Uncommitted work on a teammate's computer is not treated as absent work, but it cannot yet support reproducibility claims in this report.

The research question remains how unemployment, median household income, and educational attainment relate to adult mental distress across U.S. counties. The [project plan](ProjectPlan.md) identifies CDC PLACES, BLS unemployment statistics, and ACS estimates as complementary sources connected through county FIPS codes. The target remains data from or representing 2023, subject to verifying the CDC reference period. The ACS 2019–2023 estimate will remain explicitly identified as pooled data.

Before this contribution, the repository contained only ProjectPlan.md and the [team README](README.md). No source datasets, acquisition scripts, cleaned datasets, integration results, or feedback records were present. Rishi has now added a modular processing implementation, reproducible software tests, and an [input and processing guide](docs/Processing.md). Actual data acquisition, source-specific staging, and real-data validation remain dependencies. There are no substantive research findings yet.

## Progress against the project plan

| Planned task | Evidence and current status | Responsibility in the plan |
|---|---|---|
| Setup and research questions | Repository, team roster, questions, and roles are documented in ProjectPlan.md. | All members; Josh guides questions |
| Acquisition and organization | Three sources are described, but raw files and acquisition artifacts are not yet committed. The staging interface is now documented. | Nithin and Tito |
| Ethics and initial quality assessment | Source permissions remain unverified. [Assessment code](scripts/assess.py) implements checks organized by accuracy, completeness, timeliness, and consistency; real-data assessment is pending. | Tito and Rishi |
| Cleaning and integration | [Cleaning](scripts/clean.py) and [integration](scripts/integrate.py) scripts are implemented and tested using synthetic data. Actual-source execution is blocked on inputs. | Nithin and Rishi |
| Post-integration assessment and analysis | Integration generates a quality report and coverage audit. [Analysis code](scripts/analyze.py) compares correlations on a common complete-case sample; no real results are available. | Josh and Rishi |
| Automation and documentation | [Processing orchestrator](run_processing.py), [guide](docs/Processing.md), and [tests](tests/test_processing.py) are committed. Acquisition is not yet connected. | All members |
| Final review and submission | Fresh-clone real-data reproduction, final report, visualizations, and release preparation remain outstanding. | All members |

## Implementation and validation

The processing sequence is assessment, cleaning, integration with post-integration checks, and exploratory analysis. Each stage is a separate script with explicit inputs and outputs. The orchestrator calls them in order and stops if a stage fails. The implementation uses the Python standard library and repository-relative paths, reducing setup dependencies.

The cleaner preserves original inputs, restores leading zeros in FIPS identifiers, normalizes numerical formatting, and converts explicit missing markers to empty values. Duplicate county identifiers, unexpected reference periods, negative or non-finite numerical values, and percentages outside 0–100 cause errors rather than silent correction. Source-specific sentinel handling and measure selection still require verified adapters.

Integration retains the union of counties and records which sources contribute each county. It reports unmatched identifiers and creates a separate complete-case analysis sample. This makes exclusions visible rather than hiding them in an inner join. The provisional analysis compares unweighted Pearson correlations using the same counties for all predictors. It reports undefined correlations and ties explicitly. Josh must review this choice before substantive interpretation.

Eight tests passed using temporary synthetic fixtures. They cover FIPS handling, numeric validation, duplicate rejection, temporal mismatch rejection, outer-join coverage and complete-case counts, correlation behavior, orchestration, and missing-input failure. A repeated-run check prevents reuse of a nonempty output directory that could contain stale results. These tests demonstrate software behavior only: they do not validate actual source accuracy, confirm nationwide coverage, or satisfy the requirement for research datasets containing at least 100 records each.

## Changes to the plan

The original schedule placed cleaning in November 2–8 and analysis in November 9–15. Repository evidence does not support marking those stages complete on actual data. The revised sequence separates software readiness from verified data availability and makes later work dependent on the input handoff. The [Milestone 3 addendum](ProjectPlan.md#milestone-3-update-rishis-work) records this change while retaining the original plan for comparison.

The processing contract now explicitly specifies one selected observation per county and source, five-digit FIPS identifiers, reference-period columns, and the four analytical variables. This is a proposed standardized interface rather than a description of the raw downloads. No Milestone 2 instructor feedback was available in the repository, so no changes are attributed to instructor feedback. The team must incorporate that feedback when it is available.

## Challenges, limitations, and remaining gaps

**Unavailable inputs:** Actual-source checks cannot run until raw datasets and reproducible staging adapters are committed. Nithin and Tito should supply these artifacts with source URLs, retrieval dates, raw-file checksums, and selected variables. Rishi can then run the processing stages and resolve issues revealed by the data. Staged-file hashes are already recorded, but do not replace raw-download integrity checks.

**Period and measure selection:** The CDC mental-distress definition, estimate type, and reference period remain to be confirmed. The implementation expects a 2023 reference year and will reject a mismatch. The team must revise the scope and validation rule together if verified coverage differs. Matching ACS's end year to BLS does not make a five-year estimate equivalent to an annual measure.

**Geographic coverage:** The plan's ACS description lists 853 rows while claiming all-county coverage. The extraction and coverage must be checked before analysis. FIPS formatting alone cannot validate county boundaries or county-equivalent changes. A reviewed geographic universe, duplicate audit, and unmatched-county investigation are still necessary.

**Quality and interpretation:** Range checks are limited evidence of accuracy. Selected values need comparison with official sources, and source uncertainty needs review. Complete-case exclusions may introduce bias. County associations cannot establish individual relationships or causation, and the provisional correlations do not adjust for confounders.

**Reproducibility and permissions:** Reuse conditions, data citations, licenses, full metadata, visualizations, and acquisition integration remain incomplete. Public accessibility is not sufficient evidence of unrestricted redistribution. A successful synthetic test run must not be described as a successful end-to-end research workflow.

## Updated timeline for Rishi's remaining work

These are proposed internal targets, not confirmed Canvas deadlines. Acquisition handoff and teammate availability must be confirmed; delays move dependent work rather than justify unsupported completion claims.

| Target | Deliverable and status | Owner/dependency |
|---|---|---|
| November 16 | Processing implementation, synthetic tests, challenge update, and contribution summary complete. | Rishi |
| November 17–18 | Obtain verified inputs and adapters; review periods, variables, coverage, and permissions. Pending handoff. | Nithin/Tito supply acquisition; Rishi reviews |
| November 19–20 | Run initial assessment, cleaning, and integration on actual data; retain quality reports and correction logs. Pending inputs. | Rishi with Nithin |
| November 21–22 | Review post-integration quality and exclusions; generate and interpret exploratory associations and visualizations. Pending validated integration. | Rishi with Josh |
| November 23–25 | Connect acquisition to processing and complete provenance, metadata, and reproduction documentation. Pending preceding stages. | All members |
| November 26–29 | Test a fresh clone and complete final review, adjusted to confirmed course deadlines. Pending full workflow. | All members |

## Individual contributions

### Rishi Akula

My contribution for this milestone consists of the processing scripts for initial quality assessment, cleaning, county-level integration, post-integration checks, and exploratory correlation analysis; the processing orchestrator; and eight reproducible software tests. I also added the staging contract and processing documentation, reviewed unresolved constraints and gaps, and updated the status and timeline for my assigned work. The implementation has been tested with synthetic fixtures. Actual-source execution and substantive findings remain pending the acquisition handoff.

### Other team members

Josh, Nithin, and Tito must each add and commit their own contribution summary and links to their work before the report is finalized. Their uncommitted progress and any instructor feedback should be incorporated into the task statuses above. The group must then review the complete report, create the status-report tag and release, and submit its release URL through Canvas.
