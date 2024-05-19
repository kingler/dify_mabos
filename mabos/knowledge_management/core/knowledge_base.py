from ..ontology.ontology import Ontology
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD
from ..utils.indexing import IndexManager
from ..utils.caching import CacheManager

class KnowledgeBase:
    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.graph = Graph()
        self.graph.parse(data=self.ontology.serialize(format='turtle'), format='turtle')
        self.index_manager = IndexManager(self.graph)
        self.cache_manager = CacheManager()

    def update(self, new_facts: dict):
        for subject, predicate, obj in new_facts.items():
            self.graph.add((URIRef(subject), URIRef(predicate), Literal(obj)))
        self.validate_consistency()
        self.index_manager.update_indexes()

    def query(self, query: str) -> list:
        cached_result = self.cache_manager.get(query)
        if cached_result:
            return cached_result

        results = self.graph.query(query)

        result_list = []
        for row in results:
            result_dict = {}
            for var in results.vars:
                result_dict[str(var)] = row[var]
            result_list.append(result_dict)

        self.cache_manager.set(query, result_list)
        return result_list
        
    def reason(self):
        # Apply reasoning rules based on the Business Model Canvas ontology
        # Example rule: If a Value Proposition targets a Customer Segment, 
        # then that Customer Segment is served by the Value Proposition
        rule = """
            PREFIX bmc: <http://example.com/business-model-canvas#>
            CONSTRUCT {
                ?customer_segment bmc:isServedBy ?value_proposition .
            }
            WHERE {
                ?value_proposition bmc:targets ?customer_segment .
            }
        """
        self.graph.update(rule)
        self.validate_consistency()
        self.index_manager.update_indexes()

    def validate_consistency(self):
        # Implement consistency checking algorithms
        # Example: Check for logical inconsistencies or constraint violations
        inconsistencies = self.check_logical_inconsistencies()
        violations = self.check_constraint_violations()
        
        if inconsistencies or violations:
            self.repair_knowledge(inconsistencies, violations)

    def check_logical_inconsistencies(self):
        # Implement logic to check for logical inconsistencies in the knowledge base
        # Return a list of inconsistencies found
        inconsistencies = []

        # Check for logical inconsistencies, such as contradictory facts
        # Example: A and not A cannot both be true
        query = """
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o .
                ?s ?p ?o2 .
                FILTER (?o != ?o2)
            }
        """
        contradictions = self.graph.query(query)
        for contradiction in contradictions:
            inconsistencies.append(contradiction)

        # Check for inconsistencies in class hierarchies
        # Example: If A is a subclass of B, an instance of A cannot also be an instance of a class disjoint with B
        query = """
            SELECT ?instance ?classA ?classB
            WHERE {
                ?instance a ?classA .
                ?instance a ?classB .
                ?classA owl:disjointWith ?classB .
            }
        """
        hierarchy_inconsistencies = self.graph.query(query)
        for inconsistency in hierarchy_inconsistencies:
            inconsistencies.append(inconsistency)

        return inconsistencies

    def check_constraint_violations(self):
        # Implement logic to check for constraint violations in the knowledge base
        # Return a list of violations found
        violations = []

        # Check for cardinality constraint violations
        # Example: If a property has a maximum cardinality of 1, check for instances with multiple values
        query = """
            SELECT ?s ?p
            WHERE {
                ?p owl:maxCardinality 1 .
                ?s ?p ?o1 .
                ?s ?p ?o2 .
                FILTER (?o1 != ?o2)
            }
        """
        cardinality_violations = self.graph.query(query)
        for violation in cardinality_violations:
            violations.append(violation)

        # Check for datatype constraint violations
        # Example: If a property has a specific datatype (e.g., xsd:integer), check for instances with invalid values
        query = """
            SELECT ?s ?p ?o
            WHERE {
                ?p rdfs:range ?datatype .
                ?s ?p ?o .
                FILTER (!datatype(?o, ?datatype))
            }
        """
        datatype_violations = self.graph.query(query)
        for violation in datatype_violations:
            violations.append(violation)

        return violations

    def repair_knowledge(self, inconsistencies, violations):
        # Implement knowledge repair mechanisms to resolve inconsistencies and violations
        # Example: Remove conflicting facts or adjust the knowledge base to satisfy constraints
        for inconsistency in inconsistencies:
            # Remove conflicting facts
            self.graph.remove((inconsistency[0], None, None))
            self.graph.remove((None, None, inconsistency[0]))

        for violation in violations:
            if len(violation) == 2:  # Cardinality violation
                subject, predicate = violation
                # Remove excess values
                values = list(self.graph.objects(subject, predicate))
                for value in values[1:]:
                    self.graph.remove((subject, predicate, value))
            elif len(violation) == 3:  # Datatype violation
                subject, predicate, value = violation
                # Remove the invalid value
                self.graph.remove((subject, predicate, value))
