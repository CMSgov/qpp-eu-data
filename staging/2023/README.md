## Metadata Files for Generating euc_county_zipcode_crosswalk.csv

To generate the `euc_county_zipcode_crosswalk.csv` file, you'll need the following metadata files:

- **euc_counties.csv: County Names and States**  
  Create a file manually by extracting county names and states from the EUC policy. Refer to the [2023MIPSAutoEUCPolicyFactSheet.pdf](https://github.com/CMSgov/qpp-eu-data/tree/main/staging/2023/2023MIPSAutoEUCPolicyFactSheet.pdf) for the 2023 Merit-based Incentive Payment System Automatic Extreme and Uncontrollable Circumstances Policy.

- **National Counties Gazetteer File: FIPS Codes**  
  Enrich each county with its corresponding FIPS code. Obtain the National Counties Gazetteer File for 2022 from [Census.gov](https://www.census.gov). Match the county and state to retrieve the FIPS code.

- **HUD USPS ZIP CODE CROSSWALK: Zip Codes**  
  Enrich each county with zip codes. Obtain the data from the [HUD USPS ZIP CODE CROSSWALK](https://www.huduser.gov/portal/datasets/usps_crosswalk.html#data), specifically from the 4th quarter of 2022.

For detailed documentation on how to generate the `euc_county_zipcode_crosswalk.csv` file, please refer to the [DEVELOPMENT.md](https://github.com/CMSgov/qpp-eu-data/blob/main/DEVELOPMENT.md) file in the [qpp-eu-data](https://github.com/CMSgov/qpp-eu-data) repository.