import networkx as nx

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        
    def build_graph(self, ontology_manager: OntologyManager):
        # Construct knowledge graph from loaded ontologies
        pass
    
    def add_node(self, node_id: str, node_data: dict):
        self.graph.add_node(node_id, **node_data)
        
    def add_edge(self, source_id: str, target_id: str, edge_data: dict):
        self.graph.add_edge(source_id, target_id, **edge_data)
        
    def get_node(self, node_id: str):
        return self.graph.nodes[node_id]
    
    def get_neighbors(self, node_id: str):
        return list(self.graph.neighbors(node_id))