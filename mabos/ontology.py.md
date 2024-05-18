

```python
class Ontology:
    def __init__(self, concepts: dict, relationships: dict):
        self.concepts = concepts
        self.relationships = relationships

    def expand(self, new_concepts: dict, new_relationships: dict):
        self.concepts.update(new_concepts)
        self.relationships.update(new_relationships)
```