# mabos/data_management/data_transformation_manager.py
from mabos.logging.logger import Logger
from mabos.configuration.configuration_manager import ConfigurationManager
from mabos.data_management.data_mapper import DataMapper
from mabos.data_management.data_validation_manager import DataValidationManager

class DataTransformationManager:
    def __init__(self, transformation_rules, logger, config_manager, data_mapper, data_validator, transformation_engine):
        self.transformation_rules = transformation_rules
        # Initialize other attributes and components
        self.logger = Logger()
        self.config_manager = ConfigurationManager()
        self.data_mapper = DataMapper()
        self.data_validator = DataValidationManager()
        self.transformation_engine = DataTransformationManager(self.transformation_rules)

    def transform_data(self, data, target_format):
        # Transform the data into the specified target format
        try:
            validated_data = self.data_validator.validate_data(data)
            mapped_data = self.data_mapper.map_data(validated_data, target_format)
            transformed_data = self.transformation_engine.apply_data_transformations(mapped_data)
            self.logger.log(f"Data transformed successfully to target format: {target_format}")
            return transformed_data
        except Exception as e:
            self.logger.log(f"Error during data transformation: {str(e)}", level="error")
            raise

    def map_data_fields(self, source_data, target_data):
        # Map the fields from the source data to the target data
        mapped_data = {}
        for source_field, target_field in self.data_mapper.mapping_rules.items():
            if source_field in source_data:
                mapped_data[target_field] = source_data[source_field]
        target_data.update(mapped_data)

    def apply_data_transformations(self, data):
        # Apply a series of data transformations to the given data
        transformed_data = data.copy()
        for transformation_rule in self.transformation_rules:
            field = transformation_rule['field']
            transformation = transformation_rule['transformation']
            if field in transformed_data:
                value = transformed_data[field]
                transformed_value = self.apply_transformation(value, transformation)
                transformed_data[field] = transformed_value
        return transformed_data
