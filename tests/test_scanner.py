from unittest import mock, TestCase
from unittest.mock import Mock
import github

from processors.scanner import Scanner
from processors.utils import Config

class TestScanner(TestCase):

    def setUp(self):
        self.config = Config()

    def test_notify_slack(self):
        scanner = Scanner(config=self.config)
        scanner.notify_slack(['channel', 'another-channel'], 'message')

    def test_check_github_issue(self):
        scanner = Scanner(config=self.config)
        with mock.patch.object(github.Repository.Repository, "create_issue", return_value = Mock(status_code=200, json=lambda : {"data": {"id": "test"}})) as g:
            scanner.check_github_issue(1, 'title')
            g.assert_called()

    def test_scan(self):
        scanner = Scanner(config=self.config)
        scanner.scan()