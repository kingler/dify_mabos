# mabos/communication/broker.py
from .message_storage import MessageStorage
from mabos.logging.logger import Logger
from mabos.configuration.configuration_manager import ConfigurationManager
from queue import PriorityQueue
from threading import Lock
from mabos.monitoring.monitoring import MonitoringManager

class Broker:
    def __init__(self):
        self.agent_locations = {}
        self.agent_roles = {}
        self.agent_goals = {}
        self.message_queue = PriorityQueue()
        self.message_storage = MessageStorage()
        self.logger = Logger()
        self.config_manager = ConfigurationManager()
        self.cache = {}
        self.lock = Lock()
        self.topic_subscriptions = {}
        self.monitoring_manager = MonitoringManager(self.agents)

    def register_agent(self, agent_id, location, role, goals):
        self.agent_locations[agent_id] = location
        self.agent_roles[agent_id] = role
        self.agent_goals[agent_id] = goals

    def subscribe_to_topic(self, agent_id, topic):
        if topic not in self.topic_subscriptions:
            self.topic_subscriptions[topic] = set()
        self.topic_subscriptions[topic].add(agent_id)

    def unsubscribe_from_topic(self, agent_id, topic):
        if topic in self.topic_subscriptions:
            self.topic_subscriptions[topic].discard(agent_id)
            if not self.topic_subscriptions[topic]:
                del self.topic_subscriptions[topic]

    def route_message(self, sender, recipient, message, topic=None):
        if topic:
            # Broadcast message to all agents subscribed to the topic
            if topic in self.topic_subscriptions:
                for subscriber in self.topic_subscriptions[topic]:
                    self._route_message_to_agent(sender, subscriber, message)
        else:
            # Send message to a specific recipient
            self._route_message_to_agent(sender, recipient, message)
            self.monitoring_manager.log_communication(sender, recipient, message)

    def _route_message_to_agent(self, sender, recipient, message):
        if recipient in self.agent_locations:
            with self.lock:
                if recipient in self.cache:
                    recipient_location = self.cache[recipient]
                else:
                    recipient_location = self.agent_locations[recipient]
                    self.cache[recipient] = recipient_location
            
            priority = self._calculate_priority(sender, recipient, message)
            self.message_queue.put((priority, message))
            self._send_message(recipient_location, message)
            self._wait_for_acknowledgment(message)
        else:
            raise ValueError(f"Recipient {recipient} not registered with the broker")

    def _calculate_priority(self, sender, recipient, message):
        sender_role = self.agent_roles[sender]
        recipient_role = self.agent_roles[recipient]
        sender_goals = self.agent_goals[sender]
        recipient_goals = self.agent_goals[recipient]
        # Calculate priority based on agent roles and goals
        # Higher priority for messages between agents with matching roles and goals
        priority = 1
        if sender_role == recipient_role:
            priority += 1
        if set(sender_goals) & set(recipient_goals):
            priority += 1
        return priority

    def _send_message(self, recipient_location, message):
        # Send message to the recipient's location
        # Implement load balancing if multiple locations are available
        pass

    def _wait_for_acknowledgment(self, message):
        # Wait for acknowledgment from the recipient
        # Resend message if acknowledgment is not received within a timeout
        pass