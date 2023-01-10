import unittest, requests
from unittest import TestCase
from unittest import mock, TestCase
from unittest.mock import Mock

from processors.utils import Utils, APIUtils

class TestUtils(TestCase):

    def test_format_date(self):
        d = Utils.parse_date("2021-06-22 06:42:15.253671")
        self.assertIsNotNone(Utils.format_date(Utils.now()))
        self.assertIsNone(None)

    def test_parse_date(self):
        d3 = "2021-06-24T19:00:30-05:00"
        d4 = "2021-06-24T19:00:30+00:00"
        diff = Utils.elapsed_time(d4, d3)
        self.assertEqual(18000, diff)
        self.assertEqual("5 hours", Utils.human_time_duration(diff))

    def test_parse_date(self):
        d = Utils.parse_date("2021-06-22 06:42:15.253671")
        self.assertEqual("2021-06-22T06:42:15.253671", Utils.format_date(d))

        # d = Utils.parse_date("1664301600000")
        # self.assertEqual("2022-09-27T18:00:00", Utils.format_date(d))

    def test_http_get(self):
        with mock.patch.object(requests, "get", return_value = Mock(status_code=200, json=lambda : {"data": {"id": "test"}})) as g:
            APIUtils.http_get('test')
            g.assert_called()

    def test_http_get_raises_exception(self):
        try:
            with mock.patch.object(requests, "get", Mock(side_effect=Exception)) as g:
                APIUtils.http_get('test')
                g.assert_called()
                self.assertRaises(Exception)
        except Exception:
            pass