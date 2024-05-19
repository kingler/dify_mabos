# mabos/monitoring/performance_metrics_collector.py
class PerformanceMetricsCollector:
    def __init__(self, monitoring_storage):
        self.monitoring_storage = monitoring_storage
        # Initialize other attributes and components
        self.metrics_storage = {}  # Dictionary to store collected metrics
        self.supported_components = ['core', 'knowledge_management', 'reasoning', 'planning', 'execution']  # List of supported components
        self.metrics_collection_interval = 60  # Interval (in seconds) at which to collect metrics
        self.metrics_aggregation_functions = ['avg', 'max', 'min', 'sum']  # List of supported aggregation functions
        self.anomaly_detection_engine = None  # Reference to the anomaly detection engine

    def collect_metrics(self, component):
        # Collect performance metrics from a specific component
        if component in self.supported_components:
            if component == 'core':
                metrics = self._collect_core_metrics()
            elif component == 'knowledge_management':
                metrics = self._collect_knowledge_management_metrics()
            elif component == 'reasoning':
                metrics = self._collect_reasoning_metrics()
            elif component == 'planning':
                metrics = self._collect_planning_metrics()
            elif component == 'execution':
                metrics = self._collect_execution_metrics()
            else:
                raise ValueError(f"Unsupported component: {component}")
            
            self.metrics_storage[component] = metrics
            self.store_metrics(metrics)
        else:
            raise ValueError(f"Unsupported component: {component}")

    def store_metrics(self, metrics):
        # Store the collected metrics in the monitoring storage
        self.monitoring_storage.store_metrics(metrics)

    def retrieve_metrics(self, component, time_range):
        # Retrieve performance metrics for a component within a time range
        if component in self.supported_components:
            metrics = self.monitoring_storage.retrieve_metrics(component, time_range)
            return metrics
        else:
            raise ValueError(f"Unsupported component: {component}")

    def aggregate_metrics(self, component, aggregation_function):
        # Aggregate performance metrics for a component using a specified function
        if component in self.supported_components:
            if aggregation_function in self.metrics_aggregation_functions:
                metrics = self.retrieve_metrics(component, time_range='all')
                if aggregation_function == 'avg':
                    aggregated_metrics = self._calculate_average(metrics)
                elif aggregation_function == 'max':
                    aggregated_metrics = self._calculate_maximum(metrics)
                elif aggregation_function == 'min':
                    aggregated_metrics = self._calculate_minimum(metrics)
                elif aggregation_function == 'sum':
                    aggregated_metrics = self._calculate_sum(metrics)
                else:
                    raise ValueError(f"Unsupported aggregation function: {aggregation_function}")
                return aggregated_metrics
            else:
                raise ValueError(f"Unsupported aggregation function: {aggregation_function}")
        else:
            raise ValueError(f"Unsupported component: {component}")
