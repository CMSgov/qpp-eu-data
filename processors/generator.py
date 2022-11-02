import pandas as pd
import logging

from pydash import strings

from processors.utils import FileUtils, Utils

logger = logging.getLogger(__name__)

class Generator:

    def __init__(self, config, year):
        super().__init__()
        self.config = config
        self.year = year

    def generate(self):
        """
        Will generate the data files.
        :return:
        """
        euc_counties = self.load_qpp_euc_counties() # contains county name
        census_counties = self.load_census_counties() # contains county name and fips
        hud_crosswalk = self.load_hud_county_zip() # contains county-fips and zipcode
        # hud_crosswalk['zipcode'] = hud_crosswalk['zipcode'].apply(self.canonicalize_zip_code)
        print(census_counties.head(3171))


        # state, county, county-fips
        euc_counties_fips = euc_counties.merge(census_counties, on=["state_code", "county_name"], how="left")

        #state, county, county_fips, zipcode
        county_zip_crosswalk = euc_counties_fips.merge(hud_crosswalk, on=["county_fips"], how="left")
        # state, county , zipcode
        county_zip_crosswalk.drop(columns=["county_fips", "hud_state_code"], axis = 1, inplace=True)

        # publish data files
        self.publish(county_zip_crosswalk)



    def publish(self, df):
        data_folder = f'{self.config.get("data.folder")}/{self.year}/'
        FileUtils.mkdirs(FileUtils.absolute_path(data_folder))
        csv_filename = self.config.get('data.filename')
        df.to_csv(FileUtils.absolute_path(data_folder, csv_filename), index=False)

    def load_df(self, key):
        staging_folder = self.config.get('staging.folder')
        c = self.config.get(f'generator.{self.year}.{key}')
        format = c.get('format')
        fields = c.get('fields')
        dtypes = {}
        for f in fields:
            dtypes[f] = object
        file = FileUtils.absolute_path(f'{staging_folder}/{self.year}/', c.get('filename'))
        df = None
        if format == 'csv':
            df = pd.DataFrame(pd.read_csv(file, usecols=fields, dtype=dtypes))
        elif format == 'tsv':
            df = pd.DataFrame(pd.read_csv(file, header = 0, sep='\t', usecols=fields, dtype=dtypes))
        elif format == 'xlsx' or format == 'excel':
            df = pd.DataFrame(pd.read_excel(file, usecols=fields, dtype=dtypes))
        df = df.astype(str)
        if c.get('rename_columns'):
            df.rename(columns= c.get('rename_columns'), inplace=True)
        return df

    def load_census_counties(self):
        df = self.load_df('census_gov_counties')
        df["county_name"] = df["county_name"].apply(self.canonicalize_county_name)
        df["state_code"] = df["state_code"].apply(self.canonicalize_state_code)
        return df

    def load_qpp_euc_counties(self):
        df = self.load_df('qpp_euc_counties')
        df["county_name"] = df["county_name"].apply(self.canonicalize_county_name)
        df["state_code"] = df["state_code"].apply(self.canonicalize_state_code)
        return df

    def load_hud_county_zip(self):
        df = self.load_df('udh_county_zip_crosswalk')
        df["hud_state_code"] = df["hud_state_code"].apply(self.canonicalize_state_code)
        return df

    def canonicalize_state_code(self, s):
        return strings.trim(strings.upper_case(s))

    def canonicalize_county_name(self, s):
        s1 = Utils.remove_all(s, ['county', 'municipio', 'municipality', 'census area', 'city and borough', 'borough'])
        s1 = Utils.remove_accents(s1)
        return strings.trim(strings.lower_case(s1))
