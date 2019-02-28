"""
Created by Louis Etienne
"""

import uuid


class Log:
    def __init__(self, level, message, timestamp, request_id, user_id, other=None):
        self.id = str(uuid.uuid1())
        self.level = level
        self.message = message
        self.timestamp = timestamp
        self.request_id = request_id
        self.user_id = user_id
        self.other = other

    def __str__(self):
        return "{} - {} - {}".format(self.timestamp, self.level.upper(), self.message)

    def level_str(self):
        return self.level.upper()

    def date_str(self):
        return self.timestamp.date().strftime("%Y-%m-%d")

    def hour_str(self):
        return self.timestamp.time().strftime("%H:%M:%S.%f")[:-3]

    def timestamp_str(self):
        return self.date_str() + " " + self.hour_str()

    def message_str(self):
        return self.message

    def user_id_str(self):
        return self.user_id

    def request_id_str(self):
        return self.request_id

    def _render_other(self, template):
        buf = ""
        for key, value in self.other.items():
            buf += template.format(key, value)

        return buf

    def render(self):
        template = "<b>{}:</b> {}<br>"

        buf =  template.format("Level", self.level_str())
        buf += template.format("Date", self.date_str())
        buf += template.format("Hour", self.hour_str())
        buf += template.format("Request id", self.request_id_str())

        if self.user_id:
            buf += template.format("User id", self.user_id_str())

        buf += template.format("Message", self.message_str())
        
        if self.other and len(self.other) > 0:
            buf += self._render_other(template)

        return buf