# mabos/process_management/process_definition_repository.py
import threading

from repository_management.repository_base import RepositoryBase

class ProcessDefinitionRepository(RepositoryBase):
    def __init__(self, data_store):
        """
        Initialize the ProcessDefinitionRepository.

        Args:
            data_store: The data store to be used by the repository.
        """
        super().__init__(data_store)
        self.process_definitions = {}  # Dictionary to store process definitions
        self.process_definition_version_history = {}  # Dictionary to store version history of process definitions

    def create(self, process_definition):
        """
        Create a new process definition.

        Args:
            process_definition: The process definition to be created.
        """
        process_definition_id = process_definition['id']
        self._create_item(process_definition_id, process_definition, self.process_definitions, 
                          self.process_definition_version_history)

    def update(self, process_definition):
        """
        Update an existing process definition.

        Args:
            process_definition: The process definition to be updated.
        """
        process_definition_id = process_definition['id']
        self._update_item(process_definition_id, process_definition, self.process_definitions, 
                          self.process_definition_version_history)

    def retrieve(self, process_definition_id):
        """
        Retrieve a process definition by its ID.

        Args:
            process_definition_id: The ID of the process definition to be retrieved.

        Returns:
            The retrieved process definition.
        """
        return self._retrieve_item(process_definition_id, self.process_definitions)

    def delete(self, process_definition_id):
        """
        Delete a process definition by its ID.

        Args:
            process_definition_id: The ID of the process definition to be deleted.
        """
        self._delete_item(process_definition_id, self.process_definitions, 
                          self.process_definition_version_history)

