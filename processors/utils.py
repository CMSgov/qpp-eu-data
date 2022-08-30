import os
from pathlib import Path

import yaml
from pydash import strings


class Config:

    def __init__(self):
        super().__init__()
        with open(os.path.join(FileUtils.get_root(), "config.yml"), 'r') as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)

    def get_value(cls, dict, key):
        v = dict
        for p in strings.split(key, "."):
            if v is None: continue
            v = v.get(p)
        return v

    def get(self, key):
        return self.get_value(self._config, key)


class FileUtils:

    @classmethod
    def get_root(cls):
        path = Path(__file__)
        return path.parent.parent

    @classmethod
    def absolute_path(cls, folder, file_name=None):
        if not (file_name is None):
            return cls.get_root().joinpath(folder).joinpath(file_name)
        return cls.get_root().joinpath(folder)

    @classmethod
    def mkdirs(cls, path):
        Path(path).mkdir(parents=True, exist_ok=True)

from slack_sdk.webhook import WebhookClient

class SlackMessenger:

    def __init__(self, config, webhook_url, disable_notification=False):
        self.config = config
        self.disable_notification = disable_notification
        self.webhook = WebhookClient(webhook_url) if webhook_url else None

    def header_block(self, str):
        return {
            "type": "header",
            "text": {"type": "plain_text", "text": str, "emoji": True}
        }

    def section_block(self, str):
        return {
            "type": "section",
            "text": {"type": "mrkdwn", "text": str}
        }

    def divider_block(self):
        return { "type": "divider"}

    def notify(self, title, headers, messages):
        try:
            blocks = []
            if title:
                blocks.append(self.header_block(title))

            if not Utils.is_empty(headers):
                blocks.append(self.section_block(Utils.join(headers, "\n")))
                if not Utils.is_empty(messages): blocks.append(self.divider_block())

            if not Utils.is_empty(messages):
                blocks.append(self.section_block(Utils.join(messages, "\n")))

            logger.info(json.dumps(blocks))

            if not self.disable_notification and not Utils.is_empty(blocks) and self.webhook:
                response = self.webhook.send(blocks=blocks)

        except Exception as err:
            logger.error("Error during Slack messaging", err, exc_info=True)
