from owlready2 import *

class OntologyManager:
    def __init__(self):
        self.ontologies = []
        
    def load_ontology(self, ontology_path: str):
        onto = get_ontology(ontology_path).load()
        self.ontologies.append(onto)
        
    def get_classes(self):
        classes = []
        for onto in self.ontologies:
            classes.extend(list(onto.classes()))
        return classes
    
    def get_properties(self):
        properties = []
        for onto in self.ontologies:
            properties.extend(list(onto.properties()))
        return properties
    
    def query_ontology(self, query: str):
        # Execute SPARQL query on loaded ontologies
        pass