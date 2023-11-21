from unittest import mock, TestCase

from processors.generator import Generator
from processors.utils import Config


class TestIntaker(TestCase):

    def setUp(self):
        self.config = Config()

    def test_load_hud_county_zip(self):
        year_count_pairs = [(2022, 54260), (2023, 54446)]
        for year, expected_count in year_count_pairs:
            generator = Generator(self.config, year)
            self.assertEqual(expected_count, generator.load_hud_county_zip().shape[0])

    def test_canonicalize_state_code(self):
        """
        Ensure that state names are canonicalized properly.
        :return:
        """
        generator = Generator(self.config, 2022)
        self.assertEqual('PA', generator.canonicalize_state_code("PA"))
        self.assertEqual('PA', generator.canonicalize_state_code("pa"))
        self.assertEqual('PA', generator.canonicalize_state_code("Pa"))

    def test_canonicalize_county_name(self):
        """
        Ensure that county names are canonicalized properly.
        :return:
        """
        generator = Generator(self.config, 2022)
        self.assertEqual('fairfax', generator.canonicalize_county_name("Fairfax County"))
        self.assertEqual('culebra', generator.canonicalize_county_name("Culebra Municipio"))
        self.assertEqual('san sebastian', generator.canonicalize_county_name("San Sebastián Municipio"))
        self.assertEqual('anchorage', generator.canonicalize_county_name("Anchorage Municipality"))

    def test_load_df(self):
        """
        Ensure that the hardcoded euc counties is not accidentally modified.
        :return:
        """
        year_count_pairs = [(2022, 220), (2023, 93)]
        for year, expected_count in year_count_pairs:
            generator = Generator(self.config, year)
            df = generator.load_df("qpp_euc_counties")
            cnt = df.shape[0]
            self.assertEqual(expected_count, cnt, f'the count must be same ({expected_count}, {cnt})')
            self.assertEqual(2, df.shape[1], f'the columns must be same (2,{df.shape[1]})')