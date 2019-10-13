"""
Created by Louis Etienne
Edited by Gregoire Henry
"""

import sys
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
        nline = 0
        with open(filename, "r") as json_file:
            for line in json_file.readlines():
                try:
                    line = json.loads(line)  # Parse json
                except json.decoder.JSONDecodeError as err:
                    print("/!\\ Impossible to load log line %d" % nline)
                    sys.exit()
                self.append_log(line)  # Append log to the LogMananger instance
                nline += 1

    def append_log(self, data):
        level = data["level"]
        message = data["message"]
        timestamp = datetime.datetime.strptime(data["timestamp"], log_timestamp_format)
        if "label" in data.keys():
            request_id = data["label"]["transactionInfo"]["requestId"]
        else:
            request_id = data
        
        path = None
        if "path" in data["label"]["transactionInfo"]:
            path = data["label"]["transactionInfo"]["path"]

        user_id = None
        if "userId" in data["label"]["transactionInfo"]:
            user_id = data["label"]["transactionInfo"]["userId"] 
                
        session_id = None
        if "sessionId" in data["label"]["transactionInfo"]:
            session_id = data["label"]["transactionInfo"]["requestId"]

        log = Log(level, message, timestamp, request_id, path, user_id, session_id)
        
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
    
    def filter_session_id(self, log_session_id):
        log_manager = LogManager()

        for log in self.logs.values():
            if log.session_id == log_session_id:
                log_manager.logs[log.id] = log

        return log_manager


    def filter_message(self, log_message):
        log_manager = LogManager()

        for log in self.logs.values():
            if log_message in log.message :
                log_manager.logs[log.id] = log

        return log_manager
