# mabos/communication/error_handler.py
import time
from .communication.communication import CommunicationFailure

class ErrorHandler:
    def handle_communication_failure(self, recipient, message, exception):
        try:
            # Attempt to send the message
            self.broker.route_message(self, recipient, message)
        except CommunicationFailure as e:
            # Log the communication failure
            self.logger.log_error(f"Communication failure: {str(e)}")
            
            # Retry sending the message with exponential backoff
            retry_count = 0
            max_retries = 3
            while retry_count < max_retries:
                try:
                    self.broker.route_message(self, recipient, message)
                    break  # Message sent successfully, exit the retry loop
                except CommunicationFailure:
                    retry_count += 1
                    delay = 2 ** retry_count  # Exponential backoff delay
                    time.sleep(delay)
            
            if retry_count == max_retries:
                # Maximum retries reached, store the message for later retry
                self.message_storage.store_failed_message(message)

    def retry_communication(self, message, max_retries):
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.broker.route_message(self, message["recipient"], message["content"])
                break  # Message sent successfully, exit the retry loop
            except CommunicationFailure:
                retry_count += 1
                delay = 2 ** retry_count  # Exponential backoff delay
                time.sleep(delay)
        
        if retry_count == max_retries:
            # Maximum retries reached, store the message for later retry
            self.message_storage.store_failed_message(message)

    def log_error(self, error):
        self.logger.log_error(error)
        # Log additional details for debugging
        self.logger.log_debug(f"Error occurred in {self.__class__.__name__}")
        self.logger.log_debug(f"Error details: {str(error)}")
