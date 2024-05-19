class CommunicationOntology:
    def __init__(self):
        self.ontology = {
        "request": {"description": "Request for information or action"},
        "inform": {"description": "Provide information"},
        "propose": {"description": "Propose a course of action"},
        "agree": {"description": "Agree to a proposal"},
        "refuse": {"description": "Refuse a proposal"},
        # ...
        }

    def get_meaning(self, term: str) -> str:
        return self.ontology.get(term, {}).get("description", "")