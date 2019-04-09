"""
Created by Louis Etienne
Edited by Gregoire Henry
"""

import datetime
import json

from sources.core.Log import Log
from sources.constants import log_timestamp_format


class LogManager:
    def __init__(self, filename=None):
        self.logs = {}
        
        if filename:
            self.load_file(filename)

    def load_file(self, filename):
        i = 0
        with open(filename, "r") as json_file:
                for line in json_file.readlines():
                    line = json.loads(line)  # Parse json
                    self.append_log(line)  # Append log to the LogMananger instance
    def append_log(self, data):
        level = data.pop("level")
        message = data.pop("message")
        timestamp = datetime.datetime.strptime(data.pop("timestamp"), log_timestamp_format)
        if "label" in data.keys():
            request_id = data.pop("label")["transactionInfo"]["requestId"]
        else:
            request_id = data
        
        user_id = None
        if "userId" in data:
            user_id = data.pop("userId")

        log = Log(level, message, timestamp, request_id, user_id)
        
        self.logs[log.id] = log

    def count(self, log_level=None):
        if not log_level:
            return len(self.logs)
        else:
            return len(self.filter_level(log_level).logs)

    def filter_id(self, log_id):
        log_manager = LogManager()

        for log in self.logs.values():
            if log.id == log_id:
                log_manager.logs[log.id] = log

        return log_manager

    def filter_level(self, log_level):
        log_manager = LogManager()

        for log in self.logs.values():
            if log.level == log_level:
                log_manager.logs[log.id] = log

        return log_manager

    def filter_request_id(self, log_request_id):
        log_manager = LogManager()

        for log in self.logs.values():
            if log.request_id == log_request_id:
                log_manager.logs[log.id] = log

        return log_manager
