
## Metadata Files for Generating euc_county_zipcode_crosswalk.csv

To generate the `euc_county_zipcode_crosswalk.csv` file, you'll need the following metadata files:

- **[euc_counties.csv](./euc_counties.csv): County Names and States**

  Create a file manually by extracting county names and states from the EUC
  policy. Refer to the
  [2024-MIPS-Automatic-EUC-Policy-Clean.docx](https://github.com/CMSgov/qpp-eu-data/tree/main/staging/2024/2024-MIPS-Automatic-EUC-Policy-Clean.docx)
  for the 2024 Merit-based Incentive Payment System Automatic Extreme and
  Uncontrollable Circumstances Policy.

  > [!NOTE]
  > This file is normally a `.pdf` file downloaded from the qpp documents page, but
  this year it was provided as a `.docx` emailed to Shane Dougherty.

- **[National Counties Gazetteer File](./2024_Gaz_counties_national.txt): FIPS Codes**

  Enrich each county with its corresponding FIPS code. Obtain the National
  Counties Gazetteer File for 2024 from [Census.gov](https://www.census.gov).
  Match the county and state to retrieve the FIPS code.

- **[HUD USPS ZIP CODE CROSSWALK](./COUNTY_ZIP_092024.xlsx): Zip Codes**
  Enrich each county with zip codes. Obtain the data from the
  [HUD USPS ZIP CODE CROSSWALK](https://www.huduser.gov/portal/datasets/usps_crosswalk.html#data),
  specifically from the 3rd quarter of 2024.

For detailed documentation on how to generate the `euc_county_zipcode_crosswalk.csv`
file, please refer to the [DEVELOPMENT.md](https://github.com/CMSgov/qpp-eu-data/blob/main/DEVELOPMENT.md)
file in the [qpp-eu-data](https://github.com/CMSgov/qpp-eu-data) repository.