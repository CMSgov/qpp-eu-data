# Extreme and Uncontrollable County Lookup

The automatic extreme and uncontrollable circumstances (EUC) policy identifies counties affected by natural disasters and public health emergencies.
A fact sheet that summarizes policy and CMS designated counties for each performance year is available for download via [QPP resource library](https://qpp.cms.gov/resources/resource-library).
There are a few downstream data processing systems within Quality Payment Program (QPP) that require county data enriched with zip codes.
This repository publishes the county-zipcode crosswalk data in various machine-readable formats and the backoffice programs that generate them.

Refer [Developer Guide](./DEVELOPMENT.md) for more information.

## EUC Zipcode Crosswalk Publications
| File                                                                                  | Details                                      |
|---------------------------------------------------------------------------------------|----------------------------------------------|
| [2022\euc_county_zipcode_crosswalk.csv](./data/2022/euc_county_zipcode_crosswalk.csv) | The 2022 EUC County Zipcode Crosswalk file.  |
| [2023\euc_county_zipcode_crosswalk.csv](./data/2023/euc_county_zipcode_crosswalk.csv) | The 2023 EUC County Zipcode Crosswalk file.  |
| [2024\euc_county_zipcode_crosswalk.csv](./data/2024/euc_county_zipcode_crosswalk.csv) | The 2024 EUC County Zipcode Crosswalk file.  |
| [2025\euc_county_zipcode_crosswalk.csv](./data/2025/euc_county_zipcode_crosswalk.csv) | The 2024 EUC County Zipcode Crosswalk file.  |



### Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to enforce code quality checks before each commit.

###### Setup

Install pre-commit and register the hooks with git:

```sh
pip install pre-commit
pre-commit install
```

###### Run manually against all files

```sh
pre-commit run --all-files
```

Hooks configured:
- `qpp-baseline` — QPP DevOps centralized baseline checks
- `check-yaml` — validates YAML file syntax
- `end-of-file-fixer` — ensures files end with a newline
- `trailing-whitespace` — removes trailing whitespace

## Want to Contribute?

Want to file a bug or contribute some code? Read up on our guidelines for [contributing].

[contributing]: /.github/CONTRIBUTING.md

## Public Domain

This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived
through the CC0 1.0 Universal public domain dedication.

All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to
comply with this waiver of copyright interest.

See the [formal LICENSE file](/LICENSE).
