# mabos/communication/delayed_message_queue.py
from .broker import Broker

class DelayedMessageQueue:
    def __init__(self):
        self.queue = []
        self.max_queue_size = 100
        self.batch_size = 10
        self.message_delay = 5  # seconds
        self.broker = Broker()

    def enqueue_message(self, message):
        self.queue.append(message)

    def send_batch(self):
        batch_messages = []
        while self.queue:
            message = self.queue.pop(0)
            batch_messages.append(message)
        
        for message in batch_messages:
            recipient = message["recipient"]
            content = message["content"]
            self.broker.route_message(self, recipient, content)