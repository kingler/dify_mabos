# mabos/agents/onboarding_agent.py
from ...communication.broker import Broker
from ...communication.message_storage import MessageStorage
from ...logging.logger import Logger
from ...communication.message_encryptor import MessageEncryptor
from ..information_agents.data_management_agent import DataManagementAgent
from ..coordinator_agents.business_process_manager import BusinessProcessManager
from ..information_agents.ontology_agent import OntologyAgent

class OnboardingAgent:
    def __init__(self, location, data_store):
        self.location = location
        self.broker = Broker()
        self.message_storage = MessageStorage()
        self.logger = Logger()
        self.message_encryptor = MessageEncryptor()
        self.data_management_agent = DataManagementAgent(data_store)
        self.business_process_manager = BusinessProcessManager(self.broker)
        self.ontology_agent = OntologyAgent(location)

    def onboard_user(self, user_data):
        # Guide user through onboarding process
        print("Welcome to the onboarding process!")
        print("We will guide you through setting up your business.")
        
        # Collect necessary information
        business_name = input("Enter your business name: ")
        business_type = input("Enter your business type: ")
        business_address = input("Enter your business address: ")
        business_phone = input("Enter your business phone number: ")
        business_email = input("Enter your business email: ")
        
        # Set up initial configuration for the business
        initial_config = {
            "name": business_name,
            "type": business_type,
            "address": business_address,
            "phone": business_phone,
            "email": business_email
        }
        
        # Generate business domain ontology using the ontology agent
        business_domain_ontology = self.ontology_agent.generate_ontology(business_type)
        
        # Store the business domain ontology in the knowledge base
        self.ontology_agent.knowledge_base.store_ontology(business_domain_ontology)
        
        print("Initial configuration for your business:")
        print(initial_config)
        print("Onboarding process completed successfully!")
        pass

    def send_message(self, recipient, message):
        if recipient.location == self.location:
            # If the recipient is in the same location, send the message directly
            recipient.receive_message(self, message)
        else:
            # If the recipient is in a different location, route the message through the broker
            broker = Broker()
            broker.route_message(self, recipient, message)
        pass