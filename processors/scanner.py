from slack_sdk.webhook import WebhookClient
import logging

logger = logging.getLogger(__name__)

class Scanner:

    def __init__(self, config, year):
        super().__init__()
        self.config = config
        pass

    def notify(self, webhook_url, header, message):
        slack = WebhookClient(webhook_url) if webhook_url else None
        try:
            pass
        except Exception as err:
            logger.error("Error during Slack messaging", err, exc_info=True)

    def get_euc_factsheet_info(self):
        """
        Will look at last changed meta-data associated with EUC Policy Factsheet and determines if crosswalk file in data/<year>/ require modificaitons.
        :return:
        """
        pass

    def scan(self):
        """
        Will scan QPP resource repository for EUC policy factsheet updates.
        :return:
        """
        pass
