import threading

class DataStorage:
    def __init__(self):
        self.data = {}  # Dictionary to store data
        self.data_lock = threading.Lock()  # Lock for synchronizing access to data

    def store_data(self, key, value):
        # Store data with the given key
        with self.data_lock:
            self.data[key] = value

    def retrieve_data(self, key):
        # Retrieve data with the given key
        with self.data_lock:
            if key in self.data:
                return self.data[key]
            else:
                raise KeyError(f"Data with key {key} does not exist.")

    def update_data(self, key, value):
        # Update data with the given key
        with self.data_lock:
            if key in self.data:
                self.data[key] = value
            else:
                raise KeyError(f"Data with key {key} does not exist.")

    def delete_data(self, key):
        # Delete data with the given key
        with self.data_lock:
            if key in self.data:
                del self.data[key]
            else:
                raise KeyError(f"Data with key {key} does not exist.")

    def clear_data(self):
        # Clear all stored data
        with self.data_lock:
            self.data.clear()

    def get_all_data(self):
        # Retrieve all stored data
        with self.data_lock:
            return self.data.copy()
