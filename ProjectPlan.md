# Project Plan

## Overview
The goal of this project is to look at how different socioeconomic factors relate to adult mental distress across U.S counties. Specifically, we want to see how unemployment, median household income, and education level are related to mental distress and determine which of these factors has the strongest association. To do this, we will use data from three different sources: CDC PLACES, the Bureau of Labor Statistics, and the U.S. Census Bureau. Each dataset provides a different part of the information we need and can be connected using five-digit county FIPS codes. We will focus on data from or representing 2023 so that the information is as consistent as possible across the datasets. After collecting the data, we will check its quality, clean and organize the variables we need, and combine the three datasets into one county-level dataset. Once the datasets are integrated, we will analyze the relationships between unemployment, income, education, and adult mental distress to see which socioeconomic factor has the strongest association with mental distress across U.S. counties.
## Team

## Research or Business Question(s)
- **Primary Research Question:** How do unemployment, median household income, and educational level relate to adult mental distress across U.S. counties, and which factor is most strongly associated?

To help answer our main research question, we will also look at the following questions:
  1. How does the unemployment rate relate to adult mental distress across U.S. counties?
  2. How does median household income relate to adult mental distress across U.S. counties?
  3. How does educational attainment relate to adult mental distress across U.S counties?
  4. Which of these three factors has the strongest association with adult mental distress?

## Datasets
We use three datasets, all from U.S. federal sources. Each provides a different type of information, and it can all be linked with a 5 digit county FIPS code, which is a 2 digit state code and a 3 digit county code for the year of 2023.

1. CDC Places: Country Data 
- **Source:** CDC Division of Population Health, Epidemiology and Surveillance Branch, produced with the Robert Wood Johnson Foundation and the CDC Foundation. 
- **Contents:** 40 measurable statistics at the county level, such as the health status which could measure the "mental distress" part of our question.
- **Access:** Downloadable from data.cdc.gov: https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-County-Data-20/swc5-untb/about_data
- **License:** This dataset has the uses listed and has unrestricted access
- **Coverage:** All U.S. counties
- **Integration:** State FIPS and county FIPS combines into a 5 digit code that is under the column "LocationID"
- **Format/Size:** Excel file of 22 columns and 229,298 rows

2. BLS Local Area Unemployment Statistics
- **Source/Provenance:** U.S. Bureau of Labor Statistics. Estimates monthly and annual employment and unemployment statistics for counties, states, and more.
- **Contents:** Labor force, employment, number of unemployed people, and unemployment rate for each county
- **Access:** One Excel file per year: https://www.bls.gov/lau/tables.htm
- **License:** U.S. government data
- **Coverage:** All counties, annual averages
- **Integration:** State FIPS and county FIPS that are combined into a 5 digit code
- **Format/Size:** Excel with 9 columns and 3221 rows

3. U.S. Census Bureau American Community Survey, 2019 - 2023 5 Year Estimates
- **Source:** U.S. Census Bureau. Five year estimates for period estimates, so that represents 60 months of survey data
- **Contents:** Median household income and percent of adults over the age of 25 with a bachelor's degree or higher separated by county
- **Access:** Downloadable from data.census.gov 
- **Coverage:** All U.S. counties
- **Integration:** Last 5 characters of the GEO_ID because that is the same as the FIPS
- **Format/Size:** 5 columns and 853 rows
## Timeline
Week 1: Project Setup and Research Questions (October 12–18)

- Establish our GitHub repository and assign responsibilities to each group member.
- Determine our research question and identify the socioeconomic factors we want to compare with adult mental distress across U.S. counties.
- Identify three datasets from CDC PLACES, the Bureau of Labor Statistics, and the U.S. Census Bureau that provide the information needed for our analysis.
- Responsible: All group members.

Week 2: Data Acquisition and Organization (October 19–25)

- Download and organize the three datasets, focusing on data from or representing 2023 to keep our information as consistent as possible.
- Examine the structure of each dataset and identify the variables needed for our analysis, including mental distress, unemployment, median household income, and education level.
- Determine how the datasets can be connected using five-digit county FIPS codes.
- Organize our files within the GitHub repository and document where each dataset came from.
- Responsible: Members Nithin and Tito.

Week 3: Ethical Considerations and Initial Data Quality Assessment (October 26–November 1)

- Review the licensing, terms of use, and other ethical considerations for each dataset to ensure we can properly use and share the information.
- Evaluate the accuracy, completeness, timeliness, and consistency of each dataset before cleaning or integrating them.
- Identify any missing values, inconsistent county identifiers, or differences in coverage that could affect our analysis.
- Document our findings and determine what changes may be needed before combining the datasets.
- Responsible: Members Tito and Rishi.

Week 4: Data Cleaning and Integration (November 2–8)

- Clean the datasets by addressing missing values, inconsistent formatting, and any other issues identified during our initial quality assessment.
- Standardize county FIPS codes and the variables needed for our research question.
- Combine the cleaned datasets into one county-level dataset using Python/Pandas or SQL.
- Responsible: Members Nithin and Rishi.

Week 5: Post-Integration Quality Assessment and Analysis (November 9–15)

- Evaluate the integrated dataset for accuracy, completeness, timeliness, and consistency to determine whether the datasets were successfully combined.
- Analyze the relationships between unemployment, median household income, education level, and adult mental distress.
- Compare the results to determine which socioeconomic factor has the strongest association with adult mental distress across U.S. counties.
- Responsible: Members Josh and Rishi.

Week 6: Workflow Automation and Documentation (November 16–22)

- Develop an automated workflow using separate scripts that can reproduce the process from data acquisition through analysis.
- Document our data sources, cleaning methods, integration process, and any limitations encountered.
- Update our GitHub repository with the necessary files, metadata, and instructions so the project can be reproduced.
- Responsible: All group members.

Week 7: Final Review and Submission (November 23–29)

- Review our completed analysis and verify that the results address our original research question.
- Finalize the project report, visualizations, and supporting documentation.
- Confirm that our workflow runs successfully and all required files are included in the GitHub repository.
Responsible: All group members.
## Constraints

**Temporal comparability:** The proposed sources do not necessarily describe identical time periods. The ACS 2019–2023 five-year estimates summarize a period, while the proposed BLS data describe 2023 annual averages. We must also verify the reference year of the selected CDC measure rather than assuming that its release year is its measurement year. These differences will be documented when interpreting associations.

**Geographic alignment and missing data:** Shared county FIPS codes provide a potential linkage, but matching coverage must be verified. Formatting differences, geographic changes, missing estimates, and duplicate records could prevent valid joins. We will preserve leading zeros, check identifier uniqueness, and report unmatched or excluded counties. Missing values will not automatically be treated as zero, and exclusions may limit how broadly our findings apply.

**Interpretation:** This is an observational, county-level analysis. Associations cannot establish that unemployment, income, or education causes mental distress, and county-level patterns cannot establish relationships for individual residents. Comparing the strongest association will require a consistent method and the same county sample across variables.

**Access and reuse:** Downloads, file formats, and source revisions may affect reproducibility. We will document the versions acquired, retain checksums, and verify each source’s reuse and redistribution conditions before publishing data. Our reporting will avoid characterizing individual residents based on county averages.

## Gaps

Several details remain unresolved before implementation:

- **CDC measure selection:** We need to confirm the exact mental-distress variable, its definition, reference year, and estimate type. Nithin and Josh will review the source documentation and record the selection.
- **ACS extraction and coverage:** We need exact table and variable identifiers for household income and educational attainment. The current description lists 853 rows while claiming all-county coverage; Nithin will verify the extraction and correct its scope or description.
- **Integration feasibility:** The number of counties shared across all three sources is not yet known. Tito and Rishi will conduct an initial join audit, investigate unmatched codes, and document geographic exclusions.
- **Analysis specification:** Josh and Rishi will define how “strongest association” will be compared, including the association measure, missing-data rule, and whether transformations are appropriate.
- **Acquisition and permissions:** Exact download endpoints, formats, and reuse terms still require verification. Nithin and Tito will test acquisition and document any access restrictions.

These gaps will be addressed during the first implementation week, with the plan updated if verification reveals changes in scope or feasibility.
