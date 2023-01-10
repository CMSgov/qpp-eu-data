import os, logging
from datetime import datetime, timedelta
from processors.github import GitFacade
from processors.utils import APIUtils
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)

class Scanner:

    def __init__(self, config):
        super().__init__()
        self.config = config
        github_token = os.environ.get("GITHUB_TOKEN")
        self.git_facade = GitFacade(self.config, personal_access_token=github_token)

    def notify_slack(self, channels, message):
        slack_token = os.environ.get("SLACK_APP_TOKEN")
        try:
            for channel in channels:
                client = WebClient(slack_token)
                client.chat_postMessage(channel=channel, text=message)
                logger.info(f'Slack Notification Successful to channel {channel} with message - {message}')
        except SlackApiError as err:
            assert err.response["ok"] is False
            assert err.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            logger.error(f"Slack Notification Error: {err.response['error']}", exc_info=True)

    def check_github_issue(self, doc_id, title):
        issue_title = f'{title} document updated - {doc_id}'
        issues = self.git_facade.search_issues(issue_title)
        if issues.totalCount == 0:
            # Create Github issue to verify the updated document.
            logging.info(f'issue not found for {doc_id}. new issue will be created and slack will be notified.')
            new_issue = self.git_facade.create_issue(issue_title, f'EUC Document Updated.  Please verify!', ['enhancement'])
            logging.info("Issue created %s", new_issue)
            
            # Notify Slack Channels about the new updated document
            channels = self.config.get('scanner.slack_notify_channels')
            self.notify_slack(channels, f'{issue_title}.  Please verify!')
        elif issues.totalCount > 0:
            for issue in issues:
                logging.info(f'Issue Exists for {doc_id}.  Issue Info - {issue}')

    def search_documents(self, json_data, search_title, last_update_date):
        try:
            logger.info("Searching documents with last update date on or after: %s", last_update_date)
            documents = [data for data in json_data 
                if data['resourceTypes'] == 'Fact Sheets' 
                and f'{search_title}' in data['title'] 
                and datetime.strptime(data['lastUpdated'], "%m/%d/%Y").date() >= last_update_date
            ]
            return documents
        except Exception:
            logger.error("error while searching documents with last update date on or after: %s", last_update_date)
            raise

    def scan(self):
        try:
            search_title = self.config.get('scanner.search_title')
            resources_api = self.config.get('scanner.resource_lib_url')
            last_update_duration = self.config.get('scanner.last_update_duration')
            last_update_date = datetime.today() - timedelta(days=last_update_duration)

            response = APIUtils.http_get(resources_api)
            documents = self.search_documents(response['resources'], search_title, last_update_date.date())

            for document in documents:
                self.check_github_issue(document["nId"], search_title)
            if documents == []:
                logging.info('No documents updated within the given date range!')

        except Exception as ex:
            logging.error(ex)