from unittest import mock, TestCase

from processors.generator import Generator
from processors.utils import Config


class TestIntaker(TestCase):

    def setUp(self):
        self.config = Config()

    def test_load_df(self):
        """
        Ensure that the hardcoded euc counties is not accidently modified.
        :return:
        """
        generator = Generator(self.config, 2022)
        df = generator.load_df("qpp_euc_counties")
        cnt = df.shape[0]
        self.assertEqual(18, cnt, f'the count must be same (18, {cnt})')
        self.assertEqual(2, df.shape[1], f'the columns must be same (2,{df.shape[1]})')
        pass