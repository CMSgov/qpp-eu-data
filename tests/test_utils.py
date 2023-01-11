import requests
from unittest import TestCase
from unittest import mock, TestCase
from unittest.mock import Mock

from processors.utils import Utils, APIUtils

class TestUtils(TestCase):

    def test_format_date(self):
        d = Utils.now()
        self.assertIsNotNone(Utils.format_date(d))
        self.assertIsNone(None)

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