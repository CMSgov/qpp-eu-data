import logging
from datetime import datetime
from github import Github

from processors.utils import Utils

logger = logging.getLogger(__name__)

class GitFacade:

    def __init__(self, config, personal_access_token, server="github"):
        self.github_pat = personal_access_token
        self.config = config
        self.server = server

        self.search_threshold = Utils.get_value(config, "github.search_api_threshold")
        self.search_delay = Utils.get_value(config, "github.search_api_delay")

        m = Utils.get_value(self.config, "settings.pr_since_months")
        self.pr_since = Utils.format_date(Utils.subtract_months(datetime.now(), int(m)))

        self.g = Github(personal_access_token)

    def create_issue(self, title, body, lables):
        try:
            repo = self.g.get_repo("CMSgov/qpp-eu-data")
            return repo.create_issue(title=title, body=body, labels=lables)
        except Exception as ex:
            logger.error("error while creating issue [%s]", title, exc_info=ex)
            raise

    def search_issues(self, keyword, repo="CMSgov/qpp-eu-data"):
        try:
            logger.info("Searching issue with keyword: %s", keyword)
            return self.g.search_issues(f'is:issue repo:{repo} {keyword}')
        except Exception as ex:
            logger.error("error while searching issues for keyworkd %s in repo : %s", keyword, repo)
            raise

    def search_prs(self, ticket):
        try:
            return self.g.search_issues(f'{ticket} in:title updated:>{self.pr_since} is:pr', org="cmsGov")
        except Exception as ex:
            logger.error("error searching linked prs (ticket=%s)  (message=%s)", ticket, str(ex), exc_info=True)
            raise