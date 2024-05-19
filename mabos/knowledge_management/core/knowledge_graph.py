import networkx as nx
from ..ontology.ontology import Ontology
from rdflib import URIRef, Literal

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        
    def build_graph(self, ontology: Ontology):
        for subject, predicate, obj in ontology.graph.triples((None, None, None)):
            subject_id = str(subject)
            object_id = str(obj)
            
            # Add nodes with their respective classes from the ontology
            self.graph.add_node(subject_id, type=self.get_node_type(subject, ontology))
            self.graph.add_node(object_id, type=self.get_node_type(obj, ontology))
            
            # Add edge with the predicate as the edge data
            self.graph.add_edge(subject_id, object_id, predicate=str(predicate))
            
            # Add data properties as node attributes
            if isinstance(obj, Literal):
                self.graph.nodes[subject_id][str(predicate)] = str(obj)
    
    def get_node_type(self, node, ontology):
        for node_class in ontology.get_classes():
            if (node, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), node_class) in ontology.graph:
                return str(node_class)
        return None
    
    def add_node(self, node_id: str, node_data: dict):
        self.graph.add_node(node_id, **node_data)
        
    def add_edge(self, source_id: str, target_id: str, edge_data: dict):
        self.graph.add_edge(source_id, target_id, **edge_data)
        
    def get_node(self, node_id: str):
        return self.graph.nodes[node_id]
    
    def get_neighbors(self, node_id: str):
        return list(self.graph.neighbors(node_id))