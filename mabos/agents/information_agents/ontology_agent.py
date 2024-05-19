# mabos/agents/ontology_agent.py
from ...communication.broker import Broker
from ...knowledge_management.core.knowledge_base import KnowledgeBase
from ...knowledge_management.ontology.ontology import Ontology 
from ...communication.communication import AgentCommunication
from ...logging.logger import Logger
from ...communication.message_storage import MessageStorage
from ...error_handler import ErrorHandler

class OntologyAgent:
    def __init__(self, location):
        self.location = location
        self.broker = Broker()
        self.knowledge_base = KnowledgeBase()
        self.communication = AgentCommunication(self, self.knowledge_base)
        self.error_handler = ErrorHandler()
        self.message_storage = MessageStorage()
        self.logger = Logger()
        self.ontology = Ontology()

    def generate_ontology(self, business_domain):
        # Load the meta-ontology
        self.ontology.load_ontology("path/to/meta_ontology.ttl")
        # Create a domain-specific ontology based on the Business Model Canvas ontology
        ontology = {
            "concepts": [],
            "relations": [],
            "axioms": []
        }
        
        # Define key concepts from the Business Model Canvas ontology
        bmc_concepts = [
            {"name": "Value Proposition", "attributes": ["product_service", "value_added", "customer_needs"]},
            {"name": "Customer Segment", "attributes": ["segment_type", "needs", "characteristics"]},
            {"name": "Channel", "attributes": ["channel_type", "function", "customer_interaction"]},
            {"name": "Customer Relationship", "attributes": ["relationship_type", "purpose", "interaction_level"]},
            {"name": "Revenue Stream", "attributes": ["stream_type", "pricing_mechanism", "payment_method"]},
            {"name": "Key Resource", "attributes": ["resource_type", "quantity", "ownership"]},
            {"name": "Key Activity", "attributes": ["activity_type", "purpose", "value_creation"]},
            {"name": "Key Partnership", "attributes": ["partner_type", "purpose", "agreement"]},
            {"name": "Cost Structure", "attributes": ["cost_type", "amount", "frequency"]}
        ]
        
        # Add Business Model Canvas concepts to the domain ontology
        for concept in bmc_concepts:
            self.ontology.add_concept(concept["name"], concept["attributes"])
        
        # Define relations between Business Model Canvas concepts
        bmc_relations = [
            {"name": "targets", "domain": "Value Proposition", "range": "Customer Segment"},
            {"name": "reaches", "domain": "Channel", "range": "Customer Segment"},
            {"name": "establishes", "domain": "Customer Relationship", "range": "Customer Segment"},
            {"name": "generates", "domain": "Value Proposition", "range": "Revenue Stream"},
            {"name": "requires", "domain": "Value Proposition", "range": "Key Resource"},
            {"name": "requires", "domain": "Value Proposition", "range": "Key Activity"},
            {"name": "enhances", "domain": "Key Partnership", "range": "Key Resource"},
            {"name": "performs", "domain": "Key Partnership", "range": "Key Activity"},
            {"name": "incurs", "domain": "Key Resource", "range": "Cost Structure"},
            {"name": "incurs", "domain": "Key Activity", "range": "Cost Structure"}
        ]
        
        # Add Business Model Canvas relations to the domain ontology
        for relation in bmc_relations:
            self.ontology.add_relation(relation["name"], relation["domain"], relation["range"])
        
        # Define axioms or rules based on the Business Model Canvas ontology
        bmc_axioms = [
            "Every Value Proposition must target at least one Customer Segment",
            "Every Customer Segment must be reached by at least one Channel",
            "Every Customer Segment must have an established Customer Relationship",
            "Every Value Proposition must generate at least one Revenue Stream",
            "Every Value Proposition requires Key Resources and Key Activities",
            "Key Partnerships can enhance Key Resources and perform Key Activities",
            "Key Resources and Key Activities incur Costs in the Cost Structure"
        ]
        
        # Add Business Model Canvas axioms to the domain ontology
        for axiom in bmc_axioms:
            self.ontology.add_axiom(axiom)

        # Merge the domain ontology with the meta-ontology
        self.ontology.graph += ontology

        # Apply custom inference rules from the meta-ontology
        self.ontology.apply_custom_inference_rules()

        # Visualize the generated ontology
        ontology_visualization = self.ontology.visualize_ontology()

        # Store the generated ontology in the knowledge base
        self.knowledge_base.store_ontology(ontology)

        return ontology


    def send_message(self, recipient, message):
        if recipient.location == self.location:
            # If the recipient is in the same location, send the message directly
            recipient.receive_message(self, message)
        else:
            # If the recipient is in a different location, route the message through the broker
            self.broker.route_message(self, recipient, message)