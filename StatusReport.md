# Milestone 3: Interim Status Report

## Scope and current status

This report presents the progress that can be seen in the repository as of November 16, 2026 (updated after source confirmation). This includes our team implementation and status contribution. The other members need to add their progress details and a summary of their contribution before the group submits the milestone. Unfinished work on a teammate’s computer does not count as missing work, but it does not yet lend itself to claims of reproducibility in this report.

It is unclear how unemployment, median household income, and level of education impact adult mental health in different U.S. counties. The [project plan](ProjectPlan.md) mentions CDC PLACES, BLS unemployment numbers, and ACS estimates as sources that play well together and are connected by county FIPS codes. Still aiming for data from or about 2023, but need to check CDC reference period first. The ACS estimate for 2019-2023 will remain clearly labeled as pooled data.

Before this contribution, the repository contained only ProjectPlan.md and the [team README](README.md). No source datasets, acquisition scripts, cleaned datasets, integration results, or feedback records were present. We now added a modular processing implementation, reproducible software tests, and an [input and processing guide](docs/Processing.md). Actual data acquisition, source-specific staging, and real-data validation remain dependencies. There are no substantive research findings yet.

## Progress against the project plan

| Planned task | Evidence and current status | Responsibility in the plan |
|---|---|---|
| Setup and research questions | Repository, team roster, questions, and roles are documented in ProjectPlan.md. | All members; Josh guides questions |
| Acquisition and organization | The [acquisition script](scripts/acquire.py) fetched CDC and BLS official files and staged county CSVs. CDC produced 2,957 county rows; BLS produced 3,221. Census returned an HTML access page, so its file is unavailable. Source URLs, UTC retrieval times, and SHA-256 hashes are recorded in [the acquisition status](data/acquisition_status.json). | Nithin and Tito |
| Ethics and initial quality assessment | Source permissions remain unverified. CDC and BLS identifiers were checked for duplicates; each has zero duplicate FIPS. [Assessment code](scripts/assess.py) implements checks organized by accuracy, completeness, timeliness, and consistency; real-data assessment is pending. | Tito and Rishi |
| Cleaning and integration | [Cleaning](scripts/clean.py) and [integration](scripts/integrate.py) scripts are implemented and tested using synthetic data. Actual-source execution is blocked on inputs. | Nithin and Josh |
| Post-integration assessment and analysis | Integration generates a quality report and coverage audit. [Analysis code](scripts/analyze.py) compares correlations on a common complete-case sample; no real results are available. | Josh and Rishi |
| Automation and documentation | [Processing orchestrator](run_processing.py), [guide](docs/Processing.md), and [tests](tests/test_processing.py) are committed. Acquisition is not yet connected. | All members |
| Final review and submission | Fresh-clone real-data reproduction, final report, visualizations, and release preparation remain outstanding. | All members |

## Implementation and validation
The processing is in the order of evaluation, cleaning, integration with post-integration checks, and exploratory analysis. Each step is a separate script with defined inputs and outputs. The conductor calls them out in order, and if one fails, it stops. It uses the standard Python library and repository-relative paths, reducing the number of dependencies needed to set up.

The cleaner preserves original inputs, restores leading zeros in FIPS identifiers, normalizes numerical formatting, and converts explicit missing markers to empty values. Duplicate county identifiers, unexpected reference periods, negative or non-finite numerical values, and percentages outside 0-100 cause errors rather than silent correction. Source-specific sentinel handling and measure selection still require verified adapters.

Integration keeps the counties together and keeps track of where each county’s sources are coming from. It creates a separate complete-case analysis sample and reports any non-matching identifiers. This shows exclusions, instead of hiding them inside an inner join. The unweighted Pearson correlations are compared in the preliminary analysis using the same counties for all predictors. It shows undefined correlations and connections. Before Josh can make a substantive interpretation, he has to look at this choice.

Eight tests passed via temporary synthetic fixtures. They talk about handling FIPS, checking numbers, getting rid of duplicates, getting rid of time mismatches, outer-join coverage and full-case counts, correlation behavior, orchestration, and failing when an input is missing. A repeated-run check stops again if the output directory is not empty, because it might contain old results. They are just tests to show how the software runs. They do not check the actual source for accuracy, check that they cover the entire country, or that they meet the requirement for research datasets with at least 100 records each.

For our analysis, we plan to use Pearson correlations to compare how unemployment, median household income, and education level relate to adult mental distress across U.S. counties. We will look at each factor separately and compare the strength of its relationship with mental distress to determine which one has the strongest association. To make sure our comparisons are consistent, we will use the same counties for all three factors and exclude counties that are missing any of the variables needed for the analysis. Once the datasets are fully cleaned and combined, we will be able to calculate these correlations and interpret what they tell us about our original research question.

## Changes to the plan

The original schedule placed cleaning in November 2-8 and analysis in November 9-15. Repository evidence does not support marking those stages complete on actual data. The revised sequence separates software readiness from verified data availability and makes later work dependent on the input handoff. The [Milestone 3 addendum](ProjectPlan.md#milestone-3-update-rishis-work) records this change while retaining the original plan for comparison.

The processing contract now explicitly specifies one selected observation per county and source, five-digit FIPS identifiers, reference-period columns, and the four analytical variables. This is a proposed standardized interface rather than a description of the raw downloads. No Milestone 2 instructor feedback was available in the repository, so no changes are attributed to instructor feedback. The team must incorporate that feedback when it is available.

## Challenges, limitations, and remaining gaps

**Unavailable inputs:** Actual-source checks cannot run until raw datasets and reproducible staging adapters are committed. Nithin and Tito should supply these artifacts with source URLs, retrieval dates, raw-file checksums, and selected variables. Rishi can then run the processing stages and resolve issues revealed by the data. Staged-file hashes are already recorded, but do not replace raw-download integrity checks.

**Period and measure selection:** The CDC mental-distress definition, estimate type, and reference period remain to be confirmed. The implementation expects a 2023 reference year and will reject a mismatch. The team must revise the scope and validation rule together if verified coverage differs. Matching ACS's end year to BLS does not make a five-year estimate equivalent to an annual measure.

**Geographic coverage:** The plan's ACS description lists 853 rows while claiming all-county coverage. The extraction and coverage must be checked before analysis. FIPS formatting alone cannot validate county boundaries or county-equivalent changes. A reviewed geographic universe, duplicate audit, and unmatched-county investigation are still necessary.

**Quality and interpretation:** Range checks are limited evidence of accuracy. Selected values need comparison with official sources, and source uncertainty needs review. Complete-case exclusions may introduce bias. County associations cannot establish individual relationships or causation, and the provisional correlations do not adjust for confounders.

**Reproducibility and permissions:** Reuse conditions, data citations, licenses, full metadata, visualizations, and acquisition integration remain incomplete. Public accessibility is not sufficient evidence of unrestricted redistribution. A successful synthetic test run must not be described as a successful end-to-end research workflow.

## Updated timeline for remaining work

These are proposed internal targets, not confirmed Canvas deadlines. Acquisition handoff and teammate availability must be confirmed; delays move dependent work rather than justify unsupported completion claims.

| Target | Deliverable and status | Owner/dependency |
|---|---|---|
| November 16 | Processing implementation, synthetic tests, challenge update, and contribution summary complete. | Rishi |
| November 17-18 | Obtain verified inputs and adapters; review periods, variables, coverage, and permissions. Pending handoff. | Nithin/Tito supply acquisition; Rishi reviews |
| November 19-20 | Run initial assessment, cleaning, and integration on actual data; retain quality reports and correction logs. Pending inputs. | Rishi with Nithin |
| November 21-22 | Review post-integration quality and exclusions; generate and interpret exploratory associations and visualizations. Pending validated integration. | Rishi with Josh |
| November 23-25 | Connect acquisition to processing and complete provenance, metadata, and reproduction documentation. Pending preceding stages. | All members |
| November 26-29 | Test a fresh clone and complete final review, adjusted to confirmed course deadlines. Pending full workflow. | All members |

## Individual contributions

### Rishi Akula

My contribution for this milestone consists of the processing scripts for initial quality assessment, cleaning, county-level integration, post-integration checks, and exploratory correlation analysis; the processing orchestrator; and eight reproducible software tests. I also added the staging contract and processing documentation, reviewed unresolved constraints and gaps, and updated the status and timeline for my assigned work. The implementation has been tested with synthetic fixtures. Actual-source execution and substantive findings remain pending the acquisition handoff.

### Josh Ahrens

For this milestone, I reviewed our progress so far and looked at how our current work connects back to the research question we developed in our original project plan. I also helped outline how we plan to analyze the relationships between unemployment, median household income, education level, and adult mental distress. Specifically, I worked on explaining how we will use Pearson correlations to compare the three factors and determine which has the strongest association with mental distress. Since our datasets have not been fully integrated yet, the actual analysis still needs to be completed. Once the data is ready, I plan to help interpret the results and make sure our findings answer our original research question.

### Tito Gavin 

For this milestone, I focused on helping organize our project's remaining responsibilities and outlining the next steps needed to move forward with our analysis. I worked on updating our project timeline to better reflect what still needs to be completed and how each team member's responsibilities connect to our overall research question. I also helped outline the data acquisition process alongside Nithin, specifically focusing on the information we need to verify before combining our datasets, including the variables being used, time periods, and county-level coverage. Since our datasets have not been fully integrated yet, there are still some steps that need to be completed before we can begin our actual analysis. Moving forward, I plan to help finalize the data acquisition process, ensure our sources are properly documented, and work with the rest of the team to make sure our datasets are ready for cleaning and integration.

## Source verification update

The CDC PLACES 2025 county release was queried for `year=2023`, `measureid=MHLTH`, and `datavaluetypeid=AgeAdjPrv` (frequent mental distress, age-adjusted prevalence). The BLS 2023 LAUS county annual-averages workbook was parsed using its documented FIPS columns. Their source files are roughly 500 KB JSON and 232 KB XLSX locally; staged rows and hashes are linked above. These counts do not demonstrate identical coverage: CDC has 264 fewer county rows than BLS. Their [two-source audit](data/two_source_audit.json) finds 2,956 shared county IDs, one CDC-only county (`15005`), and 265 BLS-only IDs. CDC includes one missing mental-distress value (`48301`). The CDC response also contained non-county ID `59`, which was retained in the raw response but excluded from the staged county file. A three-source audit still awaits ACS. The ACS income variable is `B19013_001E`, and educational attainment is profile variable `DP02_0068PE` (percent of population age 25+ with a bachelor's degree or higher). The Census API currently returns an HTML `/missing_key.html` page despite the request omitting a key. No ACS values were fabricated or substituted.
