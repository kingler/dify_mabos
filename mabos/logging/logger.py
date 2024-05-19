# mabos/logging/logger.py
from mabos.event_management.event import Event
import logging

class Logger:   


    def __init__(self, log_storage):
        self.log_storage = log_storage
        
        # Initialize log levels
        self.log_levels = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNING': 2,
            'ERROR': 3,
            'CRITICAL': 4
        }
        self.default_log_level = self.log_levels['INFO']
        
        # Initialize log formatters
        self.log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Initialize log handlers
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.log_formatter)
        self.file_handler = logging.FileHandler('mabos.log')
        self.file_handler.setFormatter(self.log_formatter)
        
        # Initialize the logger
        self.logger = logging.getLogger('mabos')
        self.logger.setLevel(self.default_log_level)
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

    def log_event(self, event: Event):
        # Log an event with relevant details
        
        log_level = self.log_levels.get(event.level, self.default_log_level)
        log_message = f"{event.message} | Event Type: {event.event_type} | Belief Updates: {event.belief_updates}"
        
        if log_level >= self.logger.level:
            if log_level == self.log_levels['DEBUG']:
                self.logger.debug(log_message)
            elif log_level == self.log_levels['INFO']:
                self.logger.info(log_message)
            elif log_level == self.log_levels['WARNING']:
                self.logger.warning(log_message)
            elif log_level == self.log_levels['ERROR']:
                self.logger.error(log_message)
            elif log_level == self.log_levels['CRITICAL']:
                self.logger.critical(log_message)

    def log_error(self, error):
        # Log an error with relevant details
        log_level = self.log_levels.get('ERROR', self.default_log_level)
        log_message = f"{error['message']} | {error.get('details', '')}"
        
        if log_level >= self.logger.level:
            self.logger.error(log_message)

    def retrieve_logs(self, event_type: str, time_range):
        # Retrieve logs of a specific event type within a given time range
        log_entries = []
        with open('mabos.log', 'r') as log_file:
            for line in log_file:
                log_entry = self._parse_log_entry(line)
                if log_entry['event_type'] == event_type and self._is_within_time_range(log_entry['timestamp'], time_range):
                    log_entries.append(log_entry)
        return log_entries
