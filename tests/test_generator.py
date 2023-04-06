from unittest import mock, TestCase

from processors.generator import Generator
from processors.utils import Config


class TestIntaker(TestCase):

    def setUp(self):
        self.config = Config()

    def test_load_hud_county_zip(self):
        generator = Generator(self.config, 2022)
        self.assertEqual(54260, generator.load_hud_county_zip().shape[0])

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
        Ensure that the hardcoded euc counties is not accidently modified.
        :return:
        """
        generator = Generator(self.config, 2022)
        df = generator.load_df("qpp_euc_counties")
        cnt = df.shape[0]
        self.assertEqual(220, cnt, f'the count must be same (18, {cnt})')
        self.assertEqual(2, df.shape[1], f'the columns must be same (2,{df.shape[1]})')