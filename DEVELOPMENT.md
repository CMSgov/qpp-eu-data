This page outlines the development guidelines for updating and publishing data files.

## System Requirements

- Python 3.11.x

## Installation
- `pipenv install --dev --ignore-pipfile` - will install all the libraries
- `pipenv run pytest --junitxml=coverage/test-report.xml --cov-report html --cov-report xml --cov=processors tests/` - will execute the tests with coverage reports

## Generating Crosswalk
Once the staging steps below are completed run the following command to
generate the [crosswalk](https://en.wikipedia.org/wiki/Schema_crosswalk) file
```
pipenv run python main.py -p generator -y <year>
```

## Overview
Obtaining EUC zipcode crosswalk is a 4 stage process:
1. Create a file containing county names and state from EUC policy (`euc_counties.csv`).
2. Enrich each county with FIPS code. This information is obtained from National Counties from [Census.gov](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html) and by matching the county and state.
3. Enrich each county with zipcodes. This information is obtained from the [HUD USPS ZIP CODE CROSSWALK](https://www.huduser.gov/portal/datasets/usps_crosswalk.html#data)
4. Publish the EUC-zipcode crosswalk. This information will be stored in `data/<year>/euc_county_zipcode_crosswalk.csv` file.

The scripts that automate parts of the above workflow will reside in `processors` package. The lookup files we use while processing and intermediate files generated gets stored in `staging` folder for later references and quality checks.

## Scripts
- **processors/scanner.py**
 This script scans the QPP resource library for EUC factsheet updates. If it finds an update, it will create a Slack alert.

- **processors/generator.py**
 This script will execute the discrete stages outlined above and publishes the final crosswalk file.

## Staging
### MIPS Automatic EUC Policy Fact Sheet.pdf
This is the actual policy file downloaded from QPP resource library. It is checked-in for later references and for QA team to validate the crosswalk data.

### euc_counties.csv
It is cumbersome to parse the fact sheet PDF file. So, to begin with we will manually create a CSV file with state and county names.
The example is from `2021\euc_counties.csv` which shows the structure :-
|state_code|county_name|
|----------|-----------|
|KY        |clay       |
|KY        |clay       |
|KY        |clay       |
|KY        |clay       |

#### Common Gotchas
- The fact sheet is often riddled with leading and trailing whitespace. These
  need to be stripped in the final `euc_counties.csv` file.
- Watch out for line endings on your files. They probably don't matter, but
  some `CRLF`s have crept in.
- Louisiana calls their county equivalents a `parish`.  The fact sheet may
report just the parish name, but the Census data marks the areas as parishes.
So you must manually add `parish` to any Louisiana 'counties', eg
`allen -> allen parish`.
- Tribal lands have not been matched to a zip code in the past (2022 and 2024).
Our process is to check that the counties intersecting the tribal lands are
included in the EUC fact sheet. This will prevent missing clinicians on tribal
lands.

### Census.gov Counties file
This file contains the county and its Federal Information Processing Standard (FIPS) code mapping. The file is available under "Counties" section within [Gazetteer Files](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html). Example, Gaz_counties_national.txt: [2021_Gaz_counties_national.zip](https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2021_Gazetteer/2021_Gaz_counties_national.zip).
The fields of interest to us in that file are:
| Column | Details                                                                                                                    |
|--------|----------------------------------------------------------------------------------------------------------------------------|
| USPS   | This is the 2 character State                                                                                              |
| GEOID  | This is the FIPS county code                                                                                               |
| NAME   | This is the county name. Note the name is suffixed with "County", which has to be omitted while joining with EUC policy.   |

### HUD County Zip Crosswalk file
This file maps county FIPS code and the zipcodes in the county. Example, COUNTY_ZIP_122021.xlsx is available from [HUD USPS ZIP CODE CROSSWALK](https://www.huduser.gov/portal/datasets/usps_crosswalk.html#data) (crosswalk type COUNTY-ZIP).
The column definitions are:
|Column|Column Name|Notes|
|------|-----------|-----|
| A    |county     |  FIPS code of the county |
| B    |zip     | zipcode within the county |
| D   |usps_zip_pref_state     | two character state code |


### euc_counties_zip_crosswalk.csv
This file in `data` folder contains the counties identified in EUC along with zipcodes.

