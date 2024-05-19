# mabos/configuration/configuration_manager.py
import os
import yaml

class ConfigurationManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_configuration()
        self.components = {}
        self.config_validators = {}
        self.config_loaders = {}
        self.config_savers = {}

    def load_configuration(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                return yaml.safe_load(file)
        else:
            return {}

    def save_configuration(self):
        with open(self.config_file, 'w') as file:
            yaml.dump(self.config_data, file)

    def get_configuration(self, component):
        if component in self.config_data:
            return self.config_data[component]
        else:
            raise ValueError(f"Component {component} not found in the configuration")

    def update_configuration(self, component, config_data):
        if component in self.components:
            if self.validate_configuration(component, config_data):
                self.config_data[component] = config_data
                self.save_configuration()
            else:
                raise ValueError(f"Invalid configuration data for component {component}")
        else:
            raise ValueError(f"Component {component} not found in the configuration manager")

    def validate_configuration(self, component, config_data):
        if component in self.config_validators:
            validator = self.config_validators[component]
            return validator(config_data)
        else:
            raise ValueError(f"No validator found for component {component}")
