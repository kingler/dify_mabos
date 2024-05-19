from typing import Dict, Any, List
import asyncio
from ..agents.agent import Agent
from ..task_management.task import Task
from ..knowledge_management.knowledge_base import KnowledgeBase
from ..knowledge_management.ontology.ontology import Ontology
from ..communication.negotiation.contract_net_protocol import ContractNetProtocol
from ..communication.negotiation.auction_based_negotiation import AuctionBasedNegotiation
from ..communication.group_formation import GroupFormation
from mabos.monitoring.monitoring import MonitoringManager

class AgentCommunication:
    def __init__(self, agent: Agent, knowledge_base: KnowledgeBase, ontology: Ontology):
        self.agent = agent
        self.knowledge_base = knowledge_base
        self.ontology = ontology
        self.contract_net_protocol = ContractNetProtocol(self)
        self.auction_based_negotiation = AuctionBasedNegotiation(self)
        self.group_formation = GroupFormation(self)
        self.subscribed_topics = []
        self.monitoring_manager = MonitoringManager([agent])

    def send_message(self, recipient: Agent, message: Dict[str, Any]):
        """
        Send a message to another agent using enhanced FIPA ACL protocol.
        
        Args:
            recipient: The recipient agent.
            message: The message content, formatted according to enhanced FIPA ACL.
        """
        # Implement message sending logic based on enhanced FIPA ACL
        # This could involve serializing the message, establishing a connection,
        # and sending the message over a network or message queue.
        # Serialize the message content
        serialized_message = self.serialize_message(message)

        # Establish a connection with the recipient agent
        connection = self.establish_connection(recipient)

        # Send the serialized message over the established connection
        self.send_over_connection(connection, serialized_message)
        # Close the connection
        self.close_connection(connection)
        
        self.monitoring_manager.log_communication(self.agent.agent_id, recipient.agent_id, message)
        self.monitoring_manager.metrics_collector.update_metric('communication', 'sent_messages', 1)
        
        pass

    def receive_message(self, sender: Agent, message: Dict[str, Any]):
        """
        Receive a message from another agent using enhanced FIPA ACL protocol.
        
        Args:
            sender: The sender agent.
            message: The received message content, formatted according to enhanced FIPA ACL.
        """
        # Deserialize the received message
        deserialized_message = self.deserialize_message(message)

        # Interpret the message content based on enhanced FIPA ACL
        message_type = deserialized_message.get("performative")
        message_content = deserialized_message.get("content")

        # Trigger appropriate actions or responses based on the message type and content
        if message_type == "request":
            self.handle_request(sender, message_content)
        elif message_type == "inform":
            self.handle_inform(sender, message_content)
        elif message_type == "query":
            self.handle_query(sender, message_content)
        elif message_type == "propose":
            self.handle_proposal(sender, message_content)
        elif message_type == "counter-propose":
            self.handle_counter_proposal(sender, message_content)
        elif message_type == "agree":
            self.handle_agreement(sender, message_content)
        # Add more message type handling as needed

        # Update the agent's knowledge base or beliefs based on the received message
        self.update_knowledge_base(deserialized_message)
        
        self.monitoring_manager.log_communication(sender.agent_id, self.agent.agent_id, message)
        self.monitoring_manager.metrics_collector.update_metric('communication', 'received_messages', 1)

    async def send_message_async(self, recipient: Agent, message: Dict[str, Any]):
         # Implement asynchronous message sending logic
         # Serialize the message content
         serialized_message = self.serialize_message(message)

         # Establish a connection with the recipient agent asynchronously
         connection = await self.establish_connection_async(recipient)

         # Send the serialized message over the established connection asynchronously
         await self.send_over_connection_async(connection, serialized_message)

         # Close the connection
         await self.close_connection_async(connection)
     
    async def process_message_async(self, message: Dict[str, Any]):
         # Process messages asynchronously without blocking execution
         # Process the message asynchronously
         asyncio.create_task(self.handle_message(message))

    def broadcast_message(self, message: Dict[str, Any]):
        """
        Broadcast a message to all known agents using enhanced FIPA ACL protocol.
        
        Args:
            message: The message content, formatted according to enhanced FIPA ACL.
        """
        # Implement message broadcasting logic based on enhanced FIPA ACL
        # This could involve iterating over all known agents and sending the message to each one.
        for agent in self.get_known_agents():
            self.send_message(agent, message)
        
    def publish_message(self, topic: str, message: Dict[str, Any]):
        """
        Publish a message to a specific topic using enhanced FIPA ACL protocol.
        
        Args:
            topic: The topic to publish the message to.
            message: The message content, formatted according to enhanced FIPA ACL.
        """
        # Implement message publishing logic based on enhanced FIPA ACL
        # This could involve sending the message to a message broker or a topic-based communication channel.
        self.message_broker.publish(topic, message)

    def subscribe_to_topic(self, topic: str):
        """
        Subscribe to a specific topic to receive related messages.
        
        Args:
            topic: The topic to subscribe to.
        """
        if topic not in self.subscribed_topics:
            self.subscribed_topics.append(topic)
            # Register the agent's interest in the topic with the message broker
            self.message_broker.subscribe(self, topic)
        

    def unsubscribe_from_topic(self, topic: str):
        """
        Unsubscribe from a specific topic to stop receiving related messages.
        
        Args:
            topic: The topic to unsubscribe from.
        """
        if topic in self.subscribed_topics:
            self.subscribed_topics.remove(topic)
            # Unregister the agent's interest in the topic with the message broker
            self.message_broker.unsubscribe(self, topic)
    
    def send_task_output(self, recipient: Agent, task: Task):
        message = {
            "performative": "inform",
            "content": task.output
        }
        self.send_message(recipient, message)
        
    def receive_task_output(self, sender: Agent, message: Dict[str, Any]):
        task_output = message["content"]
        self.agent.knowledge_base.update(task_output)
        self.agent.beliefs.update(task_output)

    def initiate_contract_net_protocol(self, task: Task, participants: List[Agent]):
        self.contract_net_protocol.initiate(task, participants)

    def participate_in_contract_net_protocol(self, initiator: Agent, cfp: Dict[str, Any]):
        self.contract_net_protocol.participate(initiator, cfp)

    def initiate_auction(self, item: Dict[str, Any], participants: List[Agent]):
        self.auction_based_negotiation.initiate_auction(item, participants)

    def participate_in_auction(self, auctioneer: Agent, item: Dict[str, Any]):
        self.auction_based_negotiation.participate_in_auction(auctioneer, item)

    def form_group(self, participants: List[Agent], group_goal: str):
        self.group_formation.form_group(participants, group_goal)

    def join_group(self, initiator: Agent, group_goal: str):
        self.group_formation.join_group(initiator, group_goal)

    def collaborate_with_group(self, group_members: List[Agent], group_goal: str):
        # Implement collaborative decision-making and task allocation within the group
        pass