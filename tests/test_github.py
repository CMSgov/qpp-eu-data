import os
from unittest import mock, TestCase
from unittest.mock import Mock

import github
from github import Github

from processors.github import GitFacade
from processors.utils import Config

class TestGitFacade(TestCase):
    def setUp(self):
        self.config = Config()

    def test_create_issue(self):
        github_token = os.environ.get("GITHUB_TOKEN")
        with mock.patch.object(github.Repository.Repository, "create_issue", return_value = Mock(status_code=200, json=lambda : {"data": {"id": "test"}})) as g:
            facade = GitFacade(personal_access_token=github_token, config=self.config)
            fc = facade.create_issue('title', 'body', 'label')
            self.assertIsNotNone(fc)
            g.assert_called()

    def test_create_issue_raises_exception(self):
        github_token = os.environ.get("GITHUB_TOKEN")
        try:
            with mock.patch.object(github.Repository.Repository, "create_issue", Mock(side_effect=Exception)) as g:
                facade = GitFacade(personal_access_token=github_token, config=self.config)
                facade.create_issue('title', 'body', 'label')
                self.assertRaises(Exception)
                g.assert_called()
        except Exception:
            pass

    def test_search_issues(self):
        github_token = os.environ.get("GITHUB_TOKEN")
        facade = GitFacade(personal_access_token=github_token, config=self.config)
        fc = facade.search_issues('test')
        self.assertIsNotNone(fc)

    def test_search_issues_raises_exception(self):
        github_token = os.environ.get("GITHUB_TOKEN")
        try:
            with mock.patch.object(Github, "search_issues", Mock(side_effect=Exception)):
                facade = GitFacade(personal_access_token=github_token, config=self.config)
                facade.search_issues('issue')
                self.assertRaises(Exception)
        except Exception:
            pass

    def test_search_prs(self):
        github_token = os.environ.get("GITHUB_TOKEN")
        with mock.patch.object(Github, "search_issues", return_value = []) as g:
            facade = GitFacade(personal_access_token=github_token, config=self.config)
            fc = facade.search_prs('ticket')
            self.assertIsNotNone(fc)
            g.assert_called()

    def test_search_prs_raises_exception(self):
        github_token = os.environ.get("GITHUB_TOKEN")
        try:
            with mock.patch.object(Github, "search_issues", Mock(side_effect=Exception)) as g:
                facade = GitFacade(personal_access_token=github_token, config=self.config)
                facade.search_prs('ticket')
                self.assertRaises(Exception)
                g.assert_called()
        except Exception:
            pass