# mabos/process_management/process_instance_repository.py
import threading
from repository_management.repository_base import RepositoryBase

class ProcessInstanceRepository(RepositoryBase):
    """
    Repository class for managing process instances.

    Attributes:
        data_store: Data store for persisting process instances.
        process_instances: Dictionary to store process instances.
        process_instance_storage: Storage for persisting process instances.
        process_instance_cache: Cache for frequently accessed process instances.
        process_instance_lock: Lock for synchronizing access to process instances.
        process_instance_version_history: Dictionary to store version history of process instances.
    """

    def __init__(self, data_store):
        """
        Initialize the ProcessInstanceRepository.

        Args:
            data_store: Data store for persisting process instances.
        """
        self.data_store = data_store
        # Initialize other attributes and components
        self.process_instances = {}  # Dictionary to store process instances
        self.process_instance_storage = data_store  # Storage for persisting process instances
        self.process_instance_cache = {}  # Cache for frequently accessed process instances
        self.process_instance_lock = threading.Lock()  # Lock for synchronizing access to process instances
        self.process_instance_version_history = {}  # Dictionary to store version history of process instances

    def create_process_instance(self, process_instance):
        """
        Create a new process instance.

        Args:
            process_instance: Process instance to be created.

        Raises:
            ValueError: If the process instance with the same ID already exists.
        """
        with self.process_instance_lock:
            process_instance_id = process_instance['id']
            if process_instance_id not in self.process_instances:
                self.process_instances[process_instance_id] = process_instance
                self.process_instance_storage.store_process_instance(process_instance)
                self.process_instance_cache[process_instance_id] = process_instance
                self.process_instance_version_history.setdefault(process_instance_id, []).append(process_instance)
            else:
                raise ValueError(f"Process instance with ID {process_instance_id} already exists.")

    def update_process_instance(self, process_instance):
        """
        Update an existing process instance.

        Args:
            process_instance: Process instance to be updated.

        Raises:
            ValueError: If the process instance with the specified ID does not exist.
        """
        with self.process_instance_lock:
            process_instance_id = process_instance['id']
            if process_instance_id in self.process_instances:
                self.process_instances[process_instance_id] = process_instance
                self.process_instance_storage.update_process_instance(process_instance)
                self.process_instance_cache[process_instance_id] = process_instance
                self.process_instance_version_history[process_instance_id].append(process_instance)
            else:
                raise ValueError(f"Process instance with ID {process_instance_id} does not exist.")

    def retrieve_process_instance(self, process_instance_id):
        """
        Retrieve a process instance by its ID.

        Args:
            process_instance_id: ID of the process instance to retrieve.

        Returns:
            The retrieved process instance.

        Raises:
            ValueError: If the process instance with the specified ID does not exist.
        """
        with self.process_instance_lock:
            if process_instance_id in self.process_instance_cache:
                return self.process_instance_cache[process_instance_id]
            elif process_instance_id in self.process_instances:
                process_instance = self.process_instances[process_instance_id]
                self.process_instance_cache[process_instance_id] = process_instance
                return process_instance
            else:
                process_instance = self.process_instance_storage.retrieve_process_instance(process_instance_id)
                if process_instance:
                    self.process_instances[process_instance_id] = process_instance
                    self.process_instance_cache[process_instance_id] = process_instance
                    return process_instance
                else:
                    raise ValueError(f"Process instance with ID {process_instance_id} does not exist.")

    def delete_process_instance(self, process_instance_id):
        """
        Delete a process instance by its ID.

        Args:
            process_instance_id: ID of the process instance to delete.

        Raises:
            ValueError: If the process instance with the specified ID does not exist.
        """
        with self.process_instance_lock:
            if process_instance_id in self.process_instances:
                del self.process_instances[process_instance_id]
                self.process_instance_storage.delete_process_instance(process_instance_id)
                if process_instance_id in self.process_instance_cache:
                    del self.process_instance_cache[process_instance_id]
                if process_instance_id in self.process_instance_version_history:
                    del self.process_instance_version_history[process_instance_id]
            else:
                raise ValueError(f"Process instance with ID {process_instance_id} does not exist.")
