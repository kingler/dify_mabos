from rdflib import Graph
from owlready2 import get_ontology, World, FunctionalProperty, InverseFunctionalProperty

from typing import List
from pydantic import BaseModel, Field

class Ontology(BaseModel):
    concepts: List[str] = Field(description="Domain concepts")
    relationships: List[str] = Field(description="Relationships between concepts")

    def __init__(self, ontology_path: str = None):
        self.ontology_path = ontology_path
        self.graph = Graph()
        self.world = World()
        self.ontology = None

    def load_ontology(self, ontology_path: str = None):
        if ontology_path:
            self.ontology_path = ontology_path
        if self.ontology_path:
            self.ontology = get_ontology(self.ontology_path).load()
            self.graph = self.ontology.world.as_rdflib_graph()

    def get_classes(self):
        return list(self.ontology.classes())

    def get_properties(self):
        return list(self.ontology.properties())

    def query_ontology(self, query: str):
        from rdflib.plugins.sparql import prepareQuery
        prepared_query = prepareQuery(query)
        return self.graph.query(prepared_query)

    def generate_domain_ontology(self, user_data):
        # Generate domain-specific ontology based on user onboarding data
        domain_ontology = get_ontology("http://example.com/onboarding-ontology") 
        
        # Define classes and properties based on user data
        with domain_ontology:
            class User(domain_ontology.Thing): pass
            class BusinessModel(domain_ontology.Thing): pass
            class ProductDescription(domain_ontology.Thing): pass
            
            class hasDescription(domain_ontology.ObjectProperty):
                domain = [BusinessModel]
                range = [str]
            class belongsTo(domain_ontology.ObjectProperty):
                domain = [ProductDescription]
                range = [BusinessModel]
        
        # Create instances based on user data
        user = User(user_data['user_id'])
        business_model = BusinessModel()
        business_model.hasDescription.append(user_data['business_idea'])
        product = ProductDescription(user_data['product_service'])
        product.belongsTo.append(business_model)
        
        # Merge the domain ontology into the main graph
        self.graph += domain_ontology.world.as_rdflib_graph()
        
        # Apply custom inference rules
        self.apply_custom_inference_rules()

    def apply_custom_inference_rules(self):
        # Define custom inference rules using OWL constructs
        with self.ontology:
            # Example: Define a functional property
            class hasPrimaryGoal(self.ontology.ObjectProperty, FunctionalProperty): pass
            
            # Example: Define an inverse functional property
            class isGoalOf(self.ontology.ObjectProperty, InverseFunctionalProperty):
                inverse_property = hasPrimaryGoal
        
        # Run the reasoner to infer new facts based on the rules
        with self.ontology:
            owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(self.graph)
            
    def visualize_ontology(self):
        # Generate a visual representation of the ontology
        viz = self.ontology.world.as_digraph()
        return viz