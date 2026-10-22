# Project Plan

## Overview
The goal of this project is to look at how different socioeconomic factors relate to adult mental distress across U.S counties. Specifically, we want to see how unemployment, median household income, and education level are related to mental distress and determine which of these factors has the strongest association. To do this, we will use data from three different sources: CDC PLACES, the Bureau of Labor Statistics, and the U.S. Census Bureau. Each dataset provides a different part of the information we need and can be connected using five-digit county FIPS codes. We will focus on data from or representing 2023 so that the information is as consistent as possible across the datasets. After collecting the data, we will check its quality, clean and organize the variables we need, and combine the three datasets into one county-level dataset. Once the datasets are integrated, we will analyze the relationships between unemployment, income, education, and adult mental distress to see which socioeconomic factor has the strongest association with mental distress across U.S. counties.
## Team

## Research or Business Question(s)
- **Primary Research Question:** How do unemployment, median household income, and educational level relate to adult mental distress across U.S. counties, and which factor is most strongly associated?

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

## Constraints

## Gaps
