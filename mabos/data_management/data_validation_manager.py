# mabos/data_management/data_validation_manager.py
from mabos.logging.logger import Logger
from mabos.configuration.configuration_manager import ConfigurationManager
from mabos.data_management.data_mapper import DataMapper


class DataValidationManager:
    def __init__(self, validation_rules):
        self.validation_rules = validation_rules
        # Initialize other attributes and components
        self.logger = Logger()
        self.config_manager = ConfigurationManager()
        self.data_mapper = DataMapper(self.config_manager.get_configuration('data_mapping_rules'))
        self.validation_engine = ValidationEngine(self.validation_rules)

    def validate_data(self, data):
        # Validate the data against the defined validation rules
        errors = self.validation_engine.validate(data)
        if errors:
            self.logger.log(f"Validation errors: {errors}", level="error")
            return False
        else:
            self.logger.log("Data validation successful")
            return True

    def clean_data(self, data):
        # Clean and sanitize the data based on predefined rules
        cleaned_data = {}
        for field, value in data.items():
            if field in self.data_mapper.mapping_rules:
                cleaned_value = self.sanitize_value(value)
                cleaned_data[field] = cleaned_value
        return cleaned_data

    def get_validation_errors(self, data):
        # Retrieve validation errors for the given data
        errors = self.validation_engine.validate(data)
        return errors


class ValidationEngine:
    def __init__(self, validation_rules):
        self.validation_rules = validation_rules

    def validate(self, data):
        errors = []
        for rule in self.validation_rules:
            field = rule['field']
            validator = rule['validator']
            if field in data:
                value = data[field]
                if not validator(value):
                    error_message = rule.get('error_message', f"Validation failed for field: {field}")
                    errors.append(error_message)
        return errors
