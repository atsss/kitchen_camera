import network
import urequests
import config

class Slack:
    def __init__(self):
        self._hook_url = config.slack_config["hook_url"]

    def send_message(self, message: str) -> bool:
        data = {
                "link_names": 1,
                "icon_url": ":ghost:",
                "username": "ESP32S3",
                "text": message
               }
        res = urequests.post(self._hook_url, json=data)
        return res.status_code == 200
